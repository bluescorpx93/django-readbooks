from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from readbooks import urls
import views

urlpatterns = [
	url(r'^readbooks/admin/',  include(admin.site.urls),   name='admin_url'),
	url(r'^hello/$',   views.hello,    name='url_hello'),
	url(r'^time/$',    views.current_time, name='present_time'),
	url(r'^time/plus/(\d{1,2})/$', views.hours_ahead,  name='future_time'),
	url(r'^readbooks/',    include(urls)),

	]  +   static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
