from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .models import Event
from .serializers import EventSerializer


@api_view(["GET", "POST"])
def event_list(request):
    if request.method == "GET":
        events = Event.objects.all()
        if request.GET:
            events = events.filter(type__exact=request.GET.get("type"))

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == "GET":
        serializer = EventSerializer(event)
        return Response(serializer.data)


@api_view(["GET"])
def user_list(request, user_id):
    events = Event.objects.filter(actor_id__exact=user_id)

    if request.method == "GET":
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def repo_list(request, repo_id):
    events = Event.objects.filter(repo_id__exact=repo_id)

    if request.method == "GET":
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
