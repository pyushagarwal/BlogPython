from main_application import *
try:
	init_db()
	print 'Databases initialised'
except Exception,err:
	print traceback.format_exc()  