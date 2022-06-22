from django.shortcuts import render

# Create your views here.

# /user/register
def register(request):
    return render(request, 'register.html')

def register_handle(request):
    pass