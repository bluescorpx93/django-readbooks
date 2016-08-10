from django.contrib import admin
from readbooks import models

class AuthorAdmin(admin.ModelAdmin):
	list_display  =	('first_name', 'last_name', 'date_of_birth',)
	search_fields =	('first_name', 'last_name')
	list_filter   =	('last_name', )

class CriticAdmin(admin.ModelAdmin):
	list_display  =	('first_name', 'last_name', 'date_of_birth')
	search_fields =	('first_name', 'last_name')
	list_filter   =	('last_name', )

class ReaderAdmin(admin.ModelAdmin):
	list_display  =	('first_name', 'last_name', 'date_of_birth', )
	search_fields =	('first_name', 'last_name')
	list_filter   =	('last_name', )

class GenreAdmin(admin.ModelAdmin):
	list_display  =	('name', )
	search_fields =	('name', )

class PublisherAdmin(admin.ModelAdmin):
	list_display  =	('name', 'website')
	search_fields =	('name', 'website')

class BookAdmin(admin.ModelAdmin):
	list_display  =	('title', 'publication_date', )
	search_fields =	('title', )
	list_filter   =	('publication_date', )

class ReviewAdmin(admin.ModelAdmin):
	list_display   =	('heading','critic','book', 'status')
	search_fields  =	('heading', 'critic', 'book')
	list_filter    =	('pubdate', )
	date_hierarchy = 'pubdate'

class CommentAdmin(admin.ModelAdmin):
	list_display 	=	('reader_comment', 'reader', 'book', 'message_time')

class ReadersCurrentlyReadAdmin(admin.ModelAdmin):
	list_display  =	('book', 'reader',  )
	search_fields =	('book', 'reader', )

class GroupAdmin(admin.ModelAdmin):
	list_display  = ('name', 'group_description', 'topic_count', 'member_count', )
	search_fields = ('name', )

class TopicAdmin(admin.ModelAdmin):
	list_display   = ('name', 'creation_date', 'reply_count', )
	search_fields  = ('name', )
	list_filter    = ('creation_date', )
	date_hierarchy = 'creation_date'

class TopicReplyAdmin(admin.ModelAdmin):
	list_display   =	('topic', 'topic_reply_user', 'message_time')

class MembershipAdmin(admin.ModelAdmin):
	list_display	=	('groups', 'members', 'join_date', 'member_status')

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', )

admin.site.register(models.Book, BookAdmin)
admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Critic, CriticAdmin)
admin.site.register(models.Reader, ReaderAdmin)
admin.site.register(models.Publisher, PublisherAdmin)
admin.site.register(models.Genre, GenreAdmin)
admin.site.register(models.Review, ReviewAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.ReadersCurrentlyRead, ReadersCurrentlyReadAdmin)
admin.site.register(models.Group, GroupAdmin)
admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.TopicReply, TopicReplyAdmin)
admin.site.register(models.Membership, MembershipAdmin)

