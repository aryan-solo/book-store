import datetime
from operator import itemgetter
pdfPath = '/home/aryan/private_proj/book_store/controller/data_temp/temp/'

# filterS=['price']
def filterBookSearch(output,filterS,flag):
	# dbclient=mongoClient.book_store
	# output = []

	if flag==True:
		newlist = sorted(output, key=itemgetter(filterS),reverse=True)
	else:
		newlist = sorted(output, key=itemgetter(filterS))
	# print newlist
	return newlist


# tag=['fiction','cognitive-ability']
def getBookByTag(bookList,tag):
	output=[]
	searchWord=""
	tagx=[]
	for i in range(0,len(tag)):
		ch=tag[i]
		if ch=='[' or ch=="'":
			continue
		elif ch==',' or ch==']':
			searchWord.replace(',','')
			searchWord.replace('[','')
			tagx.append(str(searchWord))
			searchWord=""
		else:
			searchWord=searchWord+ch
	
	for i in range(0,len(bookList)):
		tempDict=bookList[i]
		taglist=tempDict['tags']
		print taglist,tagx
		boolV=any((True for x in tagx if x in taglist))
		if boolV==True:
			output.append(tempDict)
	# print output
	return output

# if __name__=='__main__':
	# bookList=[{'createdOn': datetime.datetime(2017, 11, 25, 19, 32, 59, 840000), 'price': 1000, 'tags': u"['fiction','adventure','fantasy']", 'name': u'lord of the rings', 'author': u'j tolekins'}, {'createdOn': datetime.datetime(2017, 11, 25, 19, 39, 30, 147000), 'price': 1999, 'tags': u"['women-right','law','justice']", 'name': u'eve was framed ', 'author': u'helena kennedy'}, {'createdOn': datetime.datetime(2017, 11, 25, 20, 30, 38, 607000), 'price': 500, 'tags': u"['biases','economics','psychology']", 'name': u'thinking fast and slow', 'author': u'daniel kahneman'}, {'createdOn': datetime.datetime(2017, 11, 25, 20, 56, 58, 439000), 'price': 300, 'tags': u"['cognitive-ability','brain','memory']", 'name': u'moonwalking with einstein', 'author': u'joshua foer'}]
	# getBookByTag(bookList,tag)
	# print bookList,"before filter"
	# filterBookSearch(bookList,filterS)
	# allAvailableBooks(bookList,'price')