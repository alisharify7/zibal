"""
* Zibal Payment Test Task
*
* Developer: Ali Sharifi
* Email: alisharifyofficial@gmail.com
* Website: ali-sharify.ir
* GitHub: github.com/alisharify7/zibal
* Repository: https://github.com/alisharify7/zibal
"""

from rest_framework import serializers


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
