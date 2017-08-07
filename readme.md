# Copylighter

### kurulum

virtual environment kurulum

```virtualenv env```

virtual environment aktif etme

```source env/bin/activate```

pip paketlerinin kurulumu

```pip install -r requirements.txt```


## DATABASE MODEL

### Quote - models.py
```python
	    class Note(db.Document):
		    created_at = db.DateTimeField(default=datetime.datetime.now)
		    URLLink = db.URLField(required=False)
		    slug = db.StringField()
		    content = db.StringField(required=True)
		    tags = db.ListField(db.StringField())
		    isArchived = db.BooleanField(default=False)
		    isSecret = db.BooleanField(default=False)

```
### Example Json




```json
        {
		    "_id" : ObjectId("567ad55982ab1c146e85c583"),
		    "created_at" : ISODate("2015-12-23T19:09:45.293Z"),
		    "slug" : "proje-odevi-ve-performans-gorevi-1-sinif-proje-odevi-1-sinif-performans-gorevi-2-sinif-proje-odevi-2-sinif-pe",
		    "content" : "PROJE ÖDEVİ VE PERFORMANS GÖREVİ. 1. SINIF PROJE ÖDEVİ · 1. SINIF PERFORMANS GÖREVİ · 2. SINIF PROJE ÖDEVİ · 2. SINIF PERFORMANS ...\r\n",
		    "tags" : [ 
		        "7.sınıf"
		    ],
		    "isArchived" : false,
		    "isSecret" : false
		}
```
   
   
Quoteların kim tarafından girildiğini takip edebilmek için. Hangi quote hangi usera ait? ForeignKey mongodb de olmadığı için ReferenceField olarak ilişkilendiriyoruz.



```python
		class NoteRef(db.Document):
			created_at = db.DateTimeField(default=datetime.datetime.now)
			note_id = db.ReferenceField('Note', reverse_delete_rule=mongoengine.CASCADE)
			user_id = db.ReferenceField('User', reverse_delete_rule=mongoengine.PULL)
```



Taglere ait notları listelemek ve taglerin takibini yapabilmek için... note_id kısmındaki ListField gereksiz. Ancak silersem sıkıntı çıkıyor. Böyle devam. İleride bir tage birden fazla not(quote) da ilişkilendirilebilir.

	
```python
		class TagRef(db.Document):
			created_at = db.DateTimeField(default=datetime.datetime.now)
			tags = db.StringField(max_length=30)
			note_id = db.ListField(db.ReferenceField('Note', reverse_delete_rule=mongoengine.CASCADE))
````

**reverse delete rule??**


```python
		note_id = db.ReferenceField('Note', reverse_delete_rule=mongoengine.CASCADE)
		user_id = db.ReferenceField('User', reverse_delete_rule=mongoengine.PULL)
```

reverse delete rule: kullanıcı not eklediğinde hem notref, hem de tagref collection lara(table) user_id, note_id ve tag bilgileri relation olarak ekleniyor. reverse_delete_rule kullanıcı girdiği notu silmek istediğinde noteRef ve Tagref table larında oluşturulan bağlantıları da siliyor.


### User Model

```python
   		class User(db.Document, UserMixin):    
		    created_at = db.DateTimeField(default=datetime.datetime.now)
		    name = db.StringField(max_length=30, required=True, unique=True, help_text="Username or Name-Lastname")
		    email = db.StringField(max_length=100, required=True, help_text="Email")
		    password = db.StringField(max_length=255, required=True, help_text="Password")
		    slug = db.StringField(help_text="Slug")
		    roles = db.ListField(db.StringField())
		    notes = db.ListField(db.EmbeddedDocumentField('Note'))
			
            #trigger
		    def save(self, *args, **kwargs):
		        defaultRole = ("active",)
		        if not self.slug:
		            self.slug = slugify(self.name)
		        if not self.roles:
		            self.roles = defaultRole
		        return super(User, self).save(*args, **kwargs)
````

**EmbeddedDocumentField???** 


```python 
		class User(db.Document, UserMixin):    
			notes = db.ListField(db.EmbeddedDocumentField('Note'))
```

NoSQl yapıda relationdan ziyade embedding var. Bu da embed edilmek istenen table(collection) ı mevcut collection ın içerisine basıyor.


**def save metodu ile eklenen register olan user collection ına yapılan işlemler**


```python
		def save(self, *args, **kwargs):
		    defaultRole = ("active",)
		        if not self.slug:
		            self.slug = slugify(self.name)
		        if not self.roles:
		            self.roles = defaultRole
		        return super(User, self).save(*args, **kwargs)
```

*slugify


```json
Bugün günlerden pazar
bugun-gunlerden-pazar
```


### Örnek user collection


```json
		{
		    "_id" : ObjectId("567ad33682ab1c0fb2e33138"),
		    "created_at" : ISODate("2015-12-23T19:00:38.304Z"),
		    "name" : "ozerozer",
		    "email" : "mail@mail.com",
		    "password" : "3caad39aa968284cf40ca9edd38b40a637582c782f08cc71fce8821c",
		    "slug" : "ozerozer",
		    "roles" : [ 
		        "active"
		    ],
		    "notes" : [ 
		        {
		            "_id" : ObjectId("567ad55982ab1c146e85c583"),
		            "created_at" : ISODate("2015-12-23T19:09:45.293Z"),
		            "slug" : "proje-odevi-ve-performans-gorevi",
		            "content" : "PROJE ÖDEVİ VE PERFORMANS GÖREVİ. 1. SINIF PROJE ÖDEVİ · 1. SINIF PERFORMANS GÖREVİ · 2. SINIF PROJE ÖDEVİ · 2. SINIF PERFORMANS ...\r\n",
		            "tags" : [ 
		                "7.sınıf"
		            ],
		            "isArchived" : false,
		            "isSecret" : false
		        }		       
		    ]
		}
```

## VIEWS - CONTROLLER
### Add Quote View views.py
	
	
```python	
		if form.validate_on_submit():				
			tags = form.tags.data
			tagList = tags.split(",")
				
			note = Note(content=form.content.data, tags=tagList)		
			note.save()
				
			current_user.notes.append(note)
			current_user.save() 
				
			noteRef = NoteRef(note_id=note.id, user_id=current_user.id)
			noteRef.save()
				
			for item in tagList:
				tagRef = TagRef(tags=item, note_id=[note.id,])
				tagRef.save()

		
			flash('Quote saved successfully.','success')
			return render_template('profile.html', form=form, search_form=SearchForm(), delete_quote=deleteQuoteForm())
```

Tagler, virgülden itibaren ayırarak ayrı ayrı insert edilir. Aşağıdaki işlemde quote note collection ına kaydedilir.
	

```python
		tags = form.tags.data
		tagList = tags.split(",")

		note = Note(content=form.content.data, tags=tagList)		
		note.save()
```
***Kaydedilen bu not usera embed edilir.***
	

```python
		current_user.notes.append(note)
		current_user.save() 
````

Kaydedilen not NoteRef collection ına referans id leri ile eklenir.*
	

```python
		noteRef = NoteRef(note_id=note.id, user_id=current_user.id)
		noteRef.save()
````

Kaydedilen notun içerisinden tagler for döngüsüyle List içerisinden ayrıştırılarak ayrı ayrı row olarak insert edilirler ve her tag rowuna aynı quote id si ile  ilişkilendirilir.
	

```python
		for item in tagList:
			tagRef = TagRef(tags=item, note_id=[note.id,])
			tagRef.save()
````

Tagler, virgülden itibaren ayırarak ayrı ayrı insert edilir.
	

```python
		current_user.notes.append(note)
		current_user.save() 
```

### Register - views.py
	

```python
		if formS.validate_on_submit():					
			hashash = formS.password.data
			salt = uuid.uuid4().hex
			hashed_password = hashlib.sha224(hashash + salt).hexdigest()

			form_email = formS.email.data

			if not Email_Regex.match(form_email):
				flash('Invalid email adress','danger')
				return render_template("register.html", form=formS, title="Copylighter", regex="Invalid email adress")

			newuser = User(name=formS.name.data, email=formS.email.data, password=hashed_password)				
			
			try:
				newuser.save()
				
			except NotUniqueError:
				flash('Username or email already exists','danger')
				return render_template("register.html", form=formS, title="Copylighter")

````

### Password ün hashlenmesi
	

```python
		hashash = formS.password.data
		salt = uuid.uuid4().hex
		hashed_password = hashlib.sha224(hashash + salt).hexdigest()

		........

		newuser = User(name=formS.name.data, email=formS.email.data, password=hashed_password)				

		try:
			newuser.save()
        except NotUniqueError:
	        ..............
```