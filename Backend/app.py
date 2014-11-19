# -*- coding: utf-8 -*-

from flask import Flask, Response
app = Flask(__name__)

import os
import json
import sys
import codecs

from models import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound


# start db conection
if os.getenv("MODE",None):
	app.debug = False
	print os.environ['MODE']
else: # dev mode
	app.debug = True
	engine = create_engine('sqlite:///database.sqlite',encoding='utf8')

	
# db session
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
s = session()


args = sys.argv
if len(args) > 2 and args[1] == "import":
	f = codecs.open(args[2],mode='r',encoding='utf-8')
	f.readline() # header line
	c = 1
	for line in f:
		spl = line.split("\t")
		if len(spl) == 14:
			novo = SalarioUSP()
			novo.categoria = unicode(spl[0])
			novo.classe = unicode(spl[1])
			novo.departamento = unicode(spl[2])
			novo.funcao = unicode(spl[3])
			novo.jornada = unicode(spl[4])
			novo.jornada_ext = unicode(spl[5])
			novo.nome = unicode(spl[6])
			novo.ref_ms = unicode(spl[7])
			novo.tempo_usp = int(spl[8])
			novo.unidade = unicode(spl[9])
			novo.unidade_ext = unicode(spl[10])
			novo.sal_liquido = float(spl[11].replace(',','.'))
			novo.parcelas_eventuais = float(spl[12].replace(',','.'))
			novo.salario = float(spl[13].replace(',','.'))
			s.add(novo)
		c += 1
		print c
	s.commit()
	f.close()
	sys.exit()




@app.route("/")
def hello():
    return "Hello Salários USP!"

@app.route("/by_name/<name>")
def by_name(name):
	r = s.query(SalarioUSP).filter(SalarioUSP.nome.ilike("%"+name+"%"))
	json_r = [ serialize(sal) for sal in r]
	if len(json_r) == 0:
		code = 1
		data = u"Salário não encontrado."
	else:
		code = 0
		data = json_r
	response = {'code': code, 'data': data}
	json_str = json.dumps(response)
	return Response(json_str, mimetype='application/json')

@app.route("/icmc/<page_id>")
def icmc(page_id):
	try:
		r = s.query(Page_ICMC).filter(Page_ICMC.page_id == int(page_id)).one()
		json_r = serialize(r.salario_usp)
	except NoResultFound:
		json_r = None
	if json_r == None:
		code = 1
		data = u"Salário não encontrado."
	else:
		code = 0
		data = json_r
	response = {'code': code, 'data': data}
	json_str = json.dumps(response)
	return Response(json_str, mimetype='application/json')



if __name__ == "__main__":
    app.run()