from datetime import datetime

from flask import render_template, redirect, url_for, flash, request, session

from app import db
from . import posts_bp
from .models import Post, PostCategory
from .forms import PostForm, DeletePostForm


@posts_bp.route("/post", methods=["GET"])
def list_posts():
    stmt = (
        db.select(Post)
        .where(Post.is_active.is_(True))
        .order_by(Post.posted.desc())
    )
    posts = db.session.scalars(stmt).all()
    return render_template("posts/posts.html", posts=posts)


@posts_bp.route("/post/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()

    if request.method == "GET" and form.publish_date.data is None:
        form.publish_date.data = datetime.utcnow()

    if form.validate_on_submit():
        author = session.get("username", "Anonymous")

        post = Post(
            title=form.title.data,
            content=form.content.data,
            posted=form.publish_date.data or datetime.utcnow(),
            category=PostCategory(form.category.data),
            is_active=form.enabled.data,
            author=author,
        )

        db.session.add(post)
        db.session.commit()

        flash("Post successfully created", "success")
        return redirect(url_for("posts.list_posts"))

    return render_template(
        "posts/add_post.html",
        form=form,
        action="create",
        title="Create post",
    )


@posts_bp.route("/post/<int:post_id>", methods=["GET"])
def view_post(post_id: int):
    post = db.get_or_404(Post, post_id)
    delete_form = DeletePostForm()
    return render_template(
        "posts/detail_post.html",
        post=post,
        delete_form=delete_form,
        title=post.title,
    )


@posts_bp.route("/post/<int:post_id>/update", methods=["GET", "POST"])
def update_post(post_id: int):
    post = db.get_or_404(Post, post_id)

    if request.method == "GET":
        form = PostForm(
            title=post.title,
            content=post.content,
            enabled=post.is_active,
            category=post.category.value,
        )
        form.publish_date.data = post.posted
    else:
        form = PostForm()

    if form.validate_on_submit():
        form.populate_obj(post)
        post.posted = form.publish_date.data
        post.category = PostCategory(form.category.data)

        db.session.commit()
        flash("Post successfully updated", "success")
        return redirect(url_for("posts.view_post", post_id=post.id))

    return render_template(
        "posts/add_post.html",
        form=form,
        action="update",
        post=post,
        title="Edit post",
    )


@posts_bp.route("/post/<int:post_id>/delete", methods=["GET", "POST"])
def delete_post(post_id: int):
    post = db.get_or_404(Post, post_id)
    form = DeletePostForm()

    if request.method == "POST" and form.validate_on_submit():
        db.session.delete(post)
        db.session.commit()
        flash("Post successfully deleted", "warning")
        return redirect(url_for("posts.list_posts"))

    return render_template(
        "posts/delete_confirm.html",
        post=post,
        form=form
    )
