from copylighter.models import User, Note

queryset = Note.objects.all()

for tags in queryset:
	for obj in tags.tags:
		print obj.sum('referance')


notes_for_tags = current_user.notes

for note in notes:
     tagJ = ", "
     joinedtags = tagJ.join(note.tags)
     print joinedtags
     print joinedtags.count(str(note.tags))

