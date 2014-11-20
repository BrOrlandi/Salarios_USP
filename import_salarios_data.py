
import sys
import codecs

from settings import *
from sqlalchemy.orm import sessionmaker

from models import *

# db session
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
s = session()

args = sys.argv
if len(args) > 1:
	f = codecs.open(args[1],mode='r',encoding='utf-8')
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
else:
	print "Entre com um arquivo csv com os salarios."