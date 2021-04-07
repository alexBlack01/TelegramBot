import pymongo
from pymongo import MongoClient
import config
import user

client = MongoClient('localhost', 27017)

db = client['meet_and_greet_db']

def check_and_add_user(cur_user: user.User()):
    if db.users.find_one({'user_id': user.id}) is None:
        new_user = {
            'user_id': cur_user.id,
            'name': cur_user.name,
            'age': cur_user.age,
            'sex': cur_user.sex,
            'city': cur_user.city,
            'photo': cur_user.photo,
            'state': cur_user.state
        }
        db.users.insert_one(new_user)
    return

def get_current_state(user_id):
    cur_user = db.users.find_one({'user_id':user_id})
    return cur_user['state']

def set_state(user_id, state_value):
    db.users.update_one({'user_id': user_id}, {"$set": {'state': state_value}})