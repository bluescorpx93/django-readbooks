from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import Q
from readbooks import models, forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from datetime import date

def user_upload_dir(instance, filename):
	return 'profile_pics/users/user_{0}/{1}'.format(instance.id, filename)

def calculate_age(dob):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def readerOrCritic(logged_id):
	try:
		models.Reader.objects.get(user_id=logged_id)
		return "Reader"
	except ObjectDoesNotExist:
		models.Critic.objects.get(user_id=logged_id)
		return "Critic"

@login_required
def readbooks_index(request):
	return render(request, 'index.html',{'user_type': readerOrCritic(request.user.id) })

@login_required
def search(request):
	if ('query' in request.GET and request.GET['query']):
		query_string	=	request.GET['query']
		if (not 'query'):
			error	=	True
		else:
			return render(request,'search.html',{ 
			'books':	models.Book.objects.filter(title__icontains=query_string),
			'authors': models.Author.objects.filter(Q(first_name__icontains=query_string) | Q(last_name__icontains=query_string)), 
			'critics':  models.Critic.objects.filter(Q(first_name__icontains=query_string)|  Q(last_name__icontains=query_string)), 
			'topics': models.Topic.objects.filter(Q(name__icontains=query_string)), 
			'genres': models.Genre.objects.filter(name__icontains=query_string), 
			'groups': models.Group.objects.filter(name__icontains=query_string), 
			'publishers': models.Publisher.objects.filter(name__icontains=query_string),
			'readers':models.Reader.objects.filter(Q(first_name__icontains=query_string)|  Q(last_name__icontains=query_string)),
			'reviews': models.Review.objects.filter(heading__icontains=query_string),
			'query_string': query_string,})
	return render(request, 'search.html')

@login_required
def list_recent_models(request, message=None):
	return render(request,	'list_recent_objects.html', { 
	'recent_books': models.Book.objects.all().order_by('-id')[:4],
	'recent_authors': models.Author.objects.all().order_by('-id')[:4], 
	'recent_reviews': models.Review.objects.all().order_by('-id')[:4], 
	'recent_groups': models.Group.objects.all().order_by('-id')[:4],
	'recent_topics': models.Topic.objects.all().order_by('-id')[:10],
	'success': message,})

@login_required
def show_book_by_id(request, book_id):
	try:
		book_obj = models.Book.objects.get(id=int(book_id))
		reviews_book_obj = models.Review.objects.filter(book=int(book_id)).order_by('-id')[:10]
		comments_by_book_obj = models.Comment.objects.filter(book=int(book_id)).order_by('-id')
	except ObjectDoesNotExist:
		return render(request, 'default404.html',)
	return render(request, 'book_profile.html', {'book_obj': book_obj,'reviews_book_obj': reviews_book_obj, 'comments_by_book_obj': comments_by_book_obj,'user_type': readerOrCritic(request.user.id), 'add_review_form': forms.AddReviewForm()})

@login_required
def show_author_by_id(request, author_id):
	try:
		author_obj = models.Author.objects.get(id=int(author_id))
		books_by_author_obj= models.Book.objects.filter(author=int(author_id)).order_by('-id')[:10]
	except ObjectDoesNotExist:
		return render(request, 'default404.html')
	return render(request, 'author_profile.html', { 'author_obj': author_obj,'books_by_author_obj': books_by_author_obj, })

@login_required
def show_publisher_by_id(request, publisher_id):
	try:
		publisher_obj = models.Publisher.objects.get(id=int(publisher_id))
		books_by_publisher_obj = models.Book.objects.filter(publisher=int(publisher_id)).order_by('-id')[:10]
	except ObjectDoesNotExist:
		return render(request, 'default404.html')
	return render(request, 'publisher_profile.html', { 'publisher_obj': publisher_obj, 'books_by_publisher_obj': books_by_publisher_obj,})

@login_required
def show_reader_by_id(request, reader_id):
	try:
		reader_obj =models.Reader.objects.get(id=int(reader_id))
		reader_obj_age = calculate_age(reader_obj.date_of_birth)
		currentbooks_by_reader_obj = models.ReadersCurrentlyRead.objects.filter(reader=int(reader_id))
	except ObjectDoesNotExist:
		return render(request, 'default404.html')
	return render(request, 'reader_profile.html', { 'reader_obj': reader_obj, 'reader_obj_age': reader_obj_age, 'currentbooks_by_reader_obj': currentbooks_by_reader_obj,})

@login_required
def show_critic_by_id(request, critic_id):
	try:
		critic_obj =  models.Critic.objects.get(id=int(critic_id))
		reviews_by_critic_obj = models.Review.objects.filter(critic=int(critic_id))
	except ObjectDoesNotExist:
		return render(request, 'default404.html')
	return render(request, 'critic_profile.html', {	'critic_obj': critic_obj, 'reviews_by_critic_obj': reviews_by_critic_obj,})

def isLoggedUserReviewWriter(request, review_id):
	logged_user = models.User.objects.get(id=request.user.id)
	review_obj= models.Review.objects.get(id=int(review_id))
	if review_obj.critic.user_id==logged_user.id:
		return True
		# print ("YES %s %s") %(review_obj.critic.user_id, logged_user.id)
	else:
		return False
		# print ("NO %s %s") %(review_obj.critic.user_id, logged_user.id)


@login_required
def show_review_by_id(request, review_id, message=None):
	try:
		review_obj= models.Review.objects.get(id=int(review_id))
		review_owner = isLoggedUserReviewWriter(request, review_id)
	except ObjectDoesNotExist:
		return render(request, 'default404.html')
	return render(request, 'book_review.html', {'review_obj': review_obj, 'review_owner': review_owner, 'success': message})

@login_required
def show_group_by_id(request, group_id):
	try:
		group_obj = models.Group.objects.get(id=int(group_id))
		topics_by_group_obj = models.Topic.objects.filter(group=int(group_id))
	except ObjectDoesNotExist:
		return render(request, 'default404.html')
	return render(request, 'group_page.html', {'group_obj': group_obj, 'topics_by_group_obj': topics_by_group_obj, 'user_type': readerOrCritic(request.user.id),})

@login_required
def show_topic_by_id(request, topic_id):
	try:
		topic_obj = models.Topic.objects.get(id=int(topic_id))
		replies_by_topic_obj= models.TopicReply.objects.filter(topic=int(topic_id))
	except ObjectDoesNotExist:
		return render(request, 'default404.html')
	return render(request, 'topic_page.html', {'topic_obj': topic_obj, 'replies_by_topic_obj': replies_by_topic_obj,})

def show_genre_by_id(request, genre_id):
	try:
		genre_obj = models.Genre.objects.get(id=int(genre_id))
		books_by_genre_obj = models.Book.objects.filter(genre=int(genre_id))
	except ObjectDoesNotExist:
		return render(request, 'default404.html')
	return render(request, 'genre_page.html', {'genre_obj': genre_obj, 'books_by_genre_obj': books_by_genre_obj,})

def sitelogin(request):
	if (request.method == 'POST'):
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect("/readbooks/home/")
			else:
				return render(request, 'login.html', {'problem': "User doesn't exist!",})
		else:
			return render(request, 'login.html', {'problem': "Invalid Login Details", })
	else:
		return render(request, 'login.html',)

@login_required
def sitelogout(request):
	logout(request)
	return render(request, 'login.html',)

@login_required
def messages(request):
	return render(request, 'messages.html')

@login_required
def update_userinfo_bf(request):
	user_type=readerOrCritic(request.user.id)
	if user_type == 'Reader':
		loggedProfile =models.Reader.objects.get(user_id=request.user.id)
	else:
		loggedProfile =  models.Critic.objects.get(user_id=request.user.id)
	context_dict = {'loggedProfile': loggedProfile, 'user_type':user_type,}
	if request.method=='POST':
		loggedProfile.first_name=request.POST['userfirstname']
		loggedProfile.last_name=request.POST['userlastname']
		loggedProfile.bio = request.POST['userbio']
		loggedProfile.gender = request.POST['usergender']
		loggedProfile.date_of_birth = request.POST['userdob']
		# image_location=user_upload_dir(loggeduserprofile, request.POST.get('userprofilepic'))
		loggedProfile.profile_picture = request.POST['userprofilepic']
		loggedProfile.save()
		context_dict = {'loggedProfile': loggedProfile, 'user_type':user_type,'success': "Profile Updated. Click on your name to check out your new profile"}
		return render(request, 'user_settings_bf.html', context_dict)
	else:
		return render(request, 'user_settings_bf.html', context_dict)

def register(request):
	if request.method == 'POST':
		email = request.POST['signup_email']
		password1 = request.POST['signup_password1']
		password2 = request.POST['signup_password2']
		gender = request.POST['gender']
		account_type = request.POST['account_type']
		if not password2:
			warning="You must confirm your password"
			return render(request, 'login.html', {'warning': warning,})
		if password1 != password2:
			problem = "Your passwords don't match"
			return render(request, 'login.html', {'problem': problem,})
		try:
			newuser = User.objects.create_user(username=email, email=email, password=password1)
		except IntegrityError:
			problem = "Email Address already taken"
			return render(request, 'login.html', {'problem': problem,})	
		newuser.save()
		if account_type== 'Critic':
			newCritic = Critic(user_id=newuser.id)
			newCritic.save()
		if account_type== 'Reader':
			newReader = Reader(user_id=newuser.id)
			newReader.save()
		newuserprofile = UserProfile(user_id=newuser.id, gender=gender)
		newuserprofile.save()
		return render(request, 'login.html', {'success': "Registration Successful! Login with your newly created account details.",})
	else:
		return render(request, 'login.html', )

@login_required
def add_bf(request):
	return render (request, 'add_bf.html', {'all_authors': models.Author.objects.all(), 'all_authors_count': models.Author.objects.all().count(), 'all_genres': models.Genre.objects.all(), 'all_genre_count': models.Genre.objects.all().count(), 'all_publishers': models.Publisher.objects.all(),	'all_publishers_count': models.Publisher.objects.all().count(), 'all_books_count': models.Book.objects.all().count(),'user_type':readerOrCritic(request.user.id)})

@login_required
def add_book_bf(request):
	if request.method == 'POST':
		newbook = models.Book.create(title=request.POST['new_booktitle'])
		newbook.author = models.Author.objects.get(id=request.POST['add_author'])
		newbook.publisher = models.Publisher.objects.get(id=request.POST['add_publisher'])
		newbook.save()
		selected_genre = request.POST.getlist('add_genre')
		for genre_id in selected_genre:
			newbook.genre.add(models.Genre.objects.get(id=genre_id))
		newbook.publication_date = request.POST['add_pubdate']
		newbook.cover_picture = request.POST['add_bookcover']
		newbook.book_synopsis = request.POST['add_booksummary']
		newbook.save()
		return list_recent_models(request, "New Book Added!")

@login_required
def add_author_bf(request):
	if request.method =='POST':
		newauthor = models.Author.create(first_name=request.POST['first_name'])
		newauthor.last_name=request.POST['last_name']
		newauthor.bio=request.POST['bio']
		newauthor.gender=request.POST['gender']
		newauthor.date_of_birth=request.POST['date_of_birth']
		newauthor.profile_picture=request.POST['profile_picture']
		newauthor.save()
		return list_recent_models(request, "New Author Added!")

def add_review_bf(request):
	if request.method=='POST':
		newreview = models.Review.create(heading=request.POST['heading'])
		book_to_assign = models.Book.objects.get(id=int(request.POST['book_id']))
		newreview.status= request.POST['status']
		newreview.critic = models.Critic.objects.get(user_id=request.user.id)
		newreview.book = book_to_assign
		newreview.review = request.POST['review']
		newreview.save()
		return list_recent_models(request, "New Review Added!")

@login_required
def edit_review(request):
	review_to_edit = models.Review.objects.get(id=request.POST['review_id'])
	review_to_edit.heading = request.POST['review_heading']
	review_to_edit.status = request.POST['status']
	review_to_edit.review = request.POST['review']
	review_to_edit.save()
	return show_review_by_id(request, request.POST['review_id'], "Review Updated!")

@login_required
def add_publisher(request):
	pass
	