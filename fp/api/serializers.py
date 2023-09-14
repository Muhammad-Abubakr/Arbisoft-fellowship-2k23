from rest_framework import serializers

from .models import Docket

class DocketSerializer(serializers.Serializer):
    docket_no = serializers.CharField()
    timestamp = serializers.ReadOnlyField()
    date_filled = serializers.CharField()
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