from rest_framework import generics
from rest_framework.exceptions import ValidationError

from .models import Event
from .serializers import EventSerializer


class EventCreateView(generics.ListCreateAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        events = Event.objects.all()
        if self.request.GET:
            event_type = self.request.GET.get("type")
            if event_type not in [choice[0] for choice in Event.EVENT_CHOICES]:
                raise ValidationError(
                    detail={
                        "type": [f"Select a valid choice. {event_type} is not one of "
                                 f"the available choices."]
                    }
                )
            events = events.filter(type__exact=event_type)

        return events


class EventListView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class UserListView(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(actor_id__exact=self.kwargs.get("user_id"))


class RepoListView(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(repo_id__exact=self.kwargs.get("repo_id"))
