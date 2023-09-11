from datetime import datetime

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication, BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

import jwt
from jwt.exceptions import DecodeError
from poll.serializers import UserSerializer

from pollsite.settings import SECRET_KEY


class BearerAuthentication(TokenAuthentication):
    keyword = 'Bearer'
    

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            auth_header = request.headers['Authorization']
            auth_header_split = auth_header.split(' ')
            token_split = auth_header_split[1].split('.')
            
            if (not auth_header 
                or len(auth_header_split) != 2 
                or len(token_split) < 2):
                raise AuthenticationFailed('Invalid token.')
        
            payload = jwt.decode(
                auth_header_split[1], algorithms='HS256', key=SECRET_KEY)
        
            if datetime.now().timestamp() > payload['exp']:
                raise AuthenticationFailed('Token expired.')

            user = get_object_or_404(User, pk=payload['uid'])
        except KeyError as e:
            raise AuthenticationFailed(
                {"error": f"Missing {e.args} in request."})
        except (DecodeError, User.DoesNotExist) as e:
            raise AuthenticationFailed(e)

        return (user, auth_header)
    
    def authenticate_header(self, request):
        return super().authenticate_header(request)