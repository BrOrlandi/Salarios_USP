# -*- coding:utf-8 -*-

from models import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy import func


import os
# start db conection
if os.getenv("MODE",None):
	print os.environ['MODE']
else: # dev mode
	engine = create_engine('sqlite:///database.sqlite',encoding='utf8')

	
# db session
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
s = session()


import requests
import bs4
import urlparse



def parse_icmc_page(url,pages):
	# starts parsing

	for page in xrange(1,pages+1):
		response = requests.get(url+str(page))
		soup = bs4.BeautifulSoup(response.text)
		people = soup.select("a > b")
		# print len(people)
		# print [c.string for c in people]

		links = [a.parent for a in people]

		for x in links:
			urlp = x['href']
			parsed = urlparse.parse_qs(urlparse.urlparse(urlp).query)
			catch = {}
			catch['page_id'] = int(parsed['id'][0])
			catch['nome'] = x.b.string
			print unicode(catch['nome'])
			try:
				found = s.query(SalarioUSP).filter(SalarioUSP.nome.ilike("%"+unicode(catch['nome'])+"%")).one()
				new_page = Page_ICMC()
				new_page.page_id = catch['page_id']
				new_page.salario_usp = found
				s.add(new_page)
			except NoResultFound:
				print unicode(catch['nome']) + u" NÃO ENCONTRADO!"

#found = s.query(SalarioUSP).filter(SalarioUSP.nome.ilike("%"+u" Sáles"+"%")).one()
#print found.nome

#parse_icmc_page('http://www.icmc.usp.br/Portal/Pessoas/index.php?categ=Docente&p=',6)
parse_icmc_page('http://www.icmc.usp.br/Portal/Pessoas/index.php?categ=Func&p=',5)

s.commit()