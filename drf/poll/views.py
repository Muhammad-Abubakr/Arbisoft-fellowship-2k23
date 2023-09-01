from base64 import urlsafe_b64decode, urlsafe_b64encode
from datetime import datetime, timedelta
from django.http.response import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth.models import User

from rest_framework import generics, views
from rest_framework.request import Request
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication

import jwt
from jwt.exceptions import DecodeError

from .models import Question, Choice
from pollsite.settings import SECRET_KEY
from .serializers import (
    QuestionSerializer, ChoiceSerializer, UserSerializer
)

# Create your views here.
class IndexView(generics.GenericAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    
    def get(self, request: Request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return  JsonResponse(serializer.data, safe=False)

    def post(self, request: Request):
        try:
            data = JSONParser().parse(request)
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save(owner=request.user)
                return JsonResponse(serializer.data, safe=False)
            return JsonResponse(serializer.errors, status=400)
        except KeyError as e:
            return JsonResponse(
                {"error": f"Missing {e.args} in request."}, status=400)
    
    def patch(self, request: Request):
        try:
            queryset = self.get_queryset()
            data = JSONParser().parse(request)
            question = get_object_or_404(queryset, pk=data["question_id"])
            serializer = self.get_serializer(question, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
        except KeyError as e:
            return JsonResponse(
                {"error": f"Missing {e.args} in request."}, status=400)
        except (TypeError, Question.DoesNotExist) as e:
            return HttpResponseBadRequest(content=e)
    
    def delete(self, request: Request):
        try:
            queryset = self.get_queryset()
            data = JSONParser().parse(request)
            question_id = int(data['question_id']) 
            question = get_object_or_404(queryset, pk=question_id)
            question.delete()
            serializer = QuestionSerializer(question)
            return JsonResponse(serializer.data, safe=False)
        except KeyError as e:
            return JsonResponse(
                {"error": f"Missing {e.args} in request."}, status=400)
        except (TypeError, Question.DoesNotExist) as e:
            return HttpResponseBadRequest(content=e)
    

class ChoiceView(generics.GenericAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    
    def get(self, request: Request, question_id: int):
        queryset = self.get_queryset()
        choices = get_list_or_404(queryset, question=question_id)
        serializer = self.get_serializer(choices, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    def post(self, request: Request, question_id: int):
        try:
            data = JSONParser().parse(request)
            question = Question.objects.get(pk=question_id)
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save(question=question)
                return JsonResponse(serializer.data, safe=False)
            return JsonResponse(serializer.errors, status=400)
        except KeyError as e:
            return JsonResponse(
                {"error": f"Missing {e.args} in request."}, status=400)
        except (TypeError, Question.DoesNotExist) as e:
            return HttpResponseBadRequest(content=e)

    def patch(self, request: Request, question_id: int):
        try:
            queryset = self.get_queryset()
            data = JSONParser().parse(request)
            choice = get_object_or_404(queryset, pk=data["choice_id"])
            serializer = self.get_serializer(
                choice, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, safe=False)
            return JsonResponse(serializer.errors, status=400)
        except KeyError as e:
            return JsonResponse(
                {"error": f"Missing {e.args} in request."}, status=400)
        except (TypeError, Question.DoesNotExist) as e:
            return HttpResponseBadRequest(content=e)
    
    def delete(self, request: Request, question_id: int):
        try:
            queryset = self.get_queryset()
            data = JSONParser().parse(request)
            choice = get_object_or_404(queryset, **data)
            choice.delete()
            serializer = self.get_serializer(choice)
            return JsonResponse(serializer.data, safe=False)
        except KeyError as e:
            return JsonResponse(
                {"error": f"Missing {e.args} in request."}, status=400)
        except (TypeError, Question.DoesNotExist) as e:
            return HttpResponseBadRequest(content=e)
    

class UserList(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get(self, request: Request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    
class UserAuth(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get(self, request: Request):
        try:
            auth_header = request.headers['Authorization']
            auth_header_split = auth_header.split(' ')
            token_split = auth_header_split[1].split('.')
            
            if (not auth_header 
                or len(auth_header_split) != 2 
                or len(token_split) < 2):
                raise AuthenticationFailed('Invalid token.')
        
            payload = jwt.decode(auth_header_split[1], algorithms='HS256', key=SECRET_KEY)
        
            if datetime.now().timestamp() > payload['exp']:
                raise AuthenticationFailed('Token expired.')

            queryset = self.get_queryset()
            user = get_object_or_404(queryset, pk=payload['uid'])
            serializer = self.get_serializer(user)
        except KeyError as e:
            return JsonResponse(
                {"error": f"Missing {e.args} in request."}, status=400)
        except (DecodeError, User.DoesNotExist) as e:
            raise AuthenticationFailed(e)

        return JsonResponse(serializer.data, safe=False)



class LoginView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def post(self, request):
        try:
            data = JSONParser().parse(request)
            user = get_object_or_404(
                self.get_queryset(), username=data['username'])
            header = {
                'alg': 'HS256',
                'typ': 'jwt'
            }
            payload = {
                'uid': user.id,
                'exp': datetime.utcnow() + timedelta(minutes=60),
                'iat': datetime.utcnow()
            }
            token = jwt.encode(
                payload=payload, headers=header, 
                algorithm='HS256', key=SECRET_KEY)
            
            response = JsonResponse({'jwt': token})
            response.set_cookie(
                key='jwt', value=token, httponly=True, 
                expires=timedelta(minutes=60), secure=True)
            return response
        
        except KeyError as e:
            return JsonResponse(
                {"error": f"Missing {e.args} in request."}, status=400)
        except (TypeError, Question.DoesNotExist) as e:
            return HttpResponseBadRequest(content=e)