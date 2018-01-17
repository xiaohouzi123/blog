from django.shortcuts import render

# Create your views here.
from user.forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():

            user = form.save()
            request.session['uid'] = user.id

    return render(request,'user/register.html',{})

def login(request):
    pass