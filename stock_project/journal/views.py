from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("baaaangla")

def detail(request, id):
    response = f"It's id: {id}"
    return HttpResponse (response)