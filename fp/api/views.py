from datetime import datetime

from django.shortcuts import get_object_or_404

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from .models import Docket, Document
from .serializers import DocketSerializer, DocumentSerializer

# Create your views here.
class DocketView(GenericAPIView):
    queryset = Docket.objects.all()
    serializer_class = DocketSerializer

    def get(self, request: Request):
        queryset = self.get_queryset()
        docket_no = request.data.get("id")
        if docket_no != None:
            docket = get_object_or_404(queryset, pk=docket_no)
            serializer = self.get_serializer(docket)
            return Response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return  Response(serializer.data)
    
    
    def post(self, request: Request):
        data: dict[str] = JSONParser().parse(request)
        date_filled: list[str] = data.get("date_filled").split("/")
        parsed_date = datetime(
            month=int(date_filled[0]), 
            day=int(date_filled[0]), 
            year=int(date_filled[2])
        )
        data.update({"date_filled" : parsed_date})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "OK"}, status=200)
        

        
class DocumentView(GenericAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    
    def get(self, request):
        queryset = self.get_queryset()
        document_id = request.data.get("id")
        if document_id != None:
            document = get_object_or_404(queryset, pk=document_id)
            serializer = self.get_serializer(document)
            return Response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return  Response(serializer.data)
    
    def post(self, request: Request):
        data: dict[str] = JSONParser().parse(request)
        date_filed: list[str] = data.get("date_filed").split("-")
        parsed_date = datetime(
            month=int(date_filed[1]),
            day=int(date_filed[2]), 
            year=int(date_filed[0])
        )
        data.update({"date_filed" : parsed_date})
        data["docket"] = get_object_or_404(Docket, pk=data.get("docket"))
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "OK"}, status=200)
            