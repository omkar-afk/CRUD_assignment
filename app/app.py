from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

# MongoDB connection
MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.users_db
users = database.get_collection("users_collection")


class User(BaseModel):
    name: str
    email: str

class UpdateUser(BaseModel):
    name: str = None
    email: str = None


def userHelper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
    }


@app.post("/user")
async def create_user(user: User):
    user_exist = await users.find_one(user.dict());
    if user_exist is not None:
        raise HTTPException(status_code=400, detail="User already registered")
    user = await users.insert_one(user.dict())
    newUser = await users.find_one({"_id": user.inserted_id})
    return userHelper(newUser)


@app.get("/user/{id}")
async def get_user(id: str):
    user = await users.find_one({"_id": ObjectId(id)})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return userHelper(user)


@app.get("/users")
async def listUsers():
    userss = []
    async for user in users.find():
        userss.append(userHelper(user))
    return userss


@app.put("/user/{id}")
async def update_user(id: str, user: UpdateUser):
    user_exist = await users.find_one({"_id": ObjectId(id)})
    if user_exist is None:
        raise HTTPException(status_code=400, detail="User not found")
    await users.update_one({"_id": ObjectId(id)}, {"$set": user.dict()})
    return {"message": "User updated successfully"}
    
@app.get("/")
async def home():
    return {"message": "Welcome to FastAPI with MongoDB"}

@app.delete("/user/{id}")
async def delete_user(id: str):
    delete_result = await users.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found") 