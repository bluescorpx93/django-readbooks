from django.http import HttpResponse
from django.shortcuts import render
import datetime

def hello(request):
	return HttpResponse("Hello")
