from django.conf.urls import url
from readbooks import views

urlpatterns	= [
	url(r'^$', views.sitelogin, name='login_url'),
	url(r'^$', views.sitelogout, name='logout_url'),

	url(r'^register/$', views.register, name='signup_url'),
	url(r'^add_book_bf/$', views.add_book_bf, name='add_book_url_bf'),

	url(r'^add_df/$', views.add_df, name='add_df_url'),
	url(r'^add_book_df/$', views.add_book_df, name='add_book_url_df'),
	url(r'^add_author_df/$', views.add_author_df, name='add_author_url_df'),

	url(r'^settings_bf/$', views.update_userinfo_bf, name='user_settings_url_bf'),
	url(r'^settings_df/$', views.update_userinfo_df, name='user_settings_url_df'),

	url(r'^messages/$', views.messages, name='messages_url'),
	url(r'^userprofile/(?P<user_id>[0-9]+)/$', views.show_user_profile, name='user_profile'),
	url(r'^add_review_df/$', views.add_review_df, name='add_review_url_df'), 
	url(r'add_book_df2/$', views.add_book_df2, name='add_book_df2_url'),
	url(r'^home/$', views.readbooks_index, name='readbooks_index_url'),
	url(r'^search/$', views.search,	name='search_url'),
	url(r'^new/$', views.list_recent_models, name='list_recent_models_url'),
	
	url(r'^book/(?P<book_id>[0-9]+)/$', views.show_book_by_id, name='book_byID_url'),
	url(r'^author/(?P<author_id>[0-9]+)/$', views.show_author_by_id, name='author_byID_url'),
	url(r'^publisher/(?P<publisher_id>[0-9]+)/$', views.show_publisher_by_id, name='publisher_byID_url'),
	url(r'^reader/(?P<reader_id>[0-9]+)/$', views.show_reader_by_id, name='reader_byID_url'),
	url(r'^critic/(?P<critic_id>[0-9]+)/$', views.show_critic_by_id, name='critic_byID_url'),
	url(r'^group/(?P<group_id>[0-9]+)/$', views.show_group_by_id, name='group_byID_url'),
	url(r'^topic/(?P<topic_id>[0-9]+)/$', views.show_topic_by_id, name='topic_byID_url'),
	url(r'review/(?P<review_id>[0-9]+)/$', views.show_review_by_id, name='review_byID_url'),
	url(r'genre/(?P<genre_id>[0-9]+)/$', views.show_genre_by_id, name='genre_byID_url'),

]
