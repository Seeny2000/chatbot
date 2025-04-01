from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from routers import chat, admin, auth
from database import engine, Base
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
import logging

Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

# Custom validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    for error in exc.errors():
        if "email" in error["loc"]:
            return JSONResponse(
                status_code=400,
                content={"detail": "Please enter a valid email"},
            )
    return JSONResponse(
        status_code=400,
        content={"detail": "Enter valid username or password"},
    )

logging.basicConfig(level=logging.DEBUG)

app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(chat.router)

@app.get("/")
def home():
    return {"message": "FastAPI Chat App with Admin Panel"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    import traceback
    print("Unhandled Exception:", traceback.format_exc())
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error. Check logs."})