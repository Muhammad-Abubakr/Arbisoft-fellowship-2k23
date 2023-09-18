from django.shortcuts import get_object_or_404

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Docket, Document
from .serializers import DocketSerializer, DocumentSerializer

# Create your views here.
class DocketView(GenericAPIView):
    queryset = Docket.objects.all()
    serializer_class = DocketSerializer

    def get(self, request: Request):
        queryset = self.get_queryset()
        docket_no = request.data.get("docket_no")
        if docket_no != None:
            docket = get_object_or_404(queryset, pk=docket_no)
            serializer = self.get_serializer(docket)
            return Response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return  Response(serializer.data)
    
    
    # {'docket_no': '23-09001',
    # 'date_filled': '09/01/2023',
    # 'description': 'Informational Report of Sierra Pacific Power Company d/b/a NV Energy concerning its natural gas resource planning activities.'}
    def post(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status": "OK"}, status=200)
            

        
class DocumentView(GenericAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    
    def get(self, request):
        queryset = self.get_queryset()
        document_id = request.data.get("document_id")
        if document_id != None:
            document = get_object_or_404(queryset, pk=document_id)
            serializer = self.get_serializer(document)
            return Response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return  Response(serializer.data)
    
    def post(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status": "OK"}, status=200)
            