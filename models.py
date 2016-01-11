# -*- coding: UTF-8 -*-
# coding:utf-8
import datetime
from copylighter import db, app
from slugify import slugify
from flask.ext.login import UserMixin
from flask.ext.security import UserMixin
from flask.ext.login import current_user
from flask.ext.mongoengine import mongoengine

class Note(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now)
    URLLink = db.URLField(required=False)
    slug = db.StringField()
    content = db.StringField(required=True)
    tags = db.ListField(db.StringField())
    isSecret = db.BooleanField(default=False)
    isArchived = db.BooleanField(default=False)
    
    meta = {'indexes': [
        {'fields': ["$content","$tags"],
         'ordering': ['-created_at'],
         'default_language': 'english',
         'ordering': ['-created_at'],
         'allow_inheritance': True,
         'weights': {'content': 10, 'tags':5}
        }
    ]}
    
    def __unicode__(self):
        return self.content


    def save(self, *args, **kwargs):        
        #if not self.slug:
            #self.slug = slugify(self.title)
        #if not self.user:
            #self.user = current_user.id        
        return super(Note, self).save(*args, **kwargs)

class User(db.Document, UserMixin):    
    created_at = db.DateTimeField(default=datetime.datetime.now)
    name = db.StringField(max_length=30, required=True, unique=True, help_text="Username or Name-Lastname")
    email = db.StringField(max_length=100, required=True, help_text="Email")
    password = db.StringField(max_length=255, required=True, help_text="Password")
    slug = db.StringField(help_text="Slug")
    roles = db.ListField(db.StringField())
    notes = db.ListField(db.EmbeddedDocumentField('Note'))

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
        return unicode(str(self.id))

    def __repr__(self):
        return '<User %r>' % (self.name)

class NoteRef(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now)
    note_id = db.ReferenceField('Note', reverse_delete_rule=mongoengine.CASCADE)
    user_id = db.ReferenceField('User', reverse_delete_rule=mongoengine.PULL)

    def __str__(self):
        return self.note_id

class TagRef(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now)
    tags = db.StringField(max_length=30)
    note_id = db.ListField(db.ReferenceField('Note', reverse_delete_rule=mongoengine.CASCADE))

    def __unicode__(self):
        return self.tags