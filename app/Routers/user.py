from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import engine, get_db

router = APIRouter(
    tags=['USERS']
)

# -- USERS ROUTER --
# POST USER
@router.post('/users', status_code= status.HTTP_201_CREATED, response_model= schemas.UserResponse)
def createUser(user : schemas.UserCreate, db: Session = Depends(get_db)):

    #CHECK EXISTED EMAIL IN THE DATABASE
    checkEmail = db.query(models.User).filter(models.User.email == user.email).first()
    if checkEmail:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f'email {user.email} has been used')

    #hash the password from user.password
    hashedPassword = utils.hash(user.password)
    user.password = hashedPassword # save back to the user or update it

    # SAVE TO DB
    newUser = models.User(**user.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return newUser

# GET USER BY ID
@router.get('/users/{id}', response_model= schemas.UserResponse)
def createUser(id:int, db: Session = Depends(get_db), ):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f'user with id {id} was not found')

    return user
    

