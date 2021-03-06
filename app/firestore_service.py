import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential)

db = firestore.client()

def get_users():
    return db.collection('users').get()

def get_user(user_id):
    return db.collection('users').document(user_id).get()

def get_todos(user_id):
    return db.collection('users').document(user_id).collection('todos').get()

def put_user(user_data):
    user_ref = db.collection('users').document(user_data.username)
    user_ref.set({'password':user_data.password})

def put_todo(user_id, description):
    todo_ref = db.collection('users').document(user_id).collection('todos')
    todo_ref.add({'description': description, 'status':False})

def put_init_todo(defaul_todo):
    todo_ref = db.collection('users').document(defaul_todo.user_id).collection('todos')
    todo_ref.add({'description': defaul_todo.description,
                  'status':defaul_todo.status,})

def delete_todo(user_id, todo_id):
    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_ref.delete()

def update_todo(user_id, todo_id, status):
    todo_status = not bool(status)

    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_ref.update({'status':todo_status})

def _get_todo_ref(user_id, todo_id):
    return db.document('users/{}/todos/{}'.format(user_id, todo_id))