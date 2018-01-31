from django.shortcuts import render
from django.http import HttpResponse  # Use only for placeholding e.g. HttpResponse(html_markup)

# Create your views here.
def home_page(request):
    return render(request, 'home.html')
