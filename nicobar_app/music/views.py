# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status
from .models import Songs
from .serializers import SongsSerializer
from .decorators import validate_data


class ListSongsView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer

    @validate_data
    def post(self, request, *args, **kwargs):
        a_song = Songs.objects.create(
            title=request.data["title"],
            artist=request.data["artist"]
        )
        return Response(
            data=SongsSerializer(a_song).data,
            status=status.HTTP_201_CREATED
        )


class SongsDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    GET songs/:id/
    PUT songs/:id/
    DELETE songs/:id/
    """
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            return Response(SongsSerializer(a_song).data)
        except Songs.DoesNotExist:
            return Response(
                data={
                    "message": "Song with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_data
    def put(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            serializer = SongsSerializer()
            updated_song = serializer.update(a_song, request.data)
            return Response(SongsSerializer(updated_song).data)
        except Songs.DoesNotExist:
            return Response(
                data={
                    "message": "Song with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            a_song.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Songs.DoesNotExist:
            return Response(
                data={
                    "message": "Song with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

