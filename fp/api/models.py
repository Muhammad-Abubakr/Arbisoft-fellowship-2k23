from django.db import models
from datetime import datetime

# Create your models here.
class Docket(models.Model):
    """Docket model for the listings scraped from homepage of pucweb1.
    Has one-to-many relationship with the model Document.

    Parent Class:
        - django.db.models.Model : Parent Class to every django model
            provides an intuitive interface to the model, allowing 
            efficient and easy access to the model's objects
    
    Attrs:
        - docket_no: BigIntegerField (primary_key)
        - timestamp: DateTimeField (timestamp when this docket was 
                    scraped from the web)
        - date_filled: DateTimeField (date when the docket was filled)
        - description: CharField (description of the docket)
    
    Meta:
        ordering: date_filled [DESC]
    """
    docket_no = models.CharField(primary_key=True, max_length=9)
    timestamp = models.DateTimeField(default=datetime.now().isoformat())
    date_filled = models.CharField(max_length=16)
    description = models.CharField(max_length=512)
    
    class Meta:
        ordering = ['-date_filled']
        
class Document(models.Model):
    """Document model for the listings scraped from each docket of 
    pucweb1. Has many-to-one relationship with the model Docket.

    Parent Class:
        - django.db.models.Model : Parent Class to every django model
            provides an intuitive interface to the model, allowing 
            efficient and easy access to the model's objects
    
    Attrs:
        - docket: BigIntegerField (foreign_key, docket to which this
                document belongs to)
        - document_id: BigInteger (primary_key)
        - date_filled: DateTimeField (date when the document was filled)
        - doc_type: CharField (document type. such as Report)
        - notes: CharField (report notes for the document)
    
    Meta:
        ordering: date_filed [DESC]
    """
    docket = models.ForeignKey(to=Docket, on_delete=models.CASCADE)
    document_id = models.CharField(primary_key=True)
    date_filed = models.CharField(max_length=16)
    doc_type = models.CharField(max_length=64)
    notes = models.CharField(max_length=1024)
    
    class Meta:
        ordering = ['-date_filed']

