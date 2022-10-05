from sqlite3 import Cursor
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import oauth2

from app import oauth2
from .. import models,schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),
    limit:int = 10,skip:int = 0, search:Optional[str] = ""):
    #posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post,
    func.count(models.Vote.post_id).label("Vote")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    #cur.execute("""SELECT * FROM posts """)
    #posts = cur.fetchall()
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    #cur.execute("""INSERT INTO posts(title, content, published) values(%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    #new_post = cur.fetchone()
    #conn.commit()
    new_post = models.Post(**post.dict())
    new_post.user_id = current_user.id 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: int, db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    #cur.execute("""SELECT * from posts where id=%s """,[id])
    #post=cur.fetchone()
    post = db.query(models.Post,
    func.count(models.Vote.post_id).label("Vote")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id, models.Post.user_id == current_user.id).first()
    if not post:
       # response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    #cur.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",[id])
    #deleted_post = cur.fetchone()
    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = deleted_post_query.first()
    print(deleted_post)
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    
    if deleted_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")

    deleted_post_query.delete(synchronize_session=False)
    db.commit() 
    #conn.commit()
    #return {"message": f"post with {id} deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate,db:Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    #cur.execute("""UPDATE posts SET title=%s, content =%s, published=%s where id=%s RETURNING *""",[post.title, post.content, post.published,id])
    #updated_post = cur.fetchone()
    updated_post_query = db.query(models.Post).filter(models.Post.id == id)
    
    updated_post = updated_post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    
    if updated_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")

    updated_post_query.update(post.dict(),synchronize_session=False)
    
    db.commit()
    #conn.commit()
    return updated_post_query.first()
