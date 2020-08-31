#   Website
#   Copyright © 2019-2020  Scrub
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

# from sqlalchemy import orm

from typing import Any, List, Optional

import sqlalchemy_utc

from website import db


class Blog(db.Model):  # type: ignore
    __tablename__ = "blogs"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100), index=True, nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.String(150))
    body = db.Column(db.Text(), nullable=False)

    published = db.Column(db.Boolean(), nullable=False, default=False)
    comment = db.Column(db.Boolean(), nullable=True, default=False)

    created_at = db.Column(
        sqlalchemy_utc.UtcDateTime(),
        nullable=False,
        server_default=sqlalchemy_utc.utcnow(),
    )
    updated_at = db.Column(
        sqlalchemy_utc.UtcDateTime(), onupdate=sqlalchemy_utc.utcnow()
    )

    author_id = db.Column(
        db.Integer(), db.ForeignKey("accounts.id"), nullable=True
    )
    comments = db.relationship(
        "Comment", cascade="all, delete", backref="blog", lazy=True
    )

    def __repr__(self):
        return f"<Blog {self.title}>"

    # TODO: We need to prevent blank values.
    # @orm.validates("title")
    # def validate(self, key, value):
    #     assert value
    #     return value

    # Factories

    @classmethod
    def new(
        cls,
        title: str,
        slug: str,
        body: str,
        author: Any,
        description: Optional[str] = None,
        categories: Optional[List[Any]] = None,
        published: bool = False,
        comment: bool = False,
    ):
        """
        Create a new Blog in the database.

        Returns a Blog.
        """
        blog = cls(
            title=title,
            slug=slug,
            description=description,
            body=body,
            author=author,
            published=published,
            comment=comment,
        )

        if categories:
            blog.categories = categories

        db.session.add(blog)
        db.session.commit()

        return blog

    # Mutators

    def update(self, **kwargs):
        """
        Update Blog.
        """
        allowed_attributes = [
            "title",
            "description",
            "body",
            "author",
            "categories",
            "published",
            "comment",
        ]
        for key, value in kwargs.items():
            assert key in allowed_attributes
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        """
        Delete Blog.
        """
        db.session.delete(self)
        db.session.commit()

    # Properties

    @property
    def is_published(self) -> bool:
        return self.published
