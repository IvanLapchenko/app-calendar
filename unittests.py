import unittest
import requests


class TestCalendarAPI(unittest.TestCase):
    token = None

    def setUp(self):
        self.url = "http://localhost:5000"
        self.headers = {"Content-Type": "application/json"}
        self.login_data = {
            "nickname": "test_nickname",
            "password": "test_password",
            "email": "test_email@test.com"
        }

    def test1_register_new_user(self):
        response = requests.post(f"{self.url}/signup", json=self.login_data, headers=self.headers)

        # check if user added to db
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["isAddedToDB"], True)

        # check if user with the same credentials cannot be added to db
        response = requests.post(f"{self.url}/signup", json=self.login_data, headers=self.headers)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["isAddedToDB"], False)
        self.assertEqual(response.json()["reason"], "user exist")

    def test2_login_right_credentials(self):
        global token
        response = requests.post(f"{self.url}/login", json=self.login_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("token" in response.json())
        token = response.json()["token"]

    def test3_login_wrong_credentials(self):
        data = {
            "nickname": "test_nickname",
            "password": "wrong_password"
        }
        response = requests.post(f"{self.url}/login", json=data, headers=self.headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"isLogged": False})

    def test4_create_event(self):
        global token
        data = {
            "header": "test_event",
            "describe": "test_description",
            "date": "2023-03-17",
            "time": "11:00"
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{self.url}/create_event", json=data, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["msg"], "success")

    def test5_get_events(self):
        global token
        date = "2023-03-17"
        self.headers["Authorization"] = f"Bearer {token}"
        response = requests.get(f"{self.url}/get_events_by/{date}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test6_delete_user_by_email(self):
        response = requests.get(f"{self.url}/delete_user_by/{self.login_data['email']}", headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["is_deleted"], True)


if __name__ == "__main__":
    unittest.main()

    #
    # def test_add_event_to_calendar(self):
    #     data = {
    #         "title": "Test event",
    #         "date": "2023-04-01",
    #         "time": "14:00",
    #         "description": "This is a test event"
    #     }
    #
    #     response = requests.post(self.url + "/create_event", json=data, headers=self.headers)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json()["title"], "Test event")
    #     self.assertEqual(response.json()["date"], "2023-04-01")
    #     self.assertEqual(response.json()["time"], "14:00")
    #
    #
    # def test_get_event_from_calendar(self):
    #     date = "2023-04-01"
    #     response = requests.get(self.url + f"/get_events_by/{date}")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json()["title"], "Test event")
    #     self.assertEqual(response.json()["start_date"], "2023-04-01")
    #     self.assertEqual(response.json()["time"], "14:00")

    # def test_edit_event_in_calendar(self):
    #     event_id = 1
    #     data = {
    #         "title": "Test event",
    #         "date": "2023-04-01",
    #         "time": "14:00",
    #         "description": "This is a test event"
    #     }
    #     response = requests.put(self.url + f"/{event_id}", json=data, headers=self.headers)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json()["title"], "Edited test event")
    #     self.assertEqual(response.json()["start_date"], "2023-04-01")
    #     self.assertEqual(response.json()["end_date"], "2023-04-05")
    #
    # def test_delete_event_from_calendar(self):
    #     event_id = 1
    #     response = requests.delete(self.url + f"/{event_id}")
    #     self.assertEqual(response.status_code, 204)
    #
