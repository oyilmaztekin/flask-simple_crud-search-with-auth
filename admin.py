from flask import Flask
from flask.ext.superadmin import Admin, model, BaseView
from models import *


class MyView(BaseView):
    def is_accessible(self):
        return login.current_user.is_authenticated()


admin = Admin(app, name="Copylighter")


class UserModel(model.ModelAdmin):
	list_display = ('id','name','email')
	form_widget_args = {
        'name': {
            'readonly': True
        },
    }
	
class NoteModel(model.ModelAdmin):
	list_display = ('id', 'content','created_at',)
	column_searchable_list = ('content', 'id')
	fields = ('title','created_at','tags','content', 'isArchived', 'isSecret')

class NoteRefModel(model.ModelAdmin):
	list_display = ('id', 'note_id','user_id','created_at')

class TagRefModel(model.ModelAdmin):
	list_display = ('id', 'tags','note_id','created_at')

admin.register(User, UserModel)
admin.register(Note, NoteModel)
admin.register(TagRef, TagRefModel)
admin.register(NoteRef, NoteRefModel)
