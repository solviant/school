from django.http import HttpResponse
from django.shortcuts import render


# def test_site(request):
#     return HttpResponse("Hello, world.")

def test_site(request):
    return render(request, 'schoolregister/test_site.html')
