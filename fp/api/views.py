from django.shortcuts import get_object_or_404

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from .models import Docket
from .serializers import DocketSerializer

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
    
    def post(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def patch(self, request: Request):
        queryset = self.get_queryset()
        docket_no = request.data.get("docket_no")
        if docket_no != None:
            docket = get_object_or_404(queryset, pk=docket_no)
            serializer = self.get_serializer(
                docket, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        else:
            return Response(
            {"error": f"Missing docket_no in request."}, status=400)

    def delete(self, request: Request):
        queryset = self.get_queryset()
        docket_no = request.data.get('docket_no')
        if docket_no != None:
            docket = get_object_or_404(queryset, pk=docket_no)
            docket.delete()
            serializer = self.get_serializer(docket)
            return Response(serializer.data)
        else:       
            return Response(
                    {"error": f"Missing docket_no in request."}, status=400)
