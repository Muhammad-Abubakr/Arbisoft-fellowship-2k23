from rest_framework import serializers

from .models import Docket, Document

class DocketSerializer(serializers.Serializer):
    docket_no = serializers.CharField()
    timestamp = serializers.ReadOnlyField()
    date_filled = serializers.DateTimeField()
    description = serializers.CharField()

    def create(self, validated_data):
        return Docket.objects.create(**validated_data)

    def update(self, instance: Docket, validated_data):
        instance.description = validated_data.get(
            'description', instance.description)
        instance.date_filled = validated_data.get(
            'date_filled', instance.date_filled)
        instance.save()
        return instance
    

class DocumentSerializer(serializers.Serializer):
    docket = serializers.ReadOnlyField()
    document_id = serializers.CharField()
    date_filed = serializers.DateTimeField()
    doc_type = serializers.CharField(max_length=64)
    notes = serializers.CharField(max_length=1024)

    def create(self, validated_data):
        return Document.objects.create(**validated_data)

    def update(self, instance: Document, validated_data):
        instance.date_filed = validated_data.get(
            'date_filed', instance.date_filed)
        instance.doc_type = validated_data.get(
            'doc_type', instance.doc_type)
        instance.notes = validated_data.get(
            'notes', instance.notes)
        instance.save()
        return instance