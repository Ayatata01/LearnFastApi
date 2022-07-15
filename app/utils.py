from passlib.context import CryptContext

#BCRYPT CONFIGURATION
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def hash(password : str):
    return pwd_context.hash(password)

def verify(plainPassword, hashedPasswords):
    return pwd_context.verify(plainPassword, hashedPasswords)

