from django.http import HttpResponse
from django.shortcuts import render
import datetime

def hello(request):
	return HttpResponse("Hello")

def current_time(request):
	now=	datetime.datetime.now()
	context_dict={'current_time': now, }
	return render(request, 'present_time.html', context_dict)

def hours_ahead(request, offset):
	try:
		offset=	int(offset)
	except valueError:
		raise Http404
	dt=	datetime.datetime.now()+datetime.timedelta(hours=offset)
	context_dict={'offset': offset, 'future_time': dt, }
	return render(request, 'future_time.html', context_dict)