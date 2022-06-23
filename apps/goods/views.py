from django.shortcuts import render

# Create your views here.
# 127.0.0.1:5000
def index(request):
    return render(request, 'index.html')
