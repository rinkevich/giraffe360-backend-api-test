from json import JSONDecodeError

from django.test import TestCase

from rest_framework import status
from rest_framework.test import RequestsClient

event_01_push_actor_1 = {
    "type": "PushEvent",
    "public": True,
    "repo_id": 1,
    "actor_id": 1,
}

event_01_release_actor_1 = {
    "type": "ReleaseEvent",
    "public": True,
    "repo_id": 1,
    "actor_id": 1,
}

event_01_watch_actor_1 = {
    "type": "WatchEvent",
    "public": True,
    "repo_id": 1,
    "actor_id": 1,
}

event_02_watch_actor_1 = {
    "type": "WatchEvent",
    "public": True,
    "repo_id": 2,
    "actor_id": 1,
}

event_02_watch_actor_2 = {
    "type": "WatchEvent",
    "public": True,
    "repo_id": 2,
    "actor_id": 2,
}

HOST = "http://127.0.0.1:8000"


class CreateEventTest(TestCase):
    def setUp(self) -> None:
        self.client = RequestsClient()
        self.url = HOST + "/events/"

    def test_event_creation_valid_data(self):
        response = self.client.post(self.url, data=event_01_push_actor_1)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertIn("id", data)
        self.assertTrue(isinstance(data["id"], int))
        del data["id"]
        self.assertDictEqual(event_01_push_actor_1, data)

        response = self.client.post(self.url, data=event_02_watch_actor_1)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertIn("id", data)
        self.assertTrue(isinstance(data["id"], int))
        del data["id"]
        self.assertDictEqual(event_02_watch_actor_1, data)

    def test_event_creation_invalid_type(self):
        event_01_push_actor_1_copy = event_01_push_actor_1.copy()
        event_01_push_actor_1_copy["type"] = "pushevent"
        response = self.client.post(self.url, data=event_01_push_actor_1_copy)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestGetAllEvents(TestCase):
    def setUp(self) -> None:
        self.client = RequestsClient()
        self.url = HOST + "/events/"
        try:
            self.events = [
                self.client.post(self.url, data=event).json()
                for event in [
                    event_01_push_actor_1,
                    event_01_release_actor_1,
                    event_01_watch_actor_1,
                ]
            ]
        except JSONDecodeError:
            self.fail(
                "/events/ endpoint for POST request not implemented correctly"
            )
        self.events.sort(key=lambda event: event["id"])

    def test_get_all_events(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertListEqual(self.events, data)


class TestGetEvent(TestCase):
    def setUp(self) -> None:
        self.client = RequestsClient()
        self.url = HOST + "/events/{}/"
        try:
            self.events = [
                self.client.post(HOST + "/events/", data=event).json()
                for event in [
                    event_01_push_actor_1,
                    event_01_release_actor_1,
                    event_02_watch_actor_1,
                ]
            ]
        except JSONDecodeError:
            self.fail(
                "/events/ endpoint for POST request not implemented correctly"
            )

    def test_get_retrieve_existing_id(self):
        for event in self.events:
            event_id = event["id"]
            try:
                response = self.client.get(self.url.format(event_id))
            except JSONDecodeError:
                self.fail(
                    "/events/:event_id/ endpoint for GET request not implemented correctly"
                )
            self.assertEquals(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertDictEqual(event, data)

    def test_get_retrieve_non_existing_id(self):
        try:
            response = self.client.get(self.url.format(10000))
        except JSONDecodeError:
            self.fail(
                "/events/:event_id/ endpoint for GET request not implemented correctly"
            )
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)


class TestGetEventsByReport(TestCase):
    def setUp(self) -> None:
        self.client = RequestsClient()
        self.url = HOST + "/repos/{}/events/"
        try:
            self.events_with_repo_id_1 = [
                self.client.post(HOST + "/events/", data=event).json()
                for event in [
                    event_01_push_actor_1,
                    event_01_release_actor_1,
                    event_01_watch_actor_1,
                ]
            ]
            self.events_with_repo_id_1.sort(key=lambda event: event["id"])

            self.events_with_repo_id_2 = [
                self.client.post(HOST + "/events/", data=event).json()
                for event in [event_02_watch_actor_1]
            ]
        except JSONDecodeError:
            self.fail(
                "/events/ endpoint for POST request not implemented correctly"
            )

    def test_with_existing_id_1(self):
        try:
            response = self.client.get(self.url.format(1))
        except JSONDecodeError:
            self.fail(
                "/repos/:repo_id/events/ endpoint for GET request not implemented correctly"
            )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertListEqual(data, self.events_with_repo_id_1)

    def test_with_existing_id_2(self):
        try:
            response = self.client.get(self.url.format(2))
        except JSONDecodeError:
            self.fail(
                "/repos/:repo_id/events/ endpoint for GET request not implemented correctly"
            )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertListEqual(data, self.events_with_repo_id_2)

    def test_with_non_existing_id(self):
        try:
            response = self.client.get(self.url.format(10000))
        except JSONDecodeError:
            self.fail(
                "/repos/:repo_id/events/ endpoint for GET request not implemented correctly"
            )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertListEqual(data, [])


class TestGetEventByUser(TestCase):
    def setUp(self) -> None:
        self.client = RequestsClient()
        self.url = HOST + "/users/{}/events/"
        try:
            self.events_with_user_id_1 = [
                self.client.post(HOST + "/events/", data=event).json()
                for event in [
                    event_01_push_actor_1,
                    event_01_release_actor_1,
                    event_02_watch_actor_1,
                ]
            ]

            self.events_with_user_id_1.sort(key=lambda event: event["id"])

            self.events_with_user_id_2 = [
                self.client.post(HOST + "/events/", data=event).json()
                for event in [event_02_watch_actor_2]
            ]
        except JSONDecodeError:
            self.fail(
                "/events/ endpoint for POST request not implemented correctly"
            )

    def test_with_existing_id_1(self):
        try:
            response = self.client.get(self.url.format(1))
        except JSONDecodeError:
            self.fail(
                "/users/:user_id/events/ endpoint for GET request not implemented correctly"
            )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertListEqual(data, self.events_with_user_id_1)

    def test_with_existing_id_2(self):
        try:
            response = self.client.get(self.url.format(2))
        except JSONDecodeError:
            self.fail(
                "/users/:user_id/events/ endpoint for GET request not implemented correctly"
            )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertListEqual(data, self.events_with_user_id_2)

    def test_with_non_existing_id(self):
        try:
            response = self.client.get(self.url.format(10000))
        except JSONDecodeError:
            self.fail(
                "/users/:user_id/events/ endpoint for GET request not implemented correctly"
            )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertListEqual(data, [])


class TestGetEventWithFilter(TestCase):
    def setUp(self) -> None:
        self.client = RequestsClient()
        self.url = HOST + "/events/?type={}"
        try:
            self.database_events = [
                self.client.post(HOST + "/events/", data=event).json()
                for event in [
                    event_01_push_actor_1,
                    event_01_watch_actor_1,
                    event_01_release_actor_1,
                    event_02_watch_actor_1,
                ]
            ]

            self.database_events.sort(key=lambda event: event["id"])

            self.events_with_watch_events = list(
                filter(
                    lambda x: x["type"] == "WatchEvent", self.database_events
                )
            )

        except JSONDecodeError:
            self.fail(
                "/events/ endpoint for POST request not implemented correctly"
            )

    def test_with_wrong_filter(self):
        try:
            response = self.client.get(self.url.format("pushevent"))
        except JSONDecodeError:
            self.fail(
                "/events/?type=pushevent endpoint for GET request not implemented correctly"
            )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(
            response.content,
            {
                "type": [
                    "Select a valid choice. pushevent is not one of the available choices."
                ]
            },
        )

    def test_with_type_filter(self):
        try:
            response = self.client.get(self.url.format("WatchEvent"))
        except JSONDecodeError:
            self.fail(
                "/events/?type=WatchEvent endpoint for GET request not implemented correctly"
            )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertListEqual(data, self.events_with_watch_events)
