from rest_framework import serializers


class DocketSerializer(serializers.Serializer):
    docket_no = serializers.IntegerField()
    timestamp = serializers.ReadOnlyField()
    date_filled = serializers.DateTimeField()
    description = serializers.CharField(max_length=512)
    