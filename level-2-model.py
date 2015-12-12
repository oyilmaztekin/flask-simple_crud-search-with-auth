import datetime
#from flask import url_for
from copylighter import db, app
from flask.ext.security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin, login_required

class Liked(db.EmbeddedDocument):
    owner = db.ListField(db.ReferenceField('User'))
    location = db.PointField() #level 2
    at = db.DateTimeField(default=datetime.datetime.now, required=True)

class Copylighted(db.EmbeddedDocument):    
    owner = db.ListField(db.ReferenceField('User'))
    location = db.PointField() #level 2
    at = db.DateTimeField(default=datetime.datetime.now, required=True)

class Comment(db.EmbeddedDocument):
    commented_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(verbose_name="Comment", required=True)
    author = db.ListField(db.ReferenceField('User'))      
    
    def save(self, *args, **kwargs):
        return super(Comment, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.author

    def __str__(self):
        return self.author

    
class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

class User(db.Document, UserMixin):    
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    name = db.StringField(max_length=30, required=True)
    email = db.StringField(max_length=100, required=True)
    password = db.StringField(max_length=255, required=True)
    active = db.BooleanField(default=True)        
    mobile = db.IntField(max_length=50)
    gender = db.StringField(max_length=20)
    date_of_birth = db.DateTimeField()
    img = db.StringField()
    slug = db.StringField()
    
    _roles = db.ListField(db.ReferenceField('Role'), default=['active',])
    _notes = db.ListField(db.ReferenceField('Note'))
    _liked = db.ListField(db.ReferenceField('Liked'))
    _copylighted = db.ListField(db.ReferenceField('Copylighted')) 
    _comments = db.ListField(db.ReferenceField('Commment'))

    def save(self, *args, **kwargs):
        rolename = "active"
        if not self.roles:
            self.roles = rolename        
        return super(User, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Note(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    URLLink = db.URLField()
    title = db.StringField(max_length=255, required=True)
    slug = db.StringField()
    desc = db.StringField(max_length=160)
    img = db.URLField()
    content = db.StringField(required=True)
    tags = db.ListField(db.StringField())
    
    _owner = db.StringField(db.ReferenceField('User'))
    _isLiked = db.ListField(db.ReferenceField('Liked'))
    _isCopylighted = db.ListField(db.ReferenceField('Copylighted'))
    _comments = db.ListField(db.ReferenceField('Comment'))
    
    likeCount = db.IntField()
    copyCount = db.IntField()
    commentCount = db.IntField()

    isArchived = db.BooleanField(default=False)
    isDeleted = db.BooleanField(default=False)
    isSecret = db.BooleanField(default=False)

    def __unicode__(self):
        return self.title

user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)
