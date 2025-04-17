from datetime import datetime

from bson import ObjectId
from rest_framework import serializers


class ObjectIdField(serializers.Field):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        return ObjectId(data)


class TransactionSerializer(serializers.Serializer):
    _id = ObjectIdField(read_only=True)
    merchantId = ObjectIdField()
    amount = serializers.IntegerField()
    createdAt = serializers.DateTimeField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if "createdAt" in data and isinstance(instance["createdAt"], datetime):
            data["createdAt"] = instance["createdAt"].isoformat()
        return data


class TransactionQueryParamsSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=["amount", "count"])
    mode = serializers.ChoiceField(choices=["daily", "weekly", "monthly"])
    merchantId = serializers.CharField(
        required=False,
        max_length=24,
        min_length=24,
        error_messages={
            "min_length": "merchantId is too short",
            "max_length": "merchantId is too long",
            "invalid": "Invalid merchantId",
        },
    )


class TransactionResponseSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.IntegerField()
