#!/usr/bin/python
# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import logout
from social_auth import __version__ as version

def contacto(request):
    return render_to_response('contacto.html',RequestContext(request))
def que(request):
    return render_to_response('que.html',RequestContext(request))
def buscar(request):
    return render_to_response('que.html',RequestContext(request))

def unete(request):
    if request.user.is_authenticated():
        return redirect('/')
    else:
        return render_to_response('unete.html', {'version': version },RequestContext(request))
def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('/')

