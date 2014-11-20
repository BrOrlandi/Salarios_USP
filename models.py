# -*- coding:utf-8 -*-

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref, class_mapper
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SalarioUSP(Base):
	__tablename__ = "salario_usp"

	id = Column(Integer, primary_key=True)

	# data collumns
	categoria = Column(String(100), nullable=False)
	classe = Column(String(100), nullable=False)
	departamento = Column(String(200), nullable=False)
	funcao = Column(String(100), nullable=False)
	jornada = Column(String(50), nullable=False)
	jornada_ext = Column(String(100), nullable=False)
	nome = Column(String(100), nullable=False)
	ref_ms = Column(String(20), nullable=False)
	tempo_usp = Column(Integer, nullable=False)
	unidade = Column(String(20), nullable=False)
	unidade_ext = Column(String(100), nullable=False)
	sal_liquido = Column(Float, nullable=False)
	parcelas_eventuais = Column(Float, nullable=False)
	salario = Column(Float, nullable=False)

class Page_ICMC(Base):

	__tablename__ = "page_icmc"

	page_id = Column(Integer, primary_key=True)
	sal_id = Column(Integer, ForeignKey("salario_usp.id"), unique=True)
	salario_usp = relationship(SalarioUSP, backref=backref('salario_usp'))

def serialize(model):
  """Transforms a model into a dictionary which can be dumped to JSON."""
  # first we get the names of all the columns on your model
  columns = [c.key for c in class_mapper(model.__class__).columns]
  # then we return their values in a dict
  return dict((c, getattr(model, c)) for c in columns)