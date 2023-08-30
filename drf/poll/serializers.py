from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Question, Choice


class QuestionSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    owner = serializers.ReadOnlyField(source='owner.username')
    question_text = serializers.CharField(max_length=200)
    pub_date = serializers.DateTimeField(required=False)
    
    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance: Question, validated_data):
        instance.question_text = validated_data.get(
            'question_text', instance.question_text)
        instance.owner = validated_data.get(
            'owner', instance.owner)
        instance.pub_date = validated_data.get(
            'pub_date', instance.pub_date)
        instance.save()
        return instance

    
class ChoiceSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    question = serializers.ReadOnlyField(source='question.id')
    choice_text = serializers.CharField(max_length=200)
    vote = serializers.IntegerField(required=False)
    
    def create(self, validated_data):
        return Choice.objects.create(**validated_data)

    def update(self, instance: Choice, validated_data):
        instance.choice_text = validated_data.get(
            'choice_text', instance.choice_text)
        instance.vote = instance.vote + validated_data.get(
            'vote', instance.vote)
        instance.save()
        return instance


class UserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField()
    questions = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all, many=True)
