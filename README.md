# book-store


used python 2.7 along with mongodb [pymongo] , flask , Gridfs for document upload and read

there are 7 apis.
mongo client is a web hosted server by mlab.
1. book-upload :- [POST] , body{ 'name' : 'books name' , 'price':'price of book' ,'tags': 'type of book etc' ,'author':'', 
and 'file': 'actual pdf file'

2. all-books : [GET] give json of all available books and other details// 
3. one-book : [GET] returns one book along with actual pdf in binary object form{there is a commented section in the code to get the bson file} 

4.delete-book: [GET] deletes a book along with actual pdf which is stored in two parts : gridfs-file and grid-fs chunks

5. get books by tag : [GET] takes a list of tag and returns all books with those tags 
6. filter search : [GET] takes a criteria like price or date of creation // if choosing price and date of creation it is important to specify order : 0-> increasing order and 1-> decreasing order

7. upadate a document :[POST] name must be prresent in the request form // using name it gets the document id and update all the present field in the request body

images of the postman requests has also been provided.

will psuh some changes in a few hours.


// bookstore.api is the main appliaction script .
// the database used is live 24/7 so code can be cloned and can run from anywhere.
