from locust import HttpUser, task, between
class PerformanceTestUser(HttpUser):
    wait_time = between(0.1, 0.5)
    @task
    def ride_list(self):
        self.client.get("/api/rides/?page=1&page_size=10")