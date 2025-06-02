from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, func, Text, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from sqlalchemy import Enum as SqlEnum

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)

    posts: Mapped[List['Post']] = relationship(back_populates='author')
    comments: Mapped[List['Comment']] = relationship(back_populates='commenter')

    def serialize(self):
        
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            # do not serialize the password, its a security breach
        }

class Follower(db.Model):
    __tablename__ = 'follower'

    follower_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key= True)
    followed_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key= True)

    def serialize(self):
        return{
            'follower_id': self.follower_id,
            'followed_id': self.followed_id
        }
    

class Post(db.Model):
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'),  nullable=False)

    author: Mapped['User'] = relationship(back_populates='posts')
    media: Mapped[List['Media']] = relationship(back_populates='the_post')
    the_comments: Mapped[List['Comment']] = relationship(back_populates='post')

    def serialize(self):
        return{
            'id': self.id,
            'user_id': self.user_id
        }
    
class Media(db.Model):
    __tablename__ = 'media'

    id: Mapped[int] = mapped_column(primary_key=True)
    media_type: Mapped[str] = mapped_column(SqlEnum('image', 'video', name='media_type'), nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False) 

    the_post: Mapped['Post'] = relationship(back_populates='media')

    def serialize(self):
        return{
            'id': self.id,
            'media_type': self.media_type,
            'url': self.url,
            'post_id': self.post_id
        }
    
class Comment(db.Model):
    __tablename__ = 'comment'

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(2200), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)

    commenter: Mapped['User'] = relationship(back_populates='comments')
    post: Mapped['Post'] = relationship(back_populates='the_comments')

    def serialize(self):
        return{
            'id': self.id,
            'comment_text': self.comment_text,
            'author_id': self.author_id,
            'post_id': self.post_id
        }