from django.http.response import JsonResponse, HttpResponseBadRequest, Http404
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.parsers import JSONParser

from .models import Question, Choice
from .permissions import IsOwnerOrReadOnly
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
        except (KeyError, TypeError, Question.DoesNotExist) as e:
            return HttpResponseBadRequest(content=e)
    

class UserList(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get(self, request: Request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    
class UserDetail(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get(self, request: Request, user_id: int):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=user_id)
        serializer = self.get_serializer(user)
        return JsonResponse(serializer.data, safe=False)

