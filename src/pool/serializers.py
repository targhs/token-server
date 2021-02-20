from rest_framework import serializers

from . import models


class TokenSerializer(serializers.ModelSerializer):
    status_display_name = serializers.CharField(
        source="get_status_display", read_only=True
    )

    class Meta:
        model = models.Token
        fields = [
            "id",
            "key",
            "status",
            "status_display_name",
            "expiry",
            "allocated_till",
        ]
        read_only_fields = [
            "expiry",
            "allocated_till",
            'status',
        ]
