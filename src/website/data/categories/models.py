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

import sqlalchemy_utc

from website import db

association_table = db.Table(
    "category_blog_association",
    db.Column("blogs_id", db.Integer(), db.ForeignKey("blogs.id")),
    db.Column("categories_id", db.Integer(), db.ForeignKey("categories.id")),
)


class Category(db.Model):  # type: ignore
    __tablename__ = "categories"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100), index=True, unique=True, nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.String(150), nullable=False)

    created_at = db.Column(
        sqlalchemy_utc.UtcDateTime(),
        nullable=False,
        server_default=sqlalchemy_utc.utcnow(),
    )
    updated_at = db.Column(
        sqlalchemy_utc.UtcDateTime(), onupdate=sqlalchemy_utc.utcnow()
    )

    blogs = db.relationship(
        "Blog", secondary=association_table, backref="categories"
    )

    def __repr__(self):
        return f"<Category {self.title}>"

    @classmethod
    def new(
        cls, title: str, slug: str, description: str,
    ):
        """
        Create a new Category in the database.

        Returns a Category.
        """
        category = cls(title=title, slug=slug, description=description,)

        db.session.add(category)
        db.session.commit()

        return category

    # Mutators

    def update(self, **kwargs):
        """
        Update Category.
        """
        allowed_attributes = ["title", "description"]
        for key, value in kwargs.items():
            assert key in allowed_attributes
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        """
        Delete Category.
        """
        db.session.delete(self)
        db.session.commit()
