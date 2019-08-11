from flask import Flask,jsonify,request
from flask_cors import CORS
import pymysql
import uuid

DEBUG = True

app = Flask(__name__)


# db = pymysql.connect('localhost','root','12345','books')
# cursor = db.cursor()
#
# cursor.execute('select * from books')
# data = cursor.fetchall()
# print(list(data))
# print(type(data))



app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title' : 'On the Road',
        'author' : 'Jack Kerouac',
        'read' : True
    },
{
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/books',methods=['GET','POST'])
def all_books():
    response_object = {'status':'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)

@app.route('/books/<book_id>', methods=['PUT','DELETE'])
def single_book(book_id):
    response_object = {'status':'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id':uuid.uuid4().hex,
            'title':post_data.get('title'),
            'author':post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book Delete!'
    return jsonify(response_object)

def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False



if __name__ == '__main__':
    app.run()