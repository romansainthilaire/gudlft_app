from locust import HttpUser, task

from server import clubs, future_competitions

club = clubs[0]
competition = future_competitions[0]


class PerformanceTests(HttpUser):

    @task
    def index(self):
        self.client.get("/")

    @task
    def competitions_list(self):  # shouldn't take more than 5 seconds
        data = {"email": club["email"]}
        self.client.post("/show_summary", data)

    @task
    def booking_page(self):
        self.client.get(f"/book/{competition['name']}/{club['name']}")

    @task
    def purchase_places(self):  # shouldn't take more than 2 seconds
        data = {"club": club["name"], "competition": competition["name"], "places": 5}
        self.client.post("/purchase_places", data=data)

    @task
    def clubs_list(self):
        self.client.get(f"/clubs/{club['name']}")
