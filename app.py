# -*- coding: utf-8 -*-

from flask import Flask, Response, request
app = Flask(__name__)

import json

from models import *

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from settings import *
from pyga.requests import Tracker, Event, Session, Visitor

app.debug = DEBUG

GA_TRACKER = "UA-56971050-1"
DOMAIN = "brorlandi.me"
	
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
		register_event('ICMC',r.salario_usp.nome)

	response = {'code': code, 'data': data}
	json_str = json.dumps(response)
	return Response(json_str, mimetype='application/json')

def register_event(categ,act):
	tracker = Tracker(GA_TRACKER, DOMAIN)
	visitor = Visitor()
	#visitor.extract_from_server_meta(request.headers)
	visitor.extract_from_server_meta(request.environ)
	session = Session()
	event = Event(category=categ,action=act)
	tracker.track_event(event,session,visitor)



if __name__ == "__main__":
    app.run()