from django.utils import simplejson
import urllib
import urllib2
import settings

from django.contrib.auth.models import User
from rpx.models import RpxData


class RpxApi:
    """
    A representation of the RpxApi, implements the main functionality such as
    get auth info, map, unmap, and get a list of maps.
    """

    def get_auth_info(self, token=''):
        """
        Used for getting a new identifier
        Arguments:
        - `self`: this object
        - `token`: a token to be parsed by token_url
        """
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
        return json

    def save_data(self, json, rpxdata, user):
        """
        Saves a RpxData instance with the json data provided and asscociates
        it with user
        Arguments:
        - `self`: this object
        - `json`: the data to be saved in json format
        - `rpxdata`: an RpxData instance
        - `user`: a django.contrib.auth.models.User instance
        """
        
        profile = json['profile']
        rpx_id = profile['identifier']
        nickname = profile.get('displayName') or \
          profile.get('preferredUsername')
        email = profile.get('email', '')
        profile_pic_url = profile.get('photo')
        info_page_url = profile.get('url')
        provider=profile.get("providerName")        
        rpxdata.user=user
        if profile_pic_url:
            rpxdata.profile_pic_url=profile_pic_url
        if info_page_url:
            rpxdata.info_page_url=info_page_url
        if provider:
            rpxdata.provider=provider
        try:
            rpxdata.save()
        except:
            # the object already exists
            return False
        return True

    def request_map(self, user, token=''):
        """
        Maps a new identifier for a user.
        First obtains the identifier and the maps it to an existing user
        Arguments:
        - `self`: thie object
        - `user`: a django.contrib.auth.models.User instance
        - `token`: a token string to be parsed 
        """    
        # first the the new identifier and extra info
        json = self.get_auth_info(token)
        if json['stat'] <> 'ok':
            return False
        profile = json['profile']
        new_identifier = profile['identifier']

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
        if json['stat'] <> 'ok':
            return False
        rpxdata=RpxData(identifier=rpx_id)
        return self.save_data(json, rpxdata, user)

    def request_unmap(self, user, identifier):
        """
        Removes the association between a user and an identifier
        Arguments:
        - `self`: this object
        - `user`: a django.contrib.auth.models.User instance
        - `identifier`: the identifier as string
        """
                url = 'https://rpxnow.com/api/v2/unmap'
        args = {
          'format': 'json',
          'apiKey': settings.RPXNOW_API_KEY,
          'identifier': identifier,
          'primaryKey': user.pk
        }
        r = urllib2.urlopen(url=url,
          data=urllib.urlencode(args),
        )
        json = simplejson.load(r)
        if json['stat'] <> 'ok':
            return False

        # now delete the indentifier
        try:
            rpxdata = RpxData.objects.get(identifier=identifier)
            rpxdata.delete()
        except RpxData.DoesNotExists:
            return False
        return True       


    def get_maps(self, user):
        """
        Returns a list of identifiers the user associated to the user
        Arguments:
        - `self`: this object
        - `user`: a django.contrib.auth.models.User instance
        """
        url = 'https://rpxnow.com/api/v2/mappings'
        args = {
          'format': 'json',
          'apiKey': settings.RPXNOW_API_KEY,
          'primaryKey': user.pk
        }
        r = urllib2.urlopen(url=url,
          data=urllib.urlencode(args),
        )
        json = simplejson.load(r)
        if json['stat'] <> 'ok':
            return False
        
        return json['identifiers']

        
