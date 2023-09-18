import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    
# "mongodb+srv://masai:HgEImw8ajJICrTjC@cluster0.kd54o.mongodb.net/health_insurance_db"
