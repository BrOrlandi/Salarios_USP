
from sqlalchemy import create_engine
import os

# start db conection
if os.getenv("MODE",None):
	if os.environ['MODE'] == "PROD":
		DEBUG = False
		db_str = 'postgresql://{user}:{pass}@{host}:{port}/{dbname}'.format(
			user=os.environ['SALARIOUSP_DB_USER'],
			pass=os.environ['SALARIOUSP_DB_PASS'],
			host=os.environ['SALARIOUSP_DB_HOST'],
			port=os.environ['SALARIOUSP_DB_PORT'],
			dbname=os.environ['SALARIOUSP_DB_NAME'])
		engine = create_engine(db_str,encoding='utf8')
else: # dev mode
	DEBUG = True
	engine = create_engine('sqlite:///database.sqlite',encoding='utf8')