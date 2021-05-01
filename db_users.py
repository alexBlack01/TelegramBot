from pymongo import MongoClient
from datetime import datetime
from config import MONGODB_LINK
from config import MONGO_DB
import user
import random

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


def save_music_info(user_id, music):
    db.users.update_one(
        {'user_id': user_id},
        {'$set': {'addition_info': {'music': music
                                    }
                  }
         }
    )
    return


def save_movie_info(user_id, movie):
    db.users.update_one(
        {'user_id': user_id},
        {'$set': {'addition_info': {'movie': movie
                                    }
                  }
         }
    )
    return


def save_sex_info(user_id, sex):
    db.users.update_one(
        {'user_id': user_id},
        {'$set': {'addition_info': {'sex': sex
                                    }
                  }
         }
    )
    return


def save_zodiac_info(user_id, zodiac):
    db.users.update_one(
        {'user_id': user_id},
        {'$set': {'addition_info': {'zodiac': zodiac
                                    }
                  }
         }
    )
    return


def save_age_range_info(user_id, age_range):
    db.users.update_one(
        {'user_id': user_id},
        {'$set': {'addition_info': {'age_range': age_range
                                    }
                  }
         }
    )
    return


def get_current_state(user_id):
    cur_user = db.users.find_one({'user_id': user_id})
    return cur_user['state']


def set_state(user_id, state_value):
    db.users.update_one({'user_id': user_id}, {'$set': {'state': state_value}})


def get_all_users():
    return list(db.users.find())


def get_user_by_criteria(criterion, list_criteria):
    return list(db.users.find({criterion: list_criteria}))


def add_user_to_whitelist(user_id, id_form):
    db.users.update_one(
        {'user_id': user_id},
        {'$set': {'whitelist': id_form
                  }
         }
    )
    return
