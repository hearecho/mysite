from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(request):
    context = {}

    return render_to_response("home.html",context)
    