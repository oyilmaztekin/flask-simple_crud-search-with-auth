# -*- coding: UTF-8 -*-
# coding:utf-8
import datetime
from copylighter import db, app
from slugify import slugify
from flask.ext.login import UserMixin
from flask.ext.security import UserMixin
from flask.ext.login import current_user
from flask.ext.mongoengine import mongoengine
from passlib.hash import sha256_crypt
from flask.ext.login import current_user
import uuid

class Note(db.EmbeddedDocument):
    id = db.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    URLLink = db.StringField(required=False)
    content = db.StringField(required=True)
    tags = db.ListField(db.StringField(required=True, max_length=20))
    
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
        return '%s - %s - %s - %s - %s' % (self.id, self.tags, self.content, self.URLLink, self.URLLink)



    def save(self, *args, **kwargs):
        #if not self.slug:
            #self.slug = slugify(self.title)
        #if not self.user:
            #self.user = current_user.id
        return super(Note, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        #return '%s - %s' % (self.ad_soyad, self.basvuru_konusu)
        return super(Note, self).save(*args, **kwargs)
        

class User(db.Document, UserMixin):
    created_at = db.DateTimeField(default=datetime.datetime.now)
    name = db.StringField(max_length=30, required=True, unique=True, help_text="Username or Name-Lastname")
    email = db.StringField(max_length=100, required=True, unique=True, help_text="Email")
    password = db.StringField(max_length=255, required=True, help_text="Password")
    slug = db.StringField(help_text="Slug")
    roles = db.ListField(db.StringField())
    notes = db.EmbeddedDocumentListField('Note')

    

    def __unicode__(self):
        return '%s' % (self.name, self.password) or u''

    def save(self, *args, **kwargs):
        defaultRole = ("active",)
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.roles:
            self.roles = defaultRole
        return super(User, self).save(*args, **kwargs)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(str(self.id))

    def update(self, *args, **kwargs):
        #if not self.slug:
            #self.slug = slugify(self.title)
        #if not self.user:
            #self.user = current_user.id
        return super(User, self).update(*args, **kwargs)

    def __repr__(self):
        return '<User %r>' % (self.name)


