# -*- coding:utf-8 -*-

from models import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy import func


from settings import *

	
# db session
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
s = session()


import requests
import bs4
import urlparse
import codecs
from unidecode import unidecode


def parse_icmc_page(url,pages):
	# starts parsing

	fn = codecs.open("notfound",mode='a',encoding='utf-8')
	fm = codecs.open("multiplefound",mode='a',encoding='utf-8')

	# load all names
	qnames = s.query(SalarioUSP.id, SalarioUSP.nome)
	pids = [c[0] for c in qnames]
	pnames = [unidecode(c[1]) for c in qnames]

	for page in xrange(1,pages+1):
		print "Page: "+str(page)
		response = requests.get(url+str(page))
		response.encoding = 'utf-8'
		txt = response.text
		soup = bs4.BeautifulSoup(txt)
		people = soup.select("a > b")

		links = [a.parent for a in people]


		for x in links:
			urlp = x['href']
			parsed = urlparse.parse_qs(urlparse.urlparse(urlp).query)
			catch = {}
			catch['page_id'] = int(parsed['id'][0])
			catch['nome'] = unicode(x.b.string)
			print catch['nome']

			try:
				#found = s.query(SalarioUSP).filter(unidecode(SalarioUSP.nome.value()) == unidecode(catch['nome'])).one()
				
				occurrences = [i for i,x in enumerate(pnames) if x == unidecode(catch['nome'])]
				if len(occurrences) == 0:
					raise NoResultFound
				if len(occurrences) > 1:
					raise MultipleResultsFound

				found = s.query(SalarioUSP).filter(SalarioUSP.id == pids[occurrences[0]]).one()
				new_page = Page_ICMC()
				new_page.page_id = catch['page_id']
				new_page.salario_usp = found
				s.add(new_page)
			except NoResultFound:
				print str(catch['page_id']) + "\t"+catch['nome'] + u" NÃO ENCONTRADO!"
				fn.write(str(catch['page_id']) + "\t"+catch['nome']+"\n")
			except MultipleResultsFound:
				print str(catch['page_id']) + "\t"+catch['nome'] + u" MULTIPLOS ENCONTRADO!"
				fm.write(str(catch['page_id']) + "\t"+catch['nome']+"\n")

	fn.close()
	fm.close()


def add_manually(name, pid):
	new_page = Page_ICMC()
	found = s.query(SalarioUSP).filter(SalarioUSP.nome.ilike(name)).one()
	new_page.page_id = pid
	new_page.salario_usp = found
	s.add(new_page)

def not_found_solved():
	add_manually(u"Cynthia de Oliveira Lage Ferreira",14820182)
	add_manually(u"Beatriz Helena Souza Ceneviva Deiroz",4883306)
	add_manually(u"Marcelo Carlos Serra da Silva",7216924)
	add_manually(u"Monique Derisso",10540642)
	add_manually(u"Rosemeire do Amaral Cesar",4866806)
	add_manually(u"Sandra Cavalcante de Albuquerque Soligon",4899984)

	add_manually(u"Siumara Therezinha Taconelli Franchin",4990006)
	add_manually(u"Paulo Ferreira da Silva Porto Junior",65104)
	add_manually(u"Leonardo Tadashi Miyake",11269724)
	add_manually(u"Alfredo Rafael Roa Narvaez",11670202)
	add_manually(u"Roberto Federico Ausas",14781026)
	add_manually(u"Washington Luiz Marar",4176144)

	# multiple	
	new_page = Page_ICMC()
	found = s.query(SalarioUSP).filter(SalarioUSP.nome.ilike(u"Luiz Antonio dos Santos")).filter(SalarioUSP.funcao.like("Jardineiro")).one()
	new_page.page_id = 4841818
	new_page.salario_usp = found
	s.add(new_page)




se = s.query(Page_ICMC).delete()
parse_icmc_page('http://www.icmc.usp.br/Portal/Pessoas/index.php?categ=Docente&p=',6)
parse_icmc_page('http://www.icmc.usp.br/Portal/Pessoas/index.php?categ=Func&p=',5)
parse_icmc_page('http://www.icmc.usp.br/Portal/Pessoas/index.php?categ=Apos&p=',3)

not_found_solved()

s.commit()

# count ICMC
se = s.query(Page_ICMC).all()
print len(se)

# ICMC but don't has page
# se = s.query(SalarioUSP).filter(SalarioUSP.unidade == "ICMC").filter(SalarioUSP.salario_usp == None).all()
# aa =  [x for x in se]
# for a in aa:
# 	print serialize(a)
# print len(se)
