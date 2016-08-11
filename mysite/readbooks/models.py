from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User

def user_upload_dir(instance, filename):
	return 'profile_pics/users/user_{0}/{1}'.format(instance.id, filename)
def author_upload_directory(instance, filename):
	return 'profile_pics/authors/author_{0}/{1}'.format(instance.id, filename)
def critic_upload_directory(instance, filename):
	return 'profile_pics/critics/critic_{0}/{1}'.format(instance.id, filename)
def reader_upload_directory(instance, filename):
	return 'profile_pics/readers/reader_{0}/{1}'.format(instance.id, filename)
def book_upload_directory(instance, filename):
	return 'cover_pics/books/book_{0}/{1}'.format(instance.id, filename)
def group_upload_directory(instance, filename):
	return 'cover_pics/groups/group_{0}/{1}'.format(instance.id, filename)
def publisher_upload_directory(instance, filename):
	return 'cover_pics/publishers/publisher_{0}/{1}'.format(instance.id, filename)

class Author(models.Model):
	first_name	=	models.CharField(max_length=256)
	last_name	=	models.CharField(max_length=256)
	bio	=	models.CharField(max_length=256)
	gender_choices	= 	(('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))
	gender = models.CharField(max_length=6, choices=gender_choices)
	date_of_birth	=	models.DateField(default=date.today)
	profile_picture	=	models.ImageField(upload_to=author_upload_directory, blank=True)
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)
	class Meta:
		ordering= ['last_name']
	def __str__(self):
		return '%s %s' %(self.first_name, self.last_name)
	@classmethod
	def create(cls, first_name):
		author = cls(first_name=first_name)
		return author

class Critic(models.Model):
	user = models.ForeignKey(User)
	user_type = models.CharField(max_length=6, default="Critic")
	first_name	=	models.CharField(max_length=256)
	last_name	=	models.CharField(max_length=256)
	bio	=	models.CharField(max_length=256)
	gender_choices	= 	(('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))
	gender = models.CharField(max_length=6, choices=gender_choices)
	date_of_birth	=	models.DateField(default=date.today)
	profile_picture	=	models.ImageField(upload_to=critic_upload_directory, blank=True)
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)
	class Meta:
		ordering=	['last_name']
	def __str__(self):
		return '%s %s' %(self.first_name, self.last_name)

class Publisher(models.Model):
	name	=	models.CharField(max_length=256)
	address	=	models.CharField(max_length=256)
	website	=	models.URLField()
	cover_picture	=	models.ImageField(upload_to=publisher_upload_directory, blank=True)
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)
	class Meta:
		ordering=	['name']
	def __str__(self):
		return self.name
	@classmethod
	def create(cls, name):
		publisher = cls(name=name)
		return publisher

class Genre(models.Model):
	name  =	models.CharField(max_length=256)
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)
	class Meta:
		ordering= ['name']
	def __str__(self):
		return self.name
	@classmethod
	def create(cls, name):
		genre = cls(name=name)
		return genre

class Book(models.Model):
	title	=	models.CharField(max_length=256)
	publication_date =	models.DateField(default=date.today)
	author	=	models.ForeignKey(Author)
	publisher	=	models.ForeignKey(Publisher)
	genre	=	models.ManyToManyField(Genre)
	reviews	=	models.ManyToManyField(Critic, through='Review')
	book_synopsis = models.CharField(max_length=256)
	cover_picture	=	models.ImageField(upload_to=book_upload_directory)
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)
	class Meta:
		ordering=['title']
	def __str__(self):
		return self.title
	@classmethod
	def create(cls, title):
		book = cls(title=title)
		return book

class Group(models.Model):
	name	=	models.CharField(max_length=256)
	member_count	=	models.IntegerField(default=0)
	group_description	=	models.CharField(max_length=256)
	topic_count	=	models.IntegerField(default=0)
	cover_picture	=	models.ImageField(upload_to=group_upload_directory, blank=True)
	class Meta:
		ordering = ['name']
	def __str__(self):
		return self.name
	@classmethod
	def create(cls, name):
		group = cls(name=name)
		return group

class Review(models.Model):
	critic	=	models.ForeignKey(Critic, on_delete=models.CASCADE)
	book	=	models.ForeignKey(Book, on_delete=models.CASCADE)
	heading	=	models.CharField(max_length=100)
	review	=	models.CharField(max_length=3000)
	pub_choices	= (('Draft', 'Draft'), ('Published', 'Published') )
	status	= 	models.CharField(max_length=9, choices=pub_choices)
	pubdate	=	models.DateField(default=date.today, blank=True)
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)
	class Meta:
		ordering=	['pubdate']
	def __str__(self):
		return self.heading
	@classmethod
	def create(cls, heading):
		review = cls(heading=heading)
		return review

class Reader(models.Model):
	user = models.ForeignKey(User)
	user_type= models.CharField(max_length=6, default="Reader")
	first_name	=	models.CharField(max_length=256)
	last_name	=	models.CharField(max_length=256)
	gender_choices	= 	(('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))
	gender = models.CharField(max_length=6, choices=gender_choices)
	date_of_birth	=	models.DateField(default=date.today)
	group_joined	=	models.ManyToManyField(Group, through='Membership')
	profile_picture	=	models.ImageField(upload_to=reader_upload_directory, blank=True)
	class Meta:
		ordering=	['last_name']
	def __str__(self):
		return '%s %s' %(self.first_name, self.last_name)

class Topic(models.Model):
	name	=	models.CharField(max_length=256)
	topic_discussion	=	models.CharField(max_length=2000)
	creation_date	= 	models.DateField(default=date.today)
	group	=	models.ForeignKey(Group, on_delete=models.CASCADE)
	creator	=	models.ForeignKey(Reader, on_delete=models.CASCADE)
	reply_count	= 	models.IntegerField(default=0)
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)
	class Meta:
		ordering= ['creation_date']
	def __str__(self):
		return self.name

class TopicReply(models.Model):
	topic	=	models.ForeignKey(Topic, on_delete=models.CASCADE)
	topic_reply	=	models.CharField(max_length=2000)
	message_time	= 	models.DateTimeField(auto_now=True)
	topic_reply_user	=	models.ForeignKey(Reader, on_delete=models.CASCADE)
	message_time	=	models.DateTimeField(auto_now=True)
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)
	class Meta:
		ordering = ['message_time']
	def __str__(self):
		return self.topic_reply

class Comment(models.Model):
	reader	=	models.ForeignKey(Reader, on_delete=models.CASCADE)
	book	=	models.ForeignKey(Book, on_delete=models.CASCADE)
	reader_comment	=	models.CharField(max_length=2000)
	message_time	=	models.DateTimeField(auto_now=True)
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)
	class Meta:
		ordering=	['message_time']
	def __str__(self):
		return '%s - %s' %(self.reader, self.reader_comment)

class ReadersCurrentlyRead(models.Model):
	book	=	models.ForeignKey(Book, on_delete=models.CASCADE)
	reader	=	models.ForeignKey(Reader, on_delete=models.CASCADE)
	
class Membership(models.Model):
	groups	=	models.ForeignKey(Group)
	members	=	models.ForeignKey(Reader)
	join_date	=	models.DateField(default=date.today)
	status	=	(('Moderator', 'Moderator'), ('Admin', 'Admin'), ('Member', 'Member'))
	member_status	=	models.CharField(max_length=9, choices=status)
