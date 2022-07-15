from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import engine, get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    tags= ['POSTS']
)

#EXAMPLE TO MAKE EASY INSTEAD OF MAKING /posts A COUPLE TIMES
# router = APIRouter(
#     prefix="/posts"
# )
# @router.get('/{id}')


#GET ALL POSTS AND LIMIT IS A QUERY PARAMETER posts?limit=5
# @router.get('/posts', response_model = List[schemas.PostResponse])
@router.get('/posts', response_model = List[schemas.PostOut])
def getPosts(db: Session = Depends(get_db), currentUser: int = Depends(oauth2.get_current_user), limit: int = 100, skip: int = 0, search: Optional[str] = ""):
    
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # print(posts)
    # print(postVotes)
    # print(limit)

    return posts

#GET ALL POSTS BASED ON WHOs THE OWNER OF THE POSTS IS
@router.get('/posts/mine')
def getPosts(db: Session = Depends(get_db), currentUser: int = Depends(oauth2.get_current_user)):
    # posts = db.query(models.Post).filter(models.Post.owner_id == currentUser.id).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.owner_id == currentUser.id).all()

    # print(posts)
    return {'data' : posts}


#GET POSTS BY ID
@router.get('/posts/{id}')
def getPosts(id: int, db: Session = Depends(get_db), currentUser: int = Depends(oauth2.get_current_user)): #converted id to int
    # print(id)

    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
   
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'id {id} doesnt exist')

    # if post.owner_id != currentUser.id:
    #     raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f'Not authorized to perform requested action')

    return {"data" : post}

#POST POSTS
@router.post('/posts', status_code= status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def createPost(post: schemas.PostBase, db: Session = Depends(get_db), currentUser: int = Depends(oauth2.get_current_user)):
    # print(post.dict())
    # newPost = models.Post(title = post.title, content = post.content, published = post.published)

    print(currentUser.email)

    newPost = models.Post(owner_id = currentUser.id, **post.dict())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    message = {
        'message' : 'data is successfully posted',
        'data' : newPost #newPost.title
    }
    print(newPost)
    return newPost

#UPDATE POSTS
@router.put('/posts/{id}')
def updatePosts(id:int, updatedPost: schemas.PostBase, db: Session = Depends(get_db), currentUser: int = Depends(oauth2.get_current_user)):
    postQuery = db.query(models.Post).filter(models.Post.id == id)

    post = postQuery.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'id {id} doesnt exist')

    if post.owner_id != currentUser.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f'Not authorized to perform requested action')

    postQuery.update(updatedPost.dict(), synchronize_session = False)
    db.commit()

    return {'message' : 'data was updated', 'data' : postQuery.first() }

#DELETE POSTS
@router.delete('/posts/{id}')
def deletePost(id:int, db: Session = Depends(get_db), currentUser: int = Depends(oauth2.get_current_user)):
    postQuery = db.query(models.Post).filter(models.Post.id == id)

    post = postQuery.first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'id {id} doesnt exist')

    if post.owner_id != currentUser.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f'Not authorized to perform requested action')

    postQuery.delete(synchronize_session = False)
    db.commit()

    return {'message' : f'data with id {id} was deleted'}