import pymongo
from pymongo import MongoClient
from datetime import datetime
from config import MONGODB_LINK
from config import MONGO_DB
import config
import user

db = MongoClient(MONGODB_LINK)[MONGO_DB]

def check_and_add_user(message):
    user = db.users.find_one({'user_id': message.from_user.id.id})
    if user is None:
        new_user = {
            'user_id': message.from_user.id,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'state': 'старт'
        }
        db.users.insert_one(new_user)
    return

def save_user_form(cur_user: user.User()):
    db.users.update_one(
        {'user_id': cur_user.id},
        {'$set': {'form': {'name': cur_user.name,
                            'age': cur_user.age,
                            'sex': cur_user.sex,
                            'city': cur_user.city,
                            'photo': cur_user.photo,
                            'state': cur_user.state
                             }
                  }
         }
    )
    return user

def get_current_state(user_id):
    cur_user = db.users.find_one({'user_id': user_id})
    return cur_user['state']

def set_state(user_id, state_value):
    db.users.update_one({'user_id': user_id}, {"$set": {'state': state_value}})