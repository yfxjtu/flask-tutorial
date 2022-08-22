from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("test_plan", __name__,url_prefix="/test_plan")


@bp.route("/")
def index():
    """Show all the test_plans, most recent first."""
    db = get_db()
    test_plans = db.execute(
        "SELECT p.id, title, content, created,author_id,username"
        " FROM test_plan p  JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("test_plan/index.html", test_plans=test_plans)


def get_test_plan(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, content, created, author_id, username"
            " FROM test_plan p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new test_plan for the current user."""
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        error = None

        if not title:
            error = "计划名称不能为空！"

        if not content:
            error = "测试内容不能为空！"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO test_plan (title, content, author_id) VALUES (?, ?, ?)",
                (title, content, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("test_plan.index"))

    return render_template("test_plan/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    test_plan = get_test_plan(id)

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        error = None

        if not title:
            error = "计划名称不能为空！"

        if not content:
            error = "测试内容不能为空！"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE test_plan SET title = ?, content = ? WHERE id = ?", (title, content, id)
            )
            db.commit()
            return redirect(url_for("test_plan.index"))

    return render_template("test_plan/update.html", test_plan=test_plan)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_test_plan(id)
    db = get_db()
    db.execute("DELETE FROM test_plan WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("test_plan.index"))
