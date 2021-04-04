import pymongo
from pymongo import MongoClient
import config

client = MongoClient('localhost', 27017)

db = client['meet_and_greet_db']

def check_and_add_user(message):
    if db.users.find_one({'user_id': message.from_user.id}) is None:
        new_user = {
            'user_id': message.from_user.id,
            'name': message.from_user.first_name,
            'age': message.from_user.last_name,
            'sex': message.from_user.id,
            'city': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'photo': message.from_user.id
            'state': 'старт'
        }
        db.users.insert_one(new_user)
    return

def get_current_state(user_id):
    user = db.users.find_one({'user_id':user_id})
    return user['state']

def set_state(user_id, state_value):
    db.users.update_one({'user_id': user_id}, {"$set": {'state': state_value}})