from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)

    posts: so.WriteOnlyMapped["Post"] = so.relationship(back_populates="author")

    def __repr__(self):
        return f"<User {self.username}>"

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(1000000))
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    author: so.Mapped[User] = so.relationship(back_populates="posts")

    def __repr__(self):
        return f"<Post {self.body}>"
    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))