# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from models import User, Chat, Admin
# from schemas import UserCreate, UserUpdate, AdminCreate, AdminLogin, UserResponse
# from database import get_db
# from typing import List
# from passlib.context import CryptContext

# from datetime import timedelta
# import jwt
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# from routers.auth import get_current_user # import authentication function

# router = APIRouter(prefix="/admin", tags=["Admin"])

# SECRET_KEY = "7bc55e1bfd81a0c62d610cb50f682a1f6b796a7956d0b959db8fd24f5b34ca44"
# ALGORITHM= "HS256" 
# ACCESS_TOKEN_EXPIRE_MINUTES = 60

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/login")

# # helper function

# def get_password_hash(password):
#     return pwd_context.hash(password)

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def create_access_token(data: dict, expires_delta: timedelta):
#     to_encode = data.copy()
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         admin_username = payload.get("sub")
#         if not admin_username:
#             raise HTTPException(status_code=401, detail="Invalid token")
        
#         admin = db.query(Admin).filter(Admin.username == admin_username).first()
#         if not admin:
#             raise HTTPException(status_code=401, detail="Admin not found")

#         return admin
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token expired")
#     except jwt.JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")


# # 🚀 **Admin Registration**
# @router.post("/register")
# def register_admin(admin_data: AdminCreate, db: Session = Depends(get_db)):
#     existing_admin = db.query(Admin).filter(Admin.username == admin_data.username).first()
#     if existing_admin:
#         raise HTTPException(status_code=400, detail="Username already taken")
    
#     hashed_password = get_password_hash(admin_data.password)
#     admin = Admin(username=admin_data.username, password=hashed_password)
#     db.add(admin)
#     db.commit()
#     db.refresh(admin)
    
#     return {"message": "Admin registered successfully"}


# # 🔑 **Admin Login**
# @router.post("/login")
# def login_admin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     admin = db.query(Admin).filter(Admin.username == form_data.username).first()
#     if not admin or not verify_password(form_data.password, admin.password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     token = create_access_token(data={"sub": admin.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
#     return {"access_token": token, "token_type": "bearer"}


# # 👤 **Create User (Admin Only)**
# @router.post("/users/add")
# def create_user(user_data: UserCreate, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
#     try:
#         hashed_password = get_password_hash(user_data.password)
#         user = User(username=user_data.username, email=user_data.email, password=hashed_password)
#         db.add(user)
#         db.commit()
#         return {"message": "User created successfully"}
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))


# # 📜 **Get All Users (Admin Only)**
# @router.get("/users", response_model=List[UserCreate])
# def get_users(db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
#     return db.query(User).all()


# # ❌ **Delete User (Admin Only)**
# @router.delete("/users/delete/{user_id}")
# def delete_user(user_id: int, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     db.delete(user)
#     db.commit()
#     return {"message": "User deleted successfully"}

# # old code
# # def admin_required():
# #     return True

# def admin_required(current_user: User = Depends(get_current_user)):
#     if not current_user.is_admin:
#         raise HTTPException(status_code=403, detail="Admin access required")
#     return current_user

# @router.get("/users", response_model=List[UserResponse])
# def get_users(db: Session = Depends(get_db), admin: User = Depends(admin_required)):
#     return db.query(User).all()

# @router.delete("/users/delete/{user_id}")
# def delete_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(admin_required)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     db.delete(user)
#     db.commit()
#     return {"message": "User deleted successfully"}

# def admin_required():
#     return True




# @router.post("/users/add")
# def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
#     try:
#         if not admin_required():
#             raise HTTPException(status_code=403, detail="Admin access required")
#         # user = User(**user_data.dict())
#         hashed_password = pwd_context.hash(user_data.password)
#         user =User(username=user_data.username, email=user_data.email, password=hashed_password)
#         db.add(user)
#         db.commit()
#         return {"message": "User created successfully"}
    
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

# @router.get("/users", response_model=List[UserCreate])
# def get_users(db: Session = Depends(get_db)):
#     return db.query(User).all()

# @router.delete("/users/delete/{user_id}")
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     if not admin_required():
#         raise HTTPException(status_code=403, detail="Admin access required")
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     db.delete(user)
#     db.commit()
#     return {"message": "User deleted successfully"}


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import User, Chat, Admin
from schemas import UserCreate, UserUpdate, AdminCreate, AdminLogin, UserResponse
from database import get_db
from typing import List
from passlib.context import CryptContext
from datetime import timedelta
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import re
from pydantic import BaseModel, EmailStr, Field


router = APIRouter(prefix="/admin", tags=["Admin"])

SECRET_KEY = "cab45e3f86839165cbd821486bc63d77964e06c72917f72a6b588a9608824b9f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        admin_username = payload.get("sub")
        if not admin_username:
            raise credentials_exception
        admin = db.query(Admin).filter(Admin.username == admin_username).first()
        if not admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
        return admin
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.JWTError as e:
        print(f"JWT Error: {str(e)}")
        raise credentials_exception

@router.post("/register")
def register_admin(admin_data: AdminCreate, db: Session = Depends(get_db)):
    existing_admin = db.query(Admin).filter((Admin.username == admin_data.username) | (Admin.email == admin_data.email)).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="Username or email already taken")
    
    # otp = generate_otp()
    # admin = Admin(
    #     username=admin_data.useraname,
    #     email=admin_data.email,
    #     password=admin_data.password,
    #     otp=otp,
    #     is_verified=False
    # )
    
     # Validate password (this is already done via Pydantic, but just to ensure)
    try:
        AdminCreate.validate_password(admin_data.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    hashed_password = get_password_hash(admin_data.password)
    admin = Admin(username=admin_data.username, email=admin_data.email, password=hashed_password)
    db.add(admin)
    db.commit()
    db.refresh(admin)

    # send_otp(admin.email, otp, "Admin Email Verification", f"Your admin OTP is :{otp}")
    return {"message": "Admin registered successfully"}

@router.post("/login")
def login_admin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.username == form_data.username).first()
    if not admin or not verify_password(form_data.password, admin.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token(data={"sub": admin.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}

@router.post("/users/add")
def create_user(user_data: UserCreate, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    hashed_password = get_password_hash(user_data.password)
    user = User(username=user_data.username, email=user_data.email, password=hashed_password)
    db.add(user)
    db.commit()
    return {"message": "User created successfully"}

@router.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    return db.query(User).all()

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
@router.get("/users/{user_id}/chats")
def get_user_chat_history(user_id: int, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    chats = db.query(Chat).filter(Chat.user_id == user_id).all()
    if not chats:
        raise HTTPException(status_code=404, detail="No chat history found for this user")
    
    return {"user_id": user_id, "chat_history": [chat.message for chat in chats]}


@router.delete("/users/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.query(Chat).filter(Chat.user_id == user_id).delete()
    db.delete(user)
    db.commit()
    return {"message": f"User {user.username} and related data deleted successfully"}

