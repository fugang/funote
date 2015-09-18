from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, DateTime, Index
from datetime import datetime
from sqlalchemy.orm import sessionmaker, joinedload,load_only,object_mapper
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def get_session():
    engine = create_engine("sqlite:///tmp/quill.db")
    Session = sessionmaker(bind=engine, autocommit=True,
                           expire_on_commit = False)
    return Session()

class MyBase(object):
    def save(self, session=None):
        if not session:
            session = get_session()
        session.add(self)
        session.flush()
    def update(self, values):
        for k, v in values.iteritems():
            setattr(self, k, v)
    def __getitem__(self, key):
        return getattr(self, key)
    def get(self, key, default=None):
        return getattr(self, key, default)
    def __iter__(self):
        self._i = iter(object_mapper(self).columns)
        return self
    def iteritems(self):
        local = dict(self)
        joined = dict([(k, v) for k, v in self.__dict__.iteritems()
                      if not k[0] == "_"])
        local.update(joined)
        return local.iteritems()
    
class QuillBase(Base, MyBase):
    __tablename__ = "quillbase"
    __table_args__ = (
        Index("regin_id","regin_id"),
    )
    created_at = Column(DateTime, default=datetime.now())
    id = Column(Integer, primary_key=True,nullable=False)
    regin_id = Column(Integer,nullable=False)
    user_id = Column(String(100))
    header = Column(String(500))
    text = Column(Text(5000))
    html = Column(Text(50000))

class ReginBase(Base, MyBase):
    __tablename__ = "reginbase"
    created_at = Column(DateTime, default=datetime.now())
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(50))

def add_quill(values):
    quill = QuillBase()
    quill.update(values)
    quill.save()
    return quill

def add_regin(value):
    regin = ReginBase()
    regin.update(value)
    regin.save()
    return regin

def update_quill(tid, values):
    session = get_session()
    with session.begin():
        quilltext = session.query(QuillBase).filter_by(id=tid).first()
        quilltext.update(values)
        quilltext.save(session=session)

def get_quill_header_by_regin(reg_id, user_id):
    session = get_session()
    return session.query(QuillBase).options(load_only("header"))\
                                   .filter_by(regin_id=reg_id)\
                                   .filter_by(user_id=user_id)\
                                   .all()

def get_quill_by_regin(reg_id, user_id):
    session = get_session()
    return session.query(QuillBase).filter_by(regin_id=reg_id)\
                                   .filter_by(user_id=user_id)\
                                   .all()
    
def get_quill_by_id(tid):
    session = get_session()
    return session.query(QuillBase).filter_by(id=tid).first()

def get_regins():
    session = get_session()
    return session.query(ReginBase).all()

def query_text(keywd):
    session = get_session()
    keystr = "%%%s%%" % keywd
    print keystr
    return session.query(QuillBase).filter(QuillBase.text.like(keystr)).all()
