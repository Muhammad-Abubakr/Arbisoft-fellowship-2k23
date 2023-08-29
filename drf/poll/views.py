from django.http import JsonResponse, HttpResponseBadRequest
from django.utils import timezone
from rest_framework import views
from rest_framework.request import Request

from .models import Question, Choice
from .serializers import QuestionSerializer, ChoiceSerializer

# Create your views here.
class IndexView(views.APIView):
    def get(self, request: Request):
        serializer = QuestionSerializer(Question.objects.all(), many=True)
        return  JsonResponse(serializer.data, safe=False)

    def post(self, request: Request):
        data = request.data
        try:
            question_text = data['question_text']
            pub_date = timezone.now()
            question = Question.objects.create(
                question_text = question_text,
                pub_date = pub_date)
            question.save()
            serializer = QuestionSerializer(question)
            return JsonResponse({"created" : serializer.data})
        except KeyError:
            error_message = "question_text not found in request."
            return JsonResponse({"error_message" : error_message})
    
    def patch(self, request: Request):
        data = request.data
        try:
            question_text = data['question_text']
            question_id = int(data['question_id']) 
            question = Question.objects.get(pk=question_id)
            question.question_text = question_text
            question.save()
            serializer = QuestionSerializer(question)
            return JsonResponse({"updated" : serializer.data})
        except (KeyError, TypeError, Question.DoesNotExist):
            return HttpResponseBadRequest()
    
    def delete(self, request: Request):
        data = request.data
        try:
            question_id = int(data['question_id']) 
            question = Question.objects.get(pk=question_id)
            question.delete()
            serializer = QuestionSerializer(question)
            return JsonResponse({"deleted" : serializer.data})
        except (KeyError, TypeError, Question.DoesNotExist):
            return HttpResponseBadRequest()
    

class ChoiceView(views.APIView):
    def get(self, request: Request, question_id: int):
        try:
            question = Question.objects.get(pk=question_id)
            choices = question.choice_set.all()
            serializer = ChoiceSerializer(choices, many=True)
            return JsonResponse(serializer.data, safe=False)
        except Question.DoesNotExist:
            return HttpResponseBadRequest()
    
    def post(self, request: Request, question_id: int):
        data = request.data
        try:
            question = Question.objects.get(pk=question_id)
            choice_text = data["choice_text"]
            choice = Choice.objects.create(
                question=question,
                choice_text=choice_text)
            choice.save()
            serializer = ChoiceSerializer(choice)
            return JsonResponse({"created": serializer.data})
        except (KeyError, Question.DoesNotExist):
            return HttpResponseBadRequest()
    
    def delete(self, request: Request, question_id: int):
        data = request.data
        try:
            choice_id = int(data["choice_id"])
            choice = Choice.objects.get(pk=choice_id)
            choice.delete()
            serializer = ChoiceSerializer(choice)
            return JsonResponse({"deleted": serializer.data})
        except (KeyError, TypeError, Question.DoesNotExist):
            return HttpResponseBadRequest()
    
    def patch(self, request: Request, question_id: int):
        data = request.data
        try:
            choice_id = int(data["choice_id"])
            choice = Choice.objects.get(pk=choice_id)
            choice_text = data["choice_text"]
            choice.choice_text = choice_text
            choice.save()
            serializer = ChoiceSerializer(choice)
            return JsonResponse({"updated": serializer.data})
        except (KeyError, TypeError, Question.DoesNotExist):
            return HttpResponseBadRequest()


class VoteView(views.APIView):
    def post(self, request: Request, question_id: int):
        data = request.data
        try:
            choice_id = int(data["choice_id"])
            choice = Choice.objects.get(pk=choice_id)
            choice.vote += 1
            choice.save()
            serializer = ChoiceSerializer(choice)
            return JsonResponse({"updated": serializer.data})
        except (KeyError, TypeError, Question.DoesNotExist):
            return HttpResponseBadRequest()
