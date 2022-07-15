from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import database, models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

router =APIRouter(
    tags=['AUTHTENTICATION']
)

@router.post('/login', response_model= schemas.Token)
def login(userCredentials : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    # OAuth2PasswordRequestForm only return 2 things username and password
    print(userCredentials.password)
    #CHECKING INTO THE DB
    user = db.query(models.User).filter(models.User.email == userCredentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')
    
    #CHECKING IF HASHED PASSWORD IS EQUAL TO PLANE PASSWORD
    if not utils.verify(userCredentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')

    #CREATE A JWT TOKEN
    #AND RETURN TOKEN

    accessToken = oauth2.create_access_token(data = {'user_id' : user.id})
    return {'access_token': accessToken, 'token_type': 'bearer'}


