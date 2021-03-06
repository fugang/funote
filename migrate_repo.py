# -*- coding: cp936 -*-
from sqlalchemy import *

meta = MetaData()

engine = create_engine("sqlite:///tmp/quill.db")

quillbase = Table("quillbase", meta,
                  Column("click_count",Integer()),
                  Column("created_at",DateTime()),
                  Column("id", Integer(), primary_key=True, nullable=False),
                  Column("regin_id",Integer(),nullable=False),
                  Column("user_id",String(100)),
                  Column("header", String(500)),
                  Column("text", Text(5000)),
                  Column("html", Text(500000)),
                  Index("regin_id","regin_id"),
                  )
reginbase = Table("reginbase", meta,
                  Column("created_at", DateTime()),
                  Column("id", Integer(), primary_key=True, nullable=False),
                  Column("title",String(50)),
                  )

meta.create_all(engine)

conn = engine.connect()
conn.execute(
    reginbase.insert(),
    {"title":u"����"},
    {"title":u"�ʼ�"},
)
