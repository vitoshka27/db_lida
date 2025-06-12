from orm_db import SessionLocal
from sqlalchemy.orm import joinedload

class BaseService:
    def __init__(self, model_cls):
        self.model_cls = model_cls

    def get_all(self, limit=None, offset=None, filters=None):
        session = SessionLocal()
        query = session.query(self.model_cls)
        for rel in self.model_cls.__mapper__.relationships:
            query = query.options(joinedload(getattr(self.model_cls, rel.key)))
        if filters:
            for k, v in filters.items():
                query = query.filter(getattr(self.model_cls, k) == v)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        result = query.all()
        session.close()
        return result

    def get_page(self, page=1, page_size=20, filters=None):
        session = SessionLocal()
        query = session.query(self.model_cls)
        for rel in self.model_cls.__mapper__.relationships:
            query = query.options(joinedload(getattr(self.model_cls, rel.key)))
        if filters:
            for k, v in filters.items():
                query = query.filter(getattr(self.model_cls, k) == v)
        total = query.count()
        result = query.offset((page-1)*page_size).limit(page_size).all()
        session.close()
        return result, total

    def get_by_id(self, id):
        session = SessionLocal()
        obj = session.get(self.model_cls, id)
        session.close()
        return obj

    def create(self, **kwargs):
        session = SessionLocal()
        obj = self.model_cls(**kwargs)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        session.close()
        return obj

    def update(self, id, **kwargs):
        session = SessionLocal()
        obj = None
        if isinstance(id, tuple):
            pk_cols = [col.name for col in self.model_cls.__table__.primary_key.columns]
            filter_kwargs = dict(zip(pk_cols, id))
            obj = session.query(self.model_cls).filter_by(**filter_kwargs).first()
        else:
            obj = session.get(self.model_cls, id)
        if obj is None:
            session.close()
            raise Exception('Object not found')
        for k, v in kwargs.items():
            setattr(obj, k, v)
        session.commit()
        session.refresh(obj)
        session.close()
        return obj

    def delete(self, id):
        session = SessionLocal()
        obj = None
        if isinstance(id, tuple):
            pk_cols = [col.name for col in self.model_cls.__table__.primary_key.columns]
            filter_kwargs = dict(zip(pk_cols, id))
            obj = session.query(self.model_cls).filter_by(**filter_kwargs).first()
        else:
            obj = session.get(self.model_cls, id)
        if obj is None:
            session.close()
            raise Exception('Object not found')
        session.delete(obj)
        session.commit()
        session.close() 