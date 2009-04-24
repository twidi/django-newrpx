from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rpx.models import RpxData
from django.utils import simplejson
import urllib
import urllib2

import settings
TRUSTED_PROVIDERS=set(getattr(settings,'RPX_TRUSTED_PROVIDERS', []))

class MappingApi:
    identifier = ''
    api_key = settings.RPXNOW_API_KEY
    realm = settings.RPXNOW_REALM
    
        
    def request_map(self, user, token=''):
        print "tokeeeeeen -%s-" % token
        # first the the new identifier and extra info
        url = 'https://rpxnow.com/api/v2/auth_info'
        args = {
          'format': 'json',
          'apiKey': settings.RPXNOW_API_KEY,
          'token': token
        }

        r = urllib2.urlopen(url=url,
          data=urllib.urlencode(args),
        )
        json = simplejson.load(r)
        print json
        if json['stat'] <> 'ok':
            return False
        profile = json['profile']
        new_identifier = profile['identifier']
        print "tengo identifier ....... "
        url = 'https://rpxnow.com/api/v2/map'
        args = {
          'format': 'json',
          'apiKey': settings.RPXNOW_API_KEY,
          'identifier': new_identifier,
          'primaryKey': user.pk
        }
        r = urllib2.urlopen(url=url,
          data=urllib.urlencode(args),
        )
        json = simplejson.load(r)
        print json
        if json['stat'] <> 'ok':
            return False
        return True


        
        
    
        

        
        
