from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
    """Question model for polls app. Has one-many relationship with
    Choice model

    Parent Class:
        - django.db.models.Model : Parent Class to every django model
            provides an intuitive interface to the model, allowing 
            efficient and easy access to the model's objects
    
    Attrs:
        - question_text: django.db.models.CharField(max_length=200)
        - pub_date: django.db.models.DateTimeField("date published")
    """
    question_text = models.TextField(max_length=200)
    pub_date = models.DateTimeField()
    
    class Meta:
        ordering = ['pub_date']
    
class Choice(models.Model):
    """Choice model for polls app. Has many-one relationship with
    Question model

    Parent Class:
        - django.db.models.Model : Parent Class to every django model
            provides an intuitive interface to the model, allowing 
            efficient and easy access to the model's objects
    
    Attrs:
        - question ('question_id'): ForeignKey(Question, Cascade)
        - choice_text: CharField(max_length=200)
        - votes: IntegerField(default=0)
    """
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    choice_text = models.TextField(max_length=200)
    vote = models.IntegerField(default=0, auto_created=True)
    