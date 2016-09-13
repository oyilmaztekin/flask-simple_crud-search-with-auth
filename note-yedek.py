#note = Note.objects.get(id=form.wtf.data)
			#note = current_user.notes.get(id=form.wtf.data)
			
			#current_user.notes.append(note)
			noteN = note(content=form.content2.data, tags=tagList, URLLink=form.URLLink2.data)			
			current_user.update(notes=noteN)
			#note.update(content=form.content2.data, tags=tagList, URLLink=form.URLLink2.data)
			current_user.save()

			#current_user.notes.append(note)
			#current_user.update(notes__tags=tagList, notes__content=form.content2.data)

			
			#note.save()
			
			

			#nottaki değişiklikleri usera ekleyemiyor.