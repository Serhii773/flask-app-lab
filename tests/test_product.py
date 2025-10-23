import unittest, json
from app import app

class ProductsBPTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_list(self):
        r = self.client.get("/products/")
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"Watch", r.data)
        self.assertIn(b"Horse", r.data)
        self.assertIn(b"Gypsi", r.data)

    def test_detail_ok(self):
        r = self.client.get("/products/1")
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"Watch", r.data)

    def test_detail_not_found(self):
        r = self.client.get("/products/999")
        self.assertEqual(r.status_code, 404)
        self.assertIn(b"Product not found", r.data)

    def test_api_ok(self):
        r = self.client.get("/products/api/1")
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.data.decode("utf-8"))
        self.assertEqual(data["id"], 1)
        self.assertIn("name", data)
        self.assertIn("price", data)

    def test_api_not_found(self):
        r = self.client.get("/products/api/999")
        self.assertEqual(r.status_code, 404)
        data = json.loads(r.data.decode("utf-8"))
        self.assertEqual(data.get("error"), "Product not found")

if __name__ == "__main__":
    unittest.main()
