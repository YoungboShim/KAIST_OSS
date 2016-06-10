from flask import Flask
from flask import render_template
from flask import request
from flask import session
import MySQLdb
from arcus import *
from arcus_mc_node import ArcusMCNodeAllocator
from arcus_mc_node import EflagFilter
import datetime, time, sys
from timeit import default_timer as timer

import time

app = Flask(__name__)

@app.route('/test')
def test():
       return render_template('test.html')

@app.route('/test',methods=['POST'])
@app.route('/test/<name>',methods=['POST'])
def no_arcus():
	#when the Button pushed from web application.
	if request.method == 'POST':   
		query = "select * from data_long where K in (select cast(K as CHAR(20)) from data)"
		#Open DB connection
		db = MySQLdb.connect("localhost","root","12345678","arcus_test")

		# arcus set-up
		timeout = 20
		client = Arcus(ArcusLocator(ArcusMCNodeAllocator(ArcusTranscoder())))
		client.connect('127.0.0.1:2181', 'test')

		#prepare cursor object
		cursor = db.cursor()
		
		#no_arcus start	
		t0 = time.time()
		for count in range(1000):
			cursor.execute(query)
			data = cursor.fetchall()
			for line in data:
				pass
		no_arcus = time.time() - t0    #measure the time spent with no_arcus ver.
		
		#with_arcus start
		t0 = time.time()	
		for count in range(1000):
			if client.get("1").get_result()!=None:
				pass
			else:	
				cursor.execute(query)
				data = cursor.fetchall()	
				client.set("1", "WWW", timeout)
		with_arcus = time.time() - t0   #measure the time spent with with_arcus ver.
 
		#close DB and disconnect with arcus 
		client.disconnect()
		db.close()
		
		#return how much time spent with each ver.
		return render_template('test.html', name=[str(no_arcus), str(with_arcus)])


if __name__ == '__main__':
       	app.debug = True
       	app.run(host = '0.0.0.0', port = 5001)
