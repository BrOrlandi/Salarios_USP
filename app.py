# -*- coding: utf-8 -*-

from flask import Flask, Response
app = Flask(__name__)

import json

from models import *

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from settings import *

app.debug = DEBUG
	
# db session
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
s = session()

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