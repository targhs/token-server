from rest_framework.decorators import action
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response


from . import models
from . import serializers


class PoolViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Token.objects.all()
    serializer_class = serializers.TokenSerializer

    @action(methods=["POST"], detail=False)
    def assign(self, request):
        available_token = (
            self.get_queryset()
            .filter(status=models.Token.Status.UNBLOCKED)
            .first()
        )
        if available_token:
            serializer = self.serializer_class(available_token)
            available_token.assign()
            available_token.save()
            return Response(serializer.data)
        return Response(
            {"detail": "No token available"}, status=status.HTTP_404_NOT_FOUND
        )

    @action(
        methods=["PATCH"],
        detail=True,
    )
    def unblock(self, request, pk):
        token = self.get_object()
        token.unblock()
        token.save()
        serializer = self.serializer_class(token)
        return Response(serializer.data)

    @action(
        methods=["PATCH"],
        detail=True,
    )
    def refresh(self, request, pk):
        token = self.get_object()
        token.refresh()
        token.save()
        serializer = self.serializer_class(token)
        return Response(serializer.data)