# -*- coding: UTF-8 -*-
# coding:utf-8
import datetime
from copylighter import db, app
from slugify import slugify
from flask_login import UserMixin

class User(db.Document, UserMixin):    
    created_at = db.DateTimeField(default=datetime.datetime.now)
    name = db.StringField(max_length=30, required=True, unique=True, help_text="Your helptext here")
    email = db.StringField(max_length=100, required=True, unique=True, help_text="Your helptext here")
    password = db.StringField(max_length=255, required=True, help_text="Your helptext here")
    slug = db.StringField(help_text="Your helptext here")
    roles = db.ListField(db.StringField())

    def save(self, *args, **kwargs):
        defaultRole = ("active",)
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.roles:
            self.roles = defaultRole
        return super(User, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self._id)
 
    def __repr__(self):
        return '<User %r>' % (self.name)



class Note(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now)
    URLLink = db.URLField()
    title = db.StringField(max_length=255, required=True)
    slug = db.StringField()
    content = db.StringField(required=True)
    tags = db.ListField(db.StringField())
    user = db.ListField(db.ReferenceField('User'))

    isArchived = db.BooleanField(default=False)
    isSecret = db.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):        
        if not self.slug:
            self.slug = slugify(self.title)
        #if not self.user:
            #self.user = online.sessioned_user or whatever!!!        
        return super(Note, self).save(*args, **kwargs)


