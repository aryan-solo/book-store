import sys
import os
sys.path.insert(0, '/home/aryan/private_proj/book_store/services')
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from pymongo import MongoClient
from datetime import datetime
from cStringIO import StringIO
import bookStoreServices as bs
import dbServices as db
from io import BytesIO
from bson import json_util
from bson.json_util import dumps
from bson import objectid
import json
import gridfs
import collections
import bson
from bson.codec_options import CodecOptions
from bson import objectid
from gridfs import GridFS


app = Flask(__name__)
# app.config['MONGO_DBNAME'] = 'bookstore'
# app.config['MONGO_URI'] = 'mongodb://aryan:aryan@ds259865.mlab.com:59865/bookstore'
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/bookstore'
# mongo = PyMongo(app)
pdfPath = '/home/aryan/private_proj/book_store/controller/data_temp/temp/'
def getMongoConnection():
	print("=====================================")
	print("CONNECTED MONGO TO SERVER")
	print("=====================================")
	flag = True
	mongodbUrl = 'mongodb://aryan:aryan@ds259865.mlab.com:59865/bookstore'
	maxSevSelDelay = 1
	client = MongoClient(mongodbUrl,serverSelectionTimeoutMS=maxSevSelDelay)
	while flag:
			try:
					flag = False
			except Exception as e:
					print("error connecting to mongo:",str(e),"\n Retrying...")
	dbclient = client["bookstore"]
	return dbclient

@app.route('/books', methods=['GET'])
def get_all_books():
	collection='book-store' 
	dbclient=mongoClient.book_store

	output = []

	for q in dbclient.find():
		# print q
		output.append({'name' : q['name'], 'price' : int(q['price']), 'author' : q['author'], 'createdOn' : q['createdOn'], 'tags': q['tags']})

	vall=output
	print vall,"look at this"
	return jsonify({'result' : output})

@app.route('/book-tags/<tags>', methods=['GET'])
def get_books_by_tags(tags):
	dbclient=mongoClient.book_store
	output = []
	vall=[]
	print tags	
	for q in dbclient.find():
		output.append({'name' : q['name'], 'price' : int(q['price']), 'author' : q['author'], 'createdOn' : q['createdOn'], 'tags': q['tags']})
	vall=bs.getBookByTag(output,tags)
	return jsonify({'result' : vall})


@app.route('/book-upload', methods = ['POST'])
def bookUpload():
	# books = mongo.db.books	
	if 'name' not in request.form or 'price' not in request.form or 'file' not in request.files:
			finalj = {"error":"parameter missing please check"}
	else:
		fileName = request.files['file']
		name = request.form['name']
		price = int(request.form['price'])
		author = request.form['author']
		tags = request.form['tags']
		# finalj = addBook(fileName,books,name,price,author,tags)
		print fileName
		finalj = db.addBook(fileName, mongoClient,name,price,author,tags)
		# finalj = addBook(fileName, mongoClient,name,price,author,tags)

	return json.dumps(finalj)


@app.route('/books/<name>', methods=['GET'])
def get_one_book(name):
	# books = mongo.db.books
	collection='book-store' 
	content_type='application/pdf'
	dbclient=mongoClient.book_store
	data=[]
	q = dbclient.find_one({'name' : name})

	if q:
		output = {'name' : q['name'], 'price' : q['price'], 'author' : q['author'], 'createdOn' : q['createdOn'], 'tags': q['tags']}
	else:
		output = 'No results found'
	if len(output)>1:
		dbf=mongoClient.bookstore
		collec=dbf.files
		collecChunk=dbf.chunks
		result=collec.find_one({'filename':name})
		print(result)
		file_id=result["_id"]
		resultChunk=collecChunk.find({'files_id':file_id})
		# for doc in resultChunk:
		# 	t=doc['data']
		# 	print(type(t))
		# 	data.append(doc['data'])

		for doc in resultChunk:
			t=doc['data']
			print(type(t))
			data.append(BytesIO(doc['data']))
	output['book']=str(data)
	# output['book']=str(data)
	return json.dumps(output,default=json_util.default)
	# return jsonify({'result' : output})

@app.route('/remove-book/<name>', methods=['GET'])	
def deleteBook(name):

	try:
		deleteResponse=db.delete(name,mongoClient)
		return json.dumps(deleteResponse)
	except Exception as e:
		print str(e)
		return e


@app.route('/filter/<choice>/<order>', methods=['GET'])
def filter(choice,order):
	dbclient=mongoClient.book_store
	output = []
	for q in dbclient.find():
		# print q
		output.append({'name' : q['name'], 'price' : int(q['price']), 'author' : q['author'], 'createdOn' : q['createdOn'], 'tags': q['tags']})
	
	if order==str(1):
		flag=True
	else:
		flag=False
	collection='book-store' 
	try:
		result=bs.filterBookSearch(output,choice,flag)
		# json.dumps(result)
		return jsonify({'result':result})
	except Exception as e:
		print str(e)
		return e

@app.route('/update', methods=['POST'])
def updateDoc():
	updateDict={}
	if 'name' not in request.form:
			finalj = {"error":"Name must be present: provide books name"}
	else:
		if 'name' in request.form:
			name = request.form['name']
			updateDict['name']=name
		if 'price' in request.form:
			price = int(request.form['price'])
			updateDict['price']=price
		if 'author' in request.form:
			author = request.form['author']
			updateDict['author']=author
		if 'price' in request.form:
			price = request.form['price']
			updateDict['price']=price
		if 'tags' in request.form:
			tags= request.form['tags']
			updateDict['tags']=tags
		try:
			respoOfUpdation=db.updateDocument(mongoClient,updateDict)
			return jsonify({'result':respoOfUpdation})
		except Exception as e:
			print str(e)
			return e








if __name__ == '__main__':
	mongoClient = getMongoConnection()

	# books = mongo.db.books
	app.run(debug=True)