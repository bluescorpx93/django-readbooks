from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import Q
from readbooks import models
from readbooks import forms
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.contrib import messages
from datetime import date

def user_upload_dir(instance, filename):
	return 'profile_pics/users/user_{0}/{1}'.format(instance.id, filename)

def calculate_age(dob):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def ReaderorCritic(id):
	try:
		models.Reader.objects.get(user_id=id)
		return "Reader"
	except ObjectDoesNotExist:
		models.Critic.objects.get(user_id=id)
		return "Critic"

@login_required
def readbooks_index(request):
	return render(request, 'index.html',{'user_type': ReaderorCritic(request.user.id) })

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
def list_recent_models(request):
	return render(request,	'list_recent_objects.html', { 
	'recent_books': models.Book.objects.all().order_by('-id')[:4],
	'recent_authors': models.Author.objects.all().order_by('-id')[:4], 
	'recent_reviews': models.Review.objects.all().order_by('-id')[:4], 
	'recent_groups': models.Group.objects.all().order_by('-id')[:4],
	'recent_topics': models.Topic.objects.all().order_by('-id')[:10],})

@login_required
def show_book_by_id(request, book_id):
	try:
		book_obj = models.Book.objects.get(id=int(book_id))
		reviews_book_obj = models.Review.objects.filter(book=int(book_id)).order_by('-id')[:10]
		comments_by_book_obj = models.Comment.objects.filter(book=int(book_id)).order_by('-id')
	except ObjectDoesNotExist:
		return render(request, 'default404.html',)
	return render(request, 'book_profile.html', {'book_obj': book_obj,'reviews_book_obj': reviews_book_obj, 'comments_by_book_obj': comments_by_book_obj,'user_type': ReaderorCritic(request.user.id), 'add_review_form': forms.AddReviewForm()})

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

@login_required
def show_review_by_id(request, review_id):
	try:
		review_obj= models.Review.objects.get(id=int(review_id))
	except ObjectDoesNotExist:
		return render(request, 'default404.html')
	return render(request, 'book_review.html', {'review_obj': review_obj})

@login_required
def show_group_by_id(request, group_id):
	try:
		group_obj = models.Group.objects.get(id=int(group_id))
		topics_by_group_obj = models.Topic.objects.filter(group=int(group_id))
		book_recs_by_group_obj = models.BookRecommendation.objects.filter(group=int(group_id))
	except ObjectDoesNotExist:
		return render(request, 'default404.html')
	return render(request, 'group_page.html', {'group_obj': group_obj, 'topics_by_group_obj': topics_by_group_obj, 'book_recs_by_group_obj': book_recs_by_group_obj, 'user_type': ReaderorCritic(request),})

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
def show_user_profile(request, user_id):
	return render (request, 'user_profile.html', { 'the_user': models.User.objects.get(id=user_id),'the_userprofile': models.UserProfile.objects.get(user_id=request.user.id),})

@login_required
def update_userinfo_df(request):
	loggeduser = models.User.objects.get(id=request.user.id)
	loggeduserprofile = models.UserProfile.objects.get(user_id=request.user.id)
	context_dict = {'form': forms.UserProfileForm(),'loggeduser': loggeduser,	'loggeduserprofile': loggeduserprofile,}
	try:
		if request.method=='POST':
			form = forms.UserProfileForm(request.POST)
			if form.is_valid():
				loggeduser.first_name = form.cleaned_data['first_name']
				loggeduser.last_name = form.cleaned_data['last_name']
				loggeduser.save()
				loggeduserprofile.bio = form.cleaned_data['bio']
				loggeduserprofile.date_of_birth = form.cleaned_data['date_of_birth']
				loggeduserprofile.gender = form.cleaned_data['gender']
				loggeduserprofile.profile_picture = form.cleaned_data['profile_picture']
				loggeduserprofile.save()
				return render(request, 'user_settings_df.html', {'loggeduser': loggeduser,'loggeduserprofile': loggeduserprofile,'success': "Profile Updated Successfully",	})
			else:
				return render(request, 'user_settings_df.html', {'form': forms.UserProfileForm(), 'loggeduser': loggeduser, 'loggeduserprofile': loggeduserprofile,'problem': "Sorry there was an error",})
	except Exception as excp:
		return render(request, 'user_settings_df.html', {'form': forms.UserProfileForm(),'excp': excp,'loggeduser': loggeduser, 'loggeduserprofile': loggeduserprofile,'problem': "Sorry there was an error"})
	else:
		return render(request, 'user_settings_df.html', context_dict)

@login_required
def update_userinfo_bf(request):
	loggeduser = models.User.objects.get(id=request.user.id)
	user_type=ReaderorCritic(request.user.id)
	if user_type == 'Reader':
		loggedProfile =models.Reader.objects.get(user_id=request.user.id)
	else:
		loggedProfile =  models.Critic.objects.get(user_id=request.user.id)
	context_dict = {'loggeduser': loggeduser, 'loggedProfile': loggedProfile, 'user_type':user_type,}
	if request.method=='POST':
		loggeduser.first_name = request.POST['userfirstname']
		loggeduser.last_name= request.POST['userlastname']
		loggeduser.save()
		loggedProfile.first_name=request.POST['userfirstname']
		loggedProfile.last_name=request.POST['userlastname']
		loggedProfile.bio = request.POST['userbio']
		loggedProfile.gender = request.POST['usergender']
		loggedProfile.date_of_birth = request.POST.get('userdob')
		# image_location=user_upload_dir(loggeduserprofile, request.POST.get('userprofilepic'))
		loggedProfile.profile_picture = request.POST['userprofilepic']
		loggedProfile.save()
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
def add_book_df2(request):
	book_form = forms.AddBookForm2(request.POST or None)
	if book_form.is_valid():
		newbook = book_form.save(commit=False)
		newbook.save()
	return render(request, 'add_book_df2.html', {'book_form': forms.AddBookForm2(),})

@login_required
def add_book_df(request):
	add_book_form = forms.AddBookForm(request.POST or None)
	# if request.method=='POST':
	if add_book_form.is_valid():
		newbook = add_book_form.save(commit=False)
		# newbook = Book.create(title=add_book_form.cleaned_data['title'])
		# newbook.save()
		# newbook.author= add_book_form.cleaned_data['author']
		# newbook.publisher = add_book_form.cleaned_data['publisher']
		# newbook.genre = add_book_form.cleaned_data['genre']
		# newbook.publication_date = add_book_form.cleaned_data['publication_date']
		# newbook.cover_picture = add_book_form.cleaned_data['cover_picture']
		# newbook.book_synopsis = add_book_form.cleaned_data['book_synopsis']
		newbook.save()
		# return render (request, 'add_df.html', {'add_book_form':forms.AddBookForm(),'add_author_form': forms.AddAuthorForm(),'success': "Book Created!",})
	else:
		# messages.debug(request, 'What happened')
		return render(request, 'add_df.html', {'add_book_form':forms.AddBookForm(),'add_author_form':forms.AddAuthorForm(),'problem': "There was a problem",})
	# except Exception as exc:
	# 	return render(request, 'add_df.html', {'add_author_form':forms.AddAuthorForm(), 'add_book_form':forms.AddBookForm(),'problem': exc })

	return render(request, 'add_df.html', {'add_author_form':forms.AddAuthorForm(), 'add_book_form':forms.AddBookForm(),'problem': exc })


@login_required
def add_df(request):
	return render (request, 'add_df.html', {'add_book_form':forms.AddBookForm(),'add_author_form':forms.AddAuthorForm(),})

@login_required
def add_book_bf(request):
	if request.method == 'POST':
		newbook = models.Book.objects.create(title=request.POST['new_booktitle'])
		# , author=request.POST['add_author'],publisher=request.POST['add_publisher'], genre=request.POST['add_genre'],publication_date= request.POST['add_pubdate'],book_synopsis= request.POST['add_booksummary'],cover_picture= request.POST['add_bookcover'])

	# return render(request, 'add_book_bf.html',{
	# 'all_authors': models.Author.objects.all(), 'all_genres': models.Genre.objects.all(),	'all_publishers': models.Publisher.objects.all(),
	# })

			# , author=request.POST['add_author'],publisher=request.POST['add_publisher'], genre=request.POST['add_genre'],publication_date= request.POST['add_pubdate'],book_synopsis= request.POST['add_booksummary'],cover_picture= request.POST['add_bookcover'])
		# newbook.save()
		# newbook.author = request.POST['add_author']
		# newbook.publisher = 
		# newbook.genre = 
		# newbook.publication_date= request.POST['add_pubdate']
		# newbook.book_synopsis= request.POST['add_booksummary']
		# newbook.cover_picture= request.POST['add_bookcover']
		# newbook.save()
		return render(request, 'add_book_bf.html', {'all_authors': models.Author.objects.all(), 'all_genres': models.Genre.objects.all(),	'all_publishers': models.Publisher.objects.all(),})
	# else:
	# return render (request, 'add_book_bf.html', {'all_authors': models.Author.objects.all(), 'all_genres': models.Genre.objects.all(),	'all_publishers': models.Publisher.objects.all(),	})

@login_required
def add_author_df(request):
	if request.method=='POST':
		add_author_form = forms.AddAuthorForm(request.POST)
		if add_author_form.is_valid():
			newauthor = models.Author.create(first_name=add_author_form.cleaned_data['first_name'])
			newauthor.save()
			newauthor.last_name=add_author_form.cleaned_data['last_name']
			newauthor.gender=add_author_form.cleaned_data['gender']
			newauthor.date_of_birth=add_author_form.cleaned_data['date_of_birth']
			newauthor.bio=add_author_form.cleaned_data['bio']
			newauthor.profile_picture=add_author_form.cleaned_data['profile_picture']
			newauthor.save()
			return render(request, 'add_df.html', {'add_book_form':forms.AddBookForm(),'add_author_form':forms.AddAuthorForm(),'success': "Author Added!"})
	else:
		return render(request, 'add_df.html', {'add_book_form':forms.AddBookForm(),'add_author_form':forms.AddAuthorForm(),})

def add_review_df(request):
	loggedCritic =  models.Critic.objects.get(user_id=request.user.id)
	if request.method=='POST':
		add_review_form = forms.AddReviewForm(request.POST)
		newreview = models.Review.create(heading=request.POST['heading'])
		book_to_assign = models.Book.objects.get(id=int(request.POST['book_id']))
		# if add_review_form.is_valid():
			# newreview.save()
		newreview.status= request.POST['status']
		newreview.critic = loggedCritic
		newreview.book = book_to_assign
		newreview.review = request.POST['review']
		newreview.save()
		# return newreview
	else:
		return render(request, 'add_df.html', {'add_review_form':forms.AddReviewForm()} )

			# newreview.Book = 
@login_required
def edit_author_df(request, author_id):
	author = models.Author.objects.get(id=author_id)
	form = forms.AddAuthorForm(request.POST or None, instance=author)
	if form.is_valid():
		author=form.save(commit=False)
		author.save()
	return render(request, 'edit_author.html', {'form': form, 'author': author})