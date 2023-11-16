from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Event
from .serializers import EventSerializer


# class EventViewSet(viewsets.ModelViewSet):
#     serializer_class = EventSerializer
#     queryset = Event.objects.all()
#
# event_list = EventViewSet.as_view({"get": "list"})
# event_detail = EventViewSet.as_view({"get": "retrieve"})

@api_view(["GET", "POST"])
def event_list(request):
    if request.method == "GET":
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        if request.GET:
            try:
                events = Event.objects.filter(type__exact=request.GET.get("type"))
                serializer = EventSerializer(events, many=True)
                serializer = EventSerializer(data=serializer.data)
                if not serializer.is_valid():
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except Event.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data)

    elif request.method == "POST":
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def event_detail(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = EventSerializer(event)
        return Response(serializer.data)


@api_view(["GET"])
def user_list(request, user_id):
    events = Event.objects.filter(user=user_id)

    if request.method == "GET":
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def repo_list(request, repo_id):
    events = Event.objects.filter(repo_id__exact=repo_id)

    if request.method == "GET":
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
