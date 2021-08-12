## Environment:
- Python version: 3.11
- Django version: 4.2.7
- Django REST framework version: 3.14.0

## Read-Only Files:
- app/tests.py
- manage.py

## Data:
Description of an event data JSON object:

- `id`: the unique ID of the event (Integer)
- `type`: the type of the event: 'PushEvent', 'ReleaseEvent', or 'WatchEvent' (String)
- `public`: whether the event is public, either true or false (Boolean)
- `repo_id`: the ID of the repository the event belongs to (Integer)
- `actor_id`: the ID of the user who created the event (Integer)

Example of an event data JSON object:
```
{
   "type": "PushEvent",
   "public": true,
   "repo_id": 1,
   "actor_id": 1
}
```

## Requirements:

The REST service must expose endpoints, which allow managing the collection of event records in the following ways:

`POST` request to `/events/`:
- creates a new event
- expects a JSON event object without an id property as the body payload. You can assume that the given object is always valid except that the type might be invalid. A valid type is one of 'PushEvent', 'ReleaseEvent', or 'WatchEvent'.
- you can assume that all other values in the payload given to create the object are always valid
- if the given type is invalid, the response code is 400
- if the type is valid, it adds the given event object to the collection of events and assigns a unique integer id to it. The first created event must have id 1, the second one 2, and so on.
- if the type is valid, the response code is 201 and the response body is the created event object, including its id

`GET` request to `/events/`:
- returns a collection of all events
- the response code is 200, and the response body is an array of all events ordered by their ids in increasing order

`GET` request to `/events/:event_id/`:
- returns an event with the given id
- if the matching event exists, the response code is 200 and the response body is the matching event object
- if there is no event in the collection with the given id, the response code is 404

`GET` request to `/events/?type=:event_type`:
- returns a collection of events of the given type
- the response code is 200, and the response body is an array of events of the given type ordered by their ids in increasing order
- if type is invalid, the response code is 400

`GET` request to `/users/:user_id/events/`:
- returns a collection of events created by given user
- the response code is 200, and the response body is an array of events created by the given user ordered by their ids in increasing order

`GET` request to `/repos/:repo_id/events/`:
- returns a collection of events related to the given repository
- the response code is 200, and the response body is an array of events related to the given repository ordered by their ids in increasing order
