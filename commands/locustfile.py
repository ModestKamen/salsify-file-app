from locust import HttpUser, task
import random


class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        random_number = random.randint(100_000_000, 200_000_729)
        self.client.get(f"/lines/{random_number}")
