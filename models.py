# -*- coding: UTF-8 -*-
# coding:utf-8
import datetime
from copylighter import db, app
from slugify import slugify
from flask.ext.login import UserMixin
from flask.ext.security import UserMixin
from flask.ext.login import current_user

class Note(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now)
    URLLink = db.URLField()
    title = db.StringField(max_length=255)
    slug = db.StringField()
    content = db.StringField(required=True)
    tags = db.ListField(db.StringField())

    isArchived = db.BooleanField(default=False)
    isSecret = db.BooleanField(default=False)

    #meta = {
      #  'ordering': ['-created_at'],
     #   'allow_inheritance': True
    #}
    """
    meta = {'indexes': [
        {'fields': ["$tags"],
         'ordering': ['-created_at'],
         'default_language': 'english',
         'ordering': ['-created_at'],
         'allow_inheritance': True,
         'weights': {'tags': 10}
        }
    ]}
    """
    def __unicode__(self):
        return '%s %s' % (self.title, self.content)

    def save(self, *args, **kwargs):        
        if not self.slug:
            self.slug = slugify(self.title)
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
    note_id = db.ReferenceField('Note')
    user_id = db.ReferenceField('User')

class TagRef(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now)
    tags = db.StringField(max_length=30)
    note_id = db.ListField(db.ReferenceField('Note'))
