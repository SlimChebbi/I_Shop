from django.shortcuts import render, redirect, get_object_or_404,\
    get_list_or_404
from django.http import Http404
from django.http import HttpResponse
from home.forms import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from accessoires.views import informatique


def home(request):
    if request.user.is_authenticated():
        return informatique(request)
    else:
        return render(request, 'home/login.html')
