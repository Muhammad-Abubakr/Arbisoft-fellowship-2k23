from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import AuthenticationFailed

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
        return  Response(serializer.data)

    def post(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def patch(self, request: Request):
        queryset = self.get_queryset()
        question_id = request.data.get("question_id")
        if question_id != None:
            try:
                question_id = int(question_id)
            except ValueError as e:
                return Response({"question_id": e.args}, status=400)
            
            question = get_object_or_404(queryset, pk=question_id)
            serializer = self.get_serializer(
                question, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        else:
            return Response(
            {"error": f"Missing question_id in request."}, status=400)

    def delete(self, request: Request):
        queryset = self.get_queryset()
        question_id = request.data.get('question_id')
        if question_id != None:
            try:
                question_id = int(question_id)
            except ValueError as e:
                return Response({"question_id": e.args}, status=400)
        
            question = get_object_or_404(queryset, pk=question_id)
            question.delete()
            serializer = QuestionSerializer(question)
            return Response(serializer.data)
        else:       
            return Response(
                    {"error": f"Missing question_id in request."}, status=400)


class ChoiceView(generics.GenericAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    
    def get(self, request: Request, question_id: int):
        queryset = self.get_queryset()
        choices = get_list_or_404(queryset, question=question_id)
        serializer = self.get_serializer(choices, many=True)
        return Response(serializer.data)
    
    def post(self, request: Request, question_id: int):
        question = get_object_or_404(Question, pk=question_id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(question=question)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request: Request, question_id: int):
        queryset = self.get_queryset()
        choice_id = request.data.get("choice_id")
        if choice_id != None:
            try:
                choice_id = int(choice_id)
            except ValueError as e:
                return Response({"choice_id": e.args}, status=400)
            
            choice = get_object_or_404(queryset, pk=choice_id)
            serializer = self.get_serializer(
                choice, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        else:
            return Response(
                {"error": f"Missing choice_id in request."}, status=400)
    
    def delete(self, request: Request, question_id: int):
        queryset = self.get_queryset()
        choice = get_object_or_404(queryset, **request.data)
        choice.delete()
        serializer = self.get_serializer(choice)
        return Response(serializer.data)
    

class UserList(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get(self, request: Request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    
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
        
            payload = jwt.decode(
                auth_header_split[1], algorithms='HS256', key=SECRET_KEY)
        
            if datetime.now().timestamp() > payload['exp']:
                raise AuthenticationFailed('Token expired.')

            queryset = self.get_queryset()
            user = get_object_or_404(queryset, pk=payload['uid'])
            serializer = self.get_serializer(user)
        except KeyError as e:
            return Response(
                {"error": f"Missing {e.args} in request."}, status=400)
        except (DecodeError, User.DoesNotExist) as e:
            raise AuthenticationFailed(e)

        return Response(serializer.data)


class LoginView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def post(self, request):
        try:
            data = JSONParser().parse(request)
            user = get_object_or_404(
                self.get_queryset(), username=data['email'])
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
            
            response = Response({'jwt': token})
            response.set_cookie(
                key='jwt', value=token, httponly=True, 
                expires=timedelta(minutes=60), secure=True)
            return response
        
        except KeyError as e:
            return Response(
                {"error": f"Missing {e.args} in request."}, status=400)
        except (ValueError, Question.DoesNotExist) as e:
            return Response({"error": e.args}, status=400)