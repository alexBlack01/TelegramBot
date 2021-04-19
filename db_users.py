from pymongo import MongoClient
from datetime import datetime
from config import MONGODB_LINK
from config import MONGO_DB
import user

db = MongoClient(MONGODB_LINK)[MONGO_DB]


def check_user(user_id):
    cur_user = db.users.find_one({'user_id': user_id})
    if cur_user is None:
        return False
    else:
        return True


def check_and_add_user(message):
    cur_user = db.users.find_one({'user_id': message.from_user.id})
    if cur_user is None:
        new_user = {
            'user_id': message.from_user.id,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'state': 'Старт'
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
                           }
                  }
         }
    )
    return


def save_music_info(user_id, cur_user: user.UserExtra()):
    db.users.update_one(
        {'user_id': user_id},
        {'$set': {'addition_info': {'music': cur_user.music
                                    }
                  }
         }
    )
    return


def save_movie_info(user_id, cur_user: user.UserExtra()):
    db.users.update_one(
        {'user_id': user_id},
        {'$set': {'addition_info': {'movie': cur_user.movie
                                    }
                  }
         }
    )
    return


def save_sex_info(user_id, cur_user: user.UserExtra()):
    db.users.update_one(
        {'user_id': user_id},
        {'$set': {'addition_info': {'sex': cur_user.sex
                                    }
                  }
         }
    )
    return


def save_zodiac_info(user_id, cur_user: user.UserExtra()):
    db.users.update_one(
        {'user_id': user_id},
        {'$set': {'addition_info': {'zodiac': cur_user.zodiac
                                    }
                  }
         }
    )
    return


def save_age_range_info(user_id, cur_user: user.UserExtra()):
    db.users.update_one(
        {'user_id': user_id},
        {'$set': {'addition_info': {'age_range': cur_user.age_range
                                    }
                  }
         }
    )
    return


def get_current_state(user_id):
    cur_user = db.users.find_one({'user_id': user_id})
    return cur_user['state']


def set_state(user_id, state_value):
    db.users.update_one({'user_id': user_id}, {"$set": {'state': state_value}})
