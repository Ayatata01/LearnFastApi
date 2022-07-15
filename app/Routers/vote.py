from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import engine, get_db

router = APIRouter(
    tags= ["VOTE"]
)

@router.post('/votes', status_code= status.HTTP_201_CREATED)
def vote(vote : schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    # print(post)
    if not post:
        raise HTTPException(status_code=404, detail="Vote not found")

    voteQuery = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    foundVote = voteQuery.first()
    
    if vote.dir == 1:
        if foundVote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Vote already exists for {vote.post_id}")

        newVote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(newVote)
        db.commit()
        db.refresh(newVote)

        return {'message': 'successfully added vote to database'}
        
    else:
        if not foundVote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote not found for {vote.post_id}")
        
        voteQuery.delete(synchronize_session=False)
        db.commit()

        return {'message' : f'vote successfully deleted'}




