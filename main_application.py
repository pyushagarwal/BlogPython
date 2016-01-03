import sqlite3,os
from flask import *
import traceback

#Configuration
DATABASE = '.\\tmp\\database.txt'
DEBUG = False
USERNAME = 'piyush'
PASSWORD = '1234'
SECRET_KEY = 'abcj'

#Initialisation
app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	db = connect_db()
	with db:
		sql_query = app.open_resource('schemas.sql', mode = 'r')
		db.executescript(sql_query.read())
		db.commit()

def modify_post(post_id, new_heading, new_detail):
	print 'modify_post invoked'
	try:
		g.db.execute('update entries set heading = ?, detail = ? where id = ?',[new_heading, new_detail, post_id])
		g.db.commit()
	except:
		print 'post method error'
	print 'modify_post terminated'		

def get_EditablePostHistory(post_id):
	print 'editable(): ',post_id
	try:
		result_query = g.db.execute('select heading,detail from entries where id = ?', [post_id])
	except Exception:
		print traceback.format_exc()
	result_tuple = result_query.fetchall()
	result_list = list()
	for x,y in result_tuple:
		result_list.append(dict(heading=x,detail=y,post_id=post_id))
	return render_template('edit_entry.html',result = result_list)	


@app.before_request
def before_request():
	g.db = connect_db()
	g.db.execute('PRAGMA foreign_keys = ON')


@app.route('/')
def show_entries():
	print 'Sample\n'
	try:
		cur = g.db.execute("""select entries.id,heading,detail,users.username,likes from entries inner join users on users.uid = entries.uid  order by entries.id desc""")
	except Exception:
		return str(traceback.format_exc())
	entries_tuple =  cur.fetchall() #list of tuples
	entries_list = list()
	for post_id,heading,detail,username,likes in entries_tuple:
		
		#liked = 2 for loggged_out users
		#liked = 1 for loggged_in users who have liked
		#liked = 0 for loggged_in users who have not liked

		liked = 2

		if 'logged_in' in session:
			liked = g.db.execute('select count(*) from likes where post_id=? and uid = ?',[post_id,session['logged_in']]).fetchall()[0][0]
		entries_list.append(dict(heading = heading, detail = detail, username = username, post_id = post_id ,likes =likes ,liked = liked ))
	return render_template('show_entries.html', entries = entries_list)


@app.route('/add_entry', methods=['POST'])
def add_entry():
	if session['logged_in']:
		try:
			var_heading = request.form['heading']
			var_detail =  request.form['detail']
			var_user = session['logged_in']
			g.db.execute('insert into entries (heading, detail,uid) values (?, ?, ?)',
	                 [var_heading, var_detail, var_user ])
			g.db.commit()
		except:
			print 'insertion error'
	return redirect(url_for('show_entries'))



@app.route('/login',methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		t_username = request.form['username']
		t_password = request.form['password']
		print 'username: ', t_username, 'password: ', t_password
		try:
			result_query = g.db.execute(""" select uid from users  where username = ? and password=? 
				""", [t_username, t_password])
		except Exception:
			print 'database check exception'
			print traceback.format_exc()
		
		result_tuple = result_query.fetchall() 	
		
		if len(result_tuple):
			print 'logged in with userid: ' , result_tuple[0][0]
			session['logged_in'] = result_tuple[0][0]
			session['username'] = t_username
			return redirect(url_for('show_entries'))
		else :
			error_on_login = 'Wrong username or password'
			print error_on_login
			return render_template('login.html', error = error_on_login)
	else:
		return render_template('login.html')	



@app.route('/logout',methods=['GET'])
def logout():
	del session['logged_in']
	del session['username']
	return redirect(url_for('show_entries')) 

@app.route('/edit_entry/<post_id>',methods = ['GET','POST'])
def edit_entry(post_id):

	#check for  logged out
	if not 'logged_in' in session:
		return render_template('layout.html',error = 'Unauthorised Access') 

	try:
		result_query = g.db.execute('select uid from entries where id = ?',[post_id])
	except Exception:
		print traceback.format.exc()
	result_tuple = result_query.fetchall()
	if session['logged_in'] != result_tuple[0][0] :
		error = 'Unauthorised Acess'
		return render_template('layout.html',error = error)
	if request.method == 'GET':
		return get_EditablePostHistory(post_id)	
	else:
		modify_post(post_id, request.form['heading'], request.form['detail'])
		return redirect(url_for('show_entries'))

@app.route('/like/<post_id>',methods=['GET'])
def like(post_id):

	#check for  logged out
	if not 'logged_in' in session:
		return render_template('layout.html',error = 'Unauthorised Access') 

	try:
		g.db.execute('insert into  likes values(?,?)', [session['logged_in'], post_id])
		g.db.execute("""update entries set likes = likes + 1 where id = ? """, [post_id])
		g.db.commit()
	except Exception ,err: #dislike
		print  'Unlike'
		try:
			g.db.execute('delete from likes where uid = ? and post_id = ? ', [session['logged_in'], post_id])
			g.db.execute("""update entries set likes = likes - 1 where id = ? """, [post_id])
			g.db.commit()
		except Exception,err:
			return str(err)+str(traceback.format_exc())
	return redirect(url_for('show_entries'))	


@app.route('/remove/<post_id>',methods=['GET'])
def remove(post_id):
	#check for  logged out
	if not 'logged_in' in session:
		return render_template('layout.html',error = 'Unauthorised Access') 

	try:
		result_query = g.db.execute('select uid from entries where id = ?',[post_id])
	except Exception:
		print traceback.format.exc()
	result_tuple = result_query.fetchall()
	if session['logged_in'] != result_tuple[0][0] :
		error = 'Unauthorised Acess'
		return render_template('layout.html',error = error)
	
	try:
		g.db.execute('delete from likes where post_id = ?',[post_id])
		g.db.execute('delete from entries where id = ?',[post_id])
		g.db.commit()
	except Exception:
		return traceback.format_exc()
	return redirect(url_for('show_entries'))	



if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)