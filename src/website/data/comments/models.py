#   Website
#   Copyright © 2019-2020  scrub
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>.

import datetime
from typing import Any, Optional

from sqlalchemy import sql

from website import db

NUMBER_OF_DIGITS: int = 6


class Comment(db.Model):  # type: ignore
    __tablename__ = "comments"

    id = db.Column(db.Integer(), primary_key=True)
    body = db.Column(db.String(200), nullable=False)
    path = db.Column(db.Text(), index=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=sql.func.current_timestamp(),
        nullable=False,
    )
    updated_at = db.Column(
        db.DateTime(timezone=True), onupdate=sql.func.current_timestamp(),
    )
    thread_at = db.Column(
        db.DateTime(timezone=True),
        server_default=sql.func.current_timestamp(),
        nullable=False,
    )

    replies = db.relationship(
        "Comment",
        cascade="all, delete",
        backref=db.backref("parent", remote_side=[id]),
        lazy="dynamic",
    )

    author_id = db.Column(db.Integer(), db.ForeignKey("accounts.id"))
    blog_id = db.Column(
        db.Integer(), db.ForeignKey("blogs.id"), nullable=False
    )
    parent_id = db.Column(db.Integer(), db.ForeignKey("comments.id"))

    def __repr__(self):
        return f"<Comment {self.id} - {self.body}>"

    # Factories

    @classmethod
    def new(
        cls,
        *,
        body: str,
        author: Any,
        blog: Any,
        parent: Optional[Any] = None,
        thread_at: Optional[datetime.datetime] = None,
    ):
        # TODO: Make this a transaction
        comment = cls(
            body=body,
            author=author,
            blog=blog,
            parent=parent,
            thread_at=thread_at,
        )
        db.session.add(comment)
        db.session.commit()
        comment.updated_at = None
        prefix = f"{comment.parent.path}." if comment.parent else ""
        comment.path = prefix + "{:0{}d}".format(comment.id, NUMBER_OF_DIGITS)
        db.session.commit()
        return comment

    # Mutators

    def update(self, **kwargs):
        """
        Update Comment.
        """
        allowed_attributes = [
            "body",
            "author",
        ]
        for key, value in kwargs.items():
            assert key in allowed_attributes
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        """
        Delete Comment.
        """
        db.session.delete(self)
        db.session.commit()

    # Properties

    @property
    def level(self):
        return len(self.path) // NUMBER_OF_DIGITS - 1
