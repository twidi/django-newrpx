from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from rpx.mapings import MappingApi

def permute_name(name_string, num):
    num_str=str(num)
    max_len=29-len(num_str)
    return ''.join([name_string[0:max_len], '-', num_str])

def rpx_response(request):
    """
    process the login token
    """
    token = request.GET.get('token', '')
    if not token: return HttpResponseForbidden()
    user=authenticate(token=token)
    if user and user.is_active:
        login(request, user)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseForbidden()

@login_required
def rpx_map(request):
    """
    maps an identifier to an existing
    """
    # first get the token
    token = request.GET.get('token', '')
    if not token: return HttpResponseForbidden()
       
    api = MappingApi()
    if api.request_map(request.user, token):
        return HttpResponseRedirect('/')
    return HttpResponseForbidden()
    
    
@login_required
def rpx_unmap(request):
    """
    unmaps an identifier from an existing user
    """
    # first get the identifier
    if request.method.lower() == 'post':
        identifier = request.POST.get('identifier', '')
        api = MappingApi()
        if api.request_unmap(request.user, identifier):
            return HttpResponseRedirect('/')
    return HttpResponseForbidden()
        
        

