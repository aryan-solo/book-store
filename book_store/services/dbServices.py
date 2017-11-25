# add all db operations here
from pymongo import MongoClient
from datetime import datetime
from gridfs import GridFS
import json
import gridfs

pdfPath = '/home/aryan/private_proj/book_store/controller/data_temp/temp/'



def addBook(pdf_file, dbClient, name,price,author,tags):
	updObj = dict()
	# name = str(randint(10, 999))
	pdfFullPath = pdfPath+name+'.pdf'
	print("===================================================")
	pdf_file.save(pdfFullPath) #saving pdf to path
	newstore="book"
	try:
		iid=uploadFileToMongo(pdf_file,dbClient,name,price,author,tags)
	except Exception as e:
		print str(e)
		return e
	
	return str(iid)


def uploadFileToMongo(docPath,dbClient,name,price,author,tags):

	pdfFullPath = pdfPath+name+'.pdf'

	b=pdfFullPath
	collection="book_store"
	mimeType = 'application/pdf'
	fs = GridFS(dbClient,"bookstore")
	with open(pdfFullPath) as f:
		index = fs.put(f, content_type='application/pdf', filename=name)
	# ob = fs.put(docPath)

	now=datetime.now()
	year=now.year
	month=now.month
	day=now.day
	date=str(day)+str(month)+str(year)
	# files = {'file': ('doc' + docPath[-4:], open(docPath, 'rb'), mimeType, {'Expires': '0'})}
	mo_obj = {
			"file":index,
			"name":name,
			"price":price,
			"author":author,
			"tags":tags,
			"createdOn": datetime.now()
		}
	print mo_obj
	result = dbClient[collection].insert_one(mo_obj)
	print(result)

	return result.inserted_id


def delete(name,mongoClient):
	collection='book-store' 
	dbc=mongoClient.book_store
	fs = GridFS(mongoClient,"bookstore")
	dbf=mongoClient.bookstore
	collec=dbf.files
	collecChunk=dbf.chunks
	try:
		dbc.delete_many({"name":name})
		result=collec.find_one({'filename':name})
		file_id=result["_id"]
		if file_id==None:
			return "File does not exists"
		print(file_id)
		resultChunk=collecChunk.find({'files_id':file_id})
		for doc in resultChunk:
			
			collecChunk.remove(doc)
		
		collec.remove(result)
		
		print type(result)
		

		
		print '\nDeletion successful\n' 
		return "Deleted"
	except Exception, e:
		print str(e)
		return e



def updateDocument(mongoClient,updateDict):
	dbClient=mongoClient.book_store
	result=dbClient.find_one({'name':updateDict['name']})
	file_id=result["_id"]

	checkList=['name','price','author','tags','createdOn']
	for i in range(0,len(checkList)):
		key=checkList[i]
		if key in updateDict.keys():
			dbClient.update({key:result['key']},{'$set':{'key':updateDict[key]}},multi=True)
		else:
			continue

		return str("Updated document",file_id)































