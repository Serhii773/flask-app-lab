# tests/test_posts.py
import unittest

from app import create_app, db
from app.posts.models import Post, PostCategory


class PostTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app("testing")
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False

        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self) -> None:
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    # --------- US01: створення поста ---------
    def test_create_post(self) -> None:
        with self.app.app_context():
            resp = self.client.post(
                "/post/create",
                data={
                    "title": "My first post",
                    "content": "Hello from test!",
                    "enabled": "y",
                    "publish_date": "2025-01-01T12:00",
                    "category": PostCategory.NEWS.value,
                    "submit": "Зберегти",
                },
                follow_redirects=True,
            )

            self.assertEqual(resp.status_code, 200)
            post = db.session.query(Post).filter_by(title="My first post").first()
            self.assertIsNotNone(post)
            self.assertEqual(post.content, "Hello from test!")

    # --------- US02: список постів ---------
    def test_list_posts(self) -> None:
        with self.app.app_context():
            p1 = Post(
                title="Post A",
                content="Content A",
                category=PostCategory.NEWS,
                is_active=True,
            )
            p2 = Post(
                title="Post B",
                content="Content B",
                category=PostCategory.TECH,
                is_active=True,
            )
            db.session.add_all([p1, p2])
            db.session.commit()

            resp = self.client.get("/post")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Post A", html)
            self.assertIn("Post B", html)

    # --------- US03: перегляд одного поста ---------
    def test_view_post_detail(self) -> None:
        with self.app.app_context():
            post = Post(
                title="Detail title",
                content="Full content here",
                category=PostCategory.NEWS,
                is_active=True,
            )
            db.session.add(post)
            db.session.commit()
            post_id = post.id

            resp = self.client.get(f"/post/{post_id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Detail title", html)
            self.assertIn("Full content here", html)

    # --------- US04: оновлення поста ---------
    def test_update_post(self) -> None:
        with self.app.app_context():
            post = Post(
                title="Old title",
                content="Old content",
                category=PostCategory.NEWS,
                is_active=True,
            )
            db.session.add(post)
            db.session.commit()
            post_id = post.id

            resp = self.client.post(
                f"/post/{post_id}/update",
                data={
                    "title": "New title",
                    "content": "New content",
                    "enabled": "y",
                    "publish_date": "2025-01-02T09:30",
                    "category": PostCategory.TECH.value,
                    "submit": "Зберегти",
                },
                follow_redirects=True,
            )

            self.assertEqual(resp.status_code, 200)

            db.session.refresh(post)
            self.assertEqual(post.title, "New title")
            self.assertEqual(post.content, "New content")

    # --------- US05: видалення поста ---------
    def test_delete_post(self) -> None:
        with self.app.app_context():
            post = Post(
                title="To be deleted",
                content="Delete me",
                category=PostCategory.NEWS,
                is_active=True,
            )
            db.session.add(post)
            db.session.commit()
            post_id = post.id

            resp = self.client.post(
                f"/post/{post_id}/delete",
                data={"submit": "Так, видалити"},
                follow_redirects=True,
            )
            self.assertEqual(resp.status_code, 200)

            deleted = db.session.get(Post, post_id)
            self.assertIsNone(deleted)

    # --------- US06: 404 для неіснуючого поста ---------
    def test_404_not_found(self) -> None:
        with self.app.app_context():
            resp = self.client.get("/post/999999")
            self.assertEqual(resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()
