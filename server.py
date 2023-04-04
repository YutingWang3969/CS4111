
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@34.73.36.248/project1
#
# For example, if you had username zy2431 and password 123123, then the following line would be:
#
#     DATABASEURI = "postgresql://zy2431:123123@34.73.36.248/project1"
#
# Modify these with your own credentials you received from TA!
DATABASE_USERNAME = "fg2545"
DATABASE_PASSWRD = "4350"
DATABASE_HOST = "34.148.107.47" # change to 34.28.53.86 if you used database 2 for part 2
DATABASEURI = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWRD}@{DATABASE_HOST}/project1"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)
#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.




@app.before_request
def before_request():
	"""
	This function is run at the beginning of every web request 
	(every time you enter an address in the web browser).
	We use it to setup a database connection that can be used throughout the request.

	The variable g is globally accessible.
	"""
	try:
		g.conn = engine.connect()
	except:
		print("uh oh, problem connecting to database")
		import traceback; traceback.print_exc()
		g.conn = None

@app.teardown_request
def teardown_request(exception):
	"""
	At the end of the web request, this makes sure to close the database connection.
	If you don't, the database could run out of memory!
	"""
	try:
		g.conn.close()
	except Exception as e:
		pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: https://flask.palletsprojects.com/en/1.1.x/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index1():

	"""
	request is a special object that Flask provides to access web request information:

	request.method:   "GET" or "POST"
	request.form:     if the browser submitted a form, this contains the data in the form
	request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

	See its API: https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data
	"""

	# DEBUG: this is debugging code to see what request looks like
	print(request.args)


	#
	# example of a database query


	#
	# Flask uses Jinja templates, which is an extension to HTML where you can
	# pass data to a template and dynamically generate HTML based on the data
	# (you can think of it as simple PHP)
	# documentation: https://realpython.com/primer-on-jinja-templating/
	#
	# You can see an example template in templates/index.html
	#
	# context are the variables that are passed to the template.
	# for example, "data" key in the context variable defined below will be 
	# accessible as a variable in index.html:
	#
	#     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
	#     <div>{{data}}</div>
	#     
	#     # creates a <div> tag for each element in data
	#     # will print: 
	#     #
	#     #   <div>grace hopper</div>
	#     #   <div>alan turing</div>
	#     #   <div>ada lovelace</div>
	#     #
	#     {% for n in data %}
	#     <div>{{n}}</div>
	#     {% endfor %}
	
	#
	# render_template looks in the templates/ folder for files.
	# for example, the below file reads template/index.html
	#
	return render_template("index1.html")


#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#



@app.route('/user')
def user():
	return render_template("user.html")

@app.route('/employee')
def employee():
	return render_template("employee.html")

@app.route('/add_order')
def add_order():
	return render_template("add_order.html")

@app.route('/add_racquet')
def add_racquet():
	return render_template("add_racquet.html")

@app.route('/add_string')
def add_string():
	return render_template("add_string.html")

@app.route('/delete_racquet')
def delete_racquet():
	select_query = "SELECT * from racquet"
	cursor = g.conn.execute(text(select_query))
	res = []
	for result in cursor:
		res.append(result[0])
	cursor.close()
	context = dict(data = res)
	return render_template("delete_racquet.html",**context)

@app.route('/delete_string')
def delete_string():
	select_query = "SELECT * from string"
	cursor = g.conn.execute(text(select_query))
	res = []
	for result in cursor:
		res.append(result[0])
	cursor.close()
	context = dict(data = res)
	return render_template("delete_string.html",**context)

@app.route('/delete_order')
def delete_order():
	select_query = "SELECT * from orders"
	cursor = g.conn.execute(text(select_query))
	res = []
	for result in cursor:
		res.append(result)
	cursor.close()
	context = dict(data = res)
	return render_template("delete_order.html",**context)

@app.route('/update_racquet')
def update_racquet():
	select_query = "SELECT * from racquet"
	cursor = g.conn.execute(text(select_query))
	res = []
	for result in cursor:
		res.append(result)
	cursor.close()
	context = dict(data = res)
	return render_template("update_racquet.html",**context)

@app.route('/update_string')
def update_string():
	select_query = "SELECT * from string"
	cursor = g.conn.execute(text(select_query))
	res = []
	for result in cursor:
		res.append(result)
	cursor.close()
	context = dict(data = res)
	return render_template("update_string.html",**context)

@app.route('/update_order')
def update_order():
	select_query = "SELECT * from orders"
	cursor = g.conn.execute(text(select_query))
	res = []
	for result in cursor:
		res.append(result)
	cursor.close()
	context = dict(data = res)
	return render_template("update_order.html",**context)


@app.route('/customer_nocontact', methods=['POST'])
def customer_nocontact():
 cursor = g.conn.execute(text("SELECT oi.*, o.order_id, o.order_date, u.cust_id, u.firstname, u.lastname, u.email_address, u.phone FROM orders o JOIN order_items oi ON o.order_id = oi.order_id JOIN users u ON u.cust_id = o.cust_id WHERE u.email_address IS NULL OR u.phone IS NULL"))
 g.conn.commit()
 record = cursor.fetchall()
 context = dict(data = record)
 print(record)
 cursor.close()
 return render_template('employee.html', **context)


@app.route('/bestsell_racquet', methods=['POST'])
def bestsell_racquet():
 cursor = g.conn.execute(text("SELECT r.racquet_code, r.name, sum(oi.quantity) FROM order_items oi JOIN racquet r ON oi.item_code = r.racquet_code GROUP BY r.racquet_code, r.name ORDER BY SUM(oi.quantity) DESC LIMIT 3"))
 g.conn.commit()
 record = cursor.fetchall()
 context = dict(data = record)
 print(record)
 cursor.close()
 return render_template('employee.html', **context)

@app.route('/bestsell_string', methods=['POST'])
def bestsell_string():
 cursor = g.conn.execute(text("SELECT s.string_code, sum(oi.quantity) FROM order_items oi JOIN string s ON oi.item_code = s.string_code GROUP BY s.string_code ORDER BY SUM(oi.quantity) DESC LIMIT 3"))
 g.conn.commit()
 record = cursor.fetchall()
 context = dict(data = record)
 print(record)
 cursor.close()
 return render_template('employee.html', **context)

# Example of adding new data to the database
@app.route('/athlete_search', methods=['POST'])
def athlete_search():
	athlete_name = request.form['athlete_name']
	cursor = g.conn.execute(text("SELECT * FROM athletes a JOIN use_equipment ue ON a.athlete_id = ue.athlete_id WHERE name = :athlete_name"), {'athlete_name':athlete_name})
	g.conn.commit()
	record = cursor.fetchone()
	context = dict(data = record)
	print(record)
	cursor.close()
	# rows = cur.fetchall()
	# print(list(rows))
	# cur.close()
	# conn.close()
	return render_template('user.html', **context)
	# return redirect("/")

@app.route('/racquet_search', methods=['POST'])
def racquet_search():
	racquet_code = request.form['racquet_code']
	cursor = g.conn.execute("SELECT * FROM racquet WHERE racquet_code=:racquet_code", {'racquet_code':racquet_code})
	g.conn.commit()
	record = cursor.fetchone()
	context = dict(data = record)
	print(record)
	cursor.close()
	return render_template('user.html', **context)


@app.route('/racquet_budget', methods=['POST'])
def racquet_budget():
	racquet_budget = request.form['racquet_budget']
	cursor = g.conn.execute(text("SELECT name, unit_price FROM racquet WHERE unit_price < :racquet_budget"), {'racquet_budget':racquet_budget})
	g.conn.begin().commit()
	record = cursor.fetchall()
	context = dict(data = record)
	print(record)
	cursor.close()
	return render_template('user.html', **context)

@app.route('/string_budget', methods=['POST'])
def string_budget():
	string_budget = request.form['string_budget']
	cursor = g.conn.execute(text("SELECT string_code, unit_price FROM string WHERE unit_price < :string_budget"), {'string_budget':string_budget})
	g.conn.begin().commit()
	record = cursor.fetchall()
	context = dict(data = record)
	print(record)
	cursor.close()
	return render_template('user.html', **context)



####waiting for action name and file name
@app.route('/Delete_racquet', methods=['POST'])
def Delete_racquet():
	racquet_code = request.form['racquet_code']
	cursor = g.conn.execute(text("DELETE FROM racquet WHERE racquet_code = :racquet_code"), {'racquet_code':racquet_code})
	g.conn.commit()
	select_query = "SELECT * from racquet"
	cursor = g.conn.execute(text(select_query))
	res = []
	for result in cursor:
		res.append(result[0])
	context = dict(data = res)
	cursor.close()
	return render_template('delete_racquet.html',**context)

@app.route('/Delete_string', methods=['POST'])
def Delete_string():
	string_code = request.form['string_code']
	cursor = g.conn.execute(text("DELETE FROM string WHERE string_code= string_code"), {'string_code':string_code})
	g.conn.commit()
	select_query = "SELECT * from string"
	cursor = g.conn.execute(text(select_query))
	res = []
	for result in cursor:
		res.append(result[0])
	context = dict(data = res)
	cursor.close()
	return render_template('delete_string.html', **context)

@app.route('/Delete_order', methods=['POST'])
def Delete_order():
	Order_id = request.form['Order_id']
	cursor = g.conn.execute(text("DELETE FROM orders WHERE Order_id= :Order_id"), {'Order_id':Order_id})
	g.conn.commit()
	select_query = "SELECT * from orders"
	cursor = g.conn.execute(text(select_query))
	res = []
	for result in cursor:
		res.append(result)
	context = dict(data = res)
	cursor.close()
	return render_template('delete_order.html', **context)

@app.route('/Update_racquet', methods=['POST'])
def Update_racquet():
	racquet_code = request.form['racquet_code']
	name = request.form['name']
	flex = request.form['flex']
	color = request.form['color']
	unit_price = request.form['unit_price']
	query = """
	UPDATE racquet
	SET name = :name, flex= :flex, color= :color, unit_price= :unit_price
	WHERE racquet_code = :racquet_code
	"""
	params = {
			'racquet_code': racquet_code,
        	'name': name,
        	'flex': flex,
        	'color': color,
        	'unit_price': unit_price
    		}
	cursor = g.conn.execute(text(query), params)
	g.conn.commit()
	select_query = "SELECT * from racquet"
	cursor = g.conn.execute(text(select_query))
	res = []
	for result in cursor:
		res.append(result)
	context = dict(data = res)
	cursor.close()
	return render_template('update_racquet.html',**context)


@app.route('/Update_string', methods=['GET', 'POST'])
def Update_string():
	if request.method == 'POST':
		string_code = request.form['string_code']
		color = request.form['color']
		gauge = request.form['gauge']
		length = request.form['length']
		core = request.form['core']
		outside = request.form['outside']
		coating = request.form['coating']
		unit_price = request.form['unit_price']
		query = """
		UPDATE string
		SET color = :color, gauge= :gauge, length= :length, core= :core, outside=:outside, coating=:coating, unit_price=:unit_price
		WHERE string_code = :string_code
		"""
		params = {
			'string_code': string_code,
        	'color': color,
        	'gauge': gauge,
        	'length': length,
        	'core': core,
			'outside': outside,
        	'coating': coating,
			'unit_price': unit_price
    		}
		g.conn.execute(text(query), params)
		g.conn.commit()
		select_query = "SELECT * from string"
		cursor = g.conn.execute(text(select_query))
		res = []
		for result in cursor:
			res.append(result)
		context = dict(data = res)
		cursor.close()
		return render_template('update_string.html', **context)
	else:
		return render_template('update_string.html')
	

@app.route('/Update_order', methods=['GET', 'POST'])
def Update_order():
	if request.method == 'POST':
		Order_id = request.form['Order_id']
		Order_date = request.form['Order_date']
		Cust_id = request.form['Cust_id']
		Employee_id = request.form['Employee_id']
		query = """
		UPDATE orders
		SET Order_date = :Order_date, Cust_id= :Cust_id, Employee_id= :Employee_id
		WHERE Order_id = :Order_id
		"""
		params = {
			'Order_id': Order_id,
        	'Order_date': Order_date,
        	'Cust_id': Cust_id,
        	'Employee_id': Employee_id,
    		}
		g.conn.execute(text(query), params)
		g.conn.commit()
		select_query = "SELECT * from orders"
		cursor = g.conn.execute(text(select_query))
		res = []
		for result in cursor:
			res.append(result)
		context = dict(data = res)
		cursor.close()
		return render_template('update_order.html', **context)
	else:
		return render_template('update_order.html', **context)
	

@app.route('/Add_racquet', methods=['POST'])
def Add_racquet():
	racquet_code = request.form['racquet_code']
	name = request.form['name']
	flex = request.form['flex']
	color = request.form['color']
	unit_price = request.form['unit_price']
	query = """
	INSERT INTO racquet(racquet_code, name, flex, color, unit_price)
	VALUES (:racquet_code, :name, :flex, :color, :unit_price)
	"""
	params = {
			'racquet_code': racquet_code,
        	'name': name,
        	'flex': flex,
        	'color': color,
        	'unit_price': unit_price
    		}
	cursor = g.conn.execute(text(query), params)
	g.conn.commit()
	select_query = "SELECT * from racquet"
	cursor = g.conn.execute(text(select_query))
	res = []
	for result in cursor:
		res.append(result)
	context = dict(data = res)
	cursor.close()
	return render_template('add_racquet.html',**context)


@app.route('/Add_string', methods=['GET', 'POST'])
def Add_string():
	if request.method == 'POST':
		string_code = request.form['string_code']
		color = request.form['color']
		gauge = request.form['gauge']
		length = request.form['length']
		core = request.form['core']
		outside = request.form['outside']
		coating = request.form['coating']
		unit_price = request.form['unit_price']
		query = """
		INSERT INTO string(string_code, color, gauge, length, core, outside, coating, unit_price)
		VALUES (:string_code, :color, :gauge, :length, :core, :outside, :coating, :unit_price)
		"""
		params = {
			'string_code': string_code,
        	'color': color,
        	'gauge': gauge,
        	'length': length,
        	'core': core,
			'outside': outside,
        	'coating': coating,
			'unit_price': unit_price
    		}
		g.conn.execute(text(query), params)
		g.conn.commit()
		return render_template('add_string.html')
	else:
		return render_template('add_string.html')
	
	
@app.route('/Add_order', methods=['GET', 'POST'])
def Add_order():
	if request.method == 'POST':
		Order_id = request.form['Order_id']
		Order_date = request.form['Order_date']
		Cust_id = request.form['Cust_id']
		Employee_id = request.form['Employee_id']
		query = """
		INSERT INTO orders(Order_id, Order_date, Cust_id, Employee_id)
		VALUES (:Order_id, :Order_date, :Cust_id, :Employee_id)
		"""
		params = {
			'Order_id': Order_id,
        	'Order_date': Order_date,
        	'Cust_id': Cust_id,
        	'Employee_id': Employee_id,
    		}
		g.conn.execute(text(query), params)
		g.conn.commit()
		return render_template('add_order.html')
	else:
		return render_template('add_order.html')
	

######waiting for html check action name and file names
# @app.route('/bestsell_sting', methods=['POST'])
# def bestsell_sting():
# 	cursor = g.conn.execute("")
# 	g.conn.begin().commit()
# 	record = cursor.fetchone()
# 	context = dict(data = record)
# 	print(record)
# 	cursor.close()
# 	return render_template('user.html', **context)

# @app.route('/bestsell_racquet', methods=['POST'])
# def bestsell_racquet():
# 	cursor = g.conn.execute("")
# 	g.conn.begin().commit()
# 	record = cursor.fetchone()
# 	context = dict(data = record)
# 	print(record)
# 	cursor.close()
# 	return render_template('user.html', **context)

# @app.route('/add_string_advice', methods=['POST'])
# def add_string_advice():
# 	racquet_code = request.form['racquet_code']
# 	string_code = request.form['string_code']
# 	g.conn.execute("INSERT INTO string_advice (racquet_code, string_code) VALUES (%s, %s)",(racquet_code, string_code))
# 	g.conn.commit()
# 	return render_template('employee.html')



@app.route('/login')
def login():
	abort(401)
	this_is_never_executed()


if __name__ == "__main__":
	import click

	@click.command()
	@click.option('--debug', is_flag=True)
	@click.option('--threaded', is_flag=True)
	@click.argument('HOST', default='0.0.0.0')
	@click.argument('PORT', default=8111, type=int)
	def run(debug, threaded, host, port):
		"""
		This function handles command line parameters.
		Run the server using:

			python server.py

		Show the help text using:

			python server.py --help

		"""

		HOST, PORT = host, port
		print("running on %s:%d" % (HOST, PORT))
		app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

run()
