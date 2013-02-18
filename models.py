from google.appengine.ext import db

class MyUser(db.Model):
    login = db.StringProperty()
    password = db.StringProperty()
    name = db.StringProperty()
    surname = db.StringProperty()
    status = db.IntegerProperty(default = 1)
    age = db.IntegerProperty()
    birthday = db.StringProperty()
    info = db.TextProperty()
    location = db.GeoPtProperty()
    created_at = db.DateTimeProperty(auto_now_add = True)
    vk_id = db.StringProperty()
    fb_id = db.StringProperty()
    phone = db.PhoneNumberProperty()
    email = db.EmailProperty()
    plan = db.StringListProperty(default=[])
    image = db.StringProperty()
    _id = db.IntegerProperty()
    bookmarks = db.StringListProperty(default=[])

class MyEvent(db.Model):
    login = db.StringProperty()
    start = db.DateTimeProperty()
    end = db.DateTimeProperty()
    status = db.IntegerProperty(default = 1)
    info = db.TextProperty()
    location = db.GeoPtProperty()
    _id = db.IntegerProperty()
    name = db.StringProperty()


