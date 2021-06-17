from django.shortcuts import render
from shop.models import Userl
from django.core import serializers
from json import dumps

# Create your views here.
def index(request):
    if request.method == "POST":
        name = request.POST.get('sname', "")
        email = request.POST.get('semail', "")
        passwrd = request.POST.get('spswrd', "")
        rpasswrd = request.POST.get('srpswrd', "")
        if passwrd == rpasswrd:
            userl = Userl(u_name=name, u_email=email, u_psswrd=passwrd, u_rpsswrd=rpasswrd)
            userl.save()

    users = Userl.objects.all()
    ret = {}
    for user in users:
        ret.update({user.u_name: user.u_psswrd})
        ret.update({user.u_email: user.u_psswrd})
    users = dumps(ret)
    params = {'users': users}
    return render(request, 'index.html', params)