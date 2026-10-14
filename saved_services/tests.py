def test_save_service(self):
    response = self.client.post(f"/api/saved-services/", {"service": self.service.id})
    self.assertEqual(response.status_code, 201)


def test_duplicate_save(self):
    self.client.post(f"/api/saved-services/", {"service": self.service.id})
    response = self.client.post(f"/api/saved-services/", {"service": self.service.id})
    self.assertEqual(response.status_code, 400)


def test_list(self):
    response = self.client.get(f"/api/saved-services/")
    self.assertEqual(response.status_code, 200)


def test_remove(self):
    save = self.client.post(f"/api/saved-services/", {"service": self.service.id})
    # id teesi delete cheyali
    response = self.client.delete(f"/api/saved-services/{self.service.id}/")
    self.assertEqual(response.status_code, 204)


def test_unauthorized(self):
    self.client.credentials()  # token remove
    response = self.client.get(f"/api/saved-services/")
    self.assertEqual(response.status_code, 401)


def test_service_not_found(self):
    response = self.client.post(f"/api/saved-services/", {"service": 99999})
    self.assertEqual(response.status_code, 404)