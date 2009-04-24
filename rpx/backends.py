from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rpx.models import RpxData
from rpx.api import RpxApi
import settings
TRUSTED_PROVIDERS=set(getattr(settings,'RPX_TRUSTED_PROVIDERS', []))

class RpxBackend:
    def get_user(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None
    def get_user_by_rpx_id(self, rpx_id):
        try:
            rpx_data = RpxData.objects.get(identifier=rpx_id)
            return rpx_data.user
        except RpxData.DoesNotExist:
            return None                

    def authenticate(self, token=''):
        """
        TODO: pass in a message array here which can be filled with an error
        message with failure response
        """
        api = RpxApi()
        json = api.get_auth_info(token)
        if json['stat'] <> 'ok':
            return None
        profile = json['profile']
        rpx_id = profile['identifier']
        nickname = profile.get('displayName') or \
          profile.get('preferredUsername')
        email = profile.get('email', '')
        profile_pic_url = profile.get('photo')
        info_page_url = profile.get('url')
        provider=profile.get("providerName")

        user=self.get_user_by_rpx_id(rpx_id)
        
        if not user:
            # no match. we can try to match on email, though, provided that doesn't steal
            # an rpx association
            if email and profile['providerName'] in TRUSTED_PROVIDERS:
                #beware - this would allow account theft, so we only allow it
                #for trusted providers
                user_candidates=User.objects.all().filter(
                  rpxdata=None).filter(email=email)
                # if unambiguous, do it. otherwise, don't.
                if user_candidates.count()==1:
                    [user]=user_candidates
                    rpxdata=RpxData(identifier=rpx_id)
                else:
                    return None
            else:
                #no match, create a new user - but there may be duplicate user names.
                username=nickname
                user=None
                try:
                    i=0
                    while True:
                        User.objects.get(username=username)
                        username=permute_name(nickname, i)
                        i+=1
                except User.DoesNotExist:
                    #available name!
                    user=User.objects.create_user(username, email)
                rpxdata = RpxData(identifier=rpx_id)
                rpxdata.user=user
                try:
                    rpxdata.save()
                except:
                    # the object already exists
                    return False
        rpxdata = RpxData.objects.get(identifier=rpx_id)
        api.save_data(json, rpxdata, user)
        if profile_pic_url:
            rpxdata.profile_pic_url=profile_pic_url
        if info_page_url:
            rpxdata.info_page_url=info_page_url
        if provider:
            rpxdata.provider=provider
        rpxdata.save()
        return user
