class User:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.age = 0
        self.sex = ''
        self.city = ''
        self.photo = ''

    def set_id(self, id):
        self.id = id

    def set_name(self, name):
        self.name = name

    def set_age(self, age):
        self.age = age

    def set_sex(self, sex):
        self.sex = sex

    def set_city(self, city):
        self.city = city

    def set_photo(self, photo):
        self.photo = photo


class UserExtra:
    def __init__(self):
        self.id = ''
        self.music = []
        self.movie = []
        self.zodiac = []
        self.sex = ''
        self.age_range = []

    def set_id(self, id):
        self.id = id

    def set_music(self, music_val):
        self.music.append(music_val)

    def set_movie(self, movie_val):
        self.movie.append(movie_val)

    def set_zodiac(self, zodiac_val):
        self.zodiac.append(zodiac_val)

    def set_sex(self, sex):
        self.sex = sex

    def set_age_range(self, age_val):
        self.age_range.append(age_val)
