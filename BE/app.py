from fastapi import FastAPI
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from naive_bayes import predict as nb_predict, summarize_by_class, load_csv, str_column_to_float, str_column_to_int
from pydantic import BaseModel

# Load dataset và train model
dataset = load_csv("diabetes.csv")
for i in range(len(dataset[0]) - 1):
    str_column_to_float(dataset, i)
str_column_to_int(dataset, len(dataset[0]) - 1)
model = summarize_by_class(dataset)

# FastAPI setup
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["Diabetes"]
collection = db["patient"]

# Định nghĩa cấu trúc dữ liệu đầu vào
class PredictionInput(BaseModel):
    pregnancy: float
    glucose: float
    blood_pressure: float
    skin_thickness: float
    insulin: float
    bmi: float
    diabetes_pedigree_function: float
    age: float

@app.post("/predict")
async def predict(data: PredictionInput):
    try:
        # Convert input thành danh sách
        convertData = [
            data.pregnancy,
            data.glucose,
            data.blood_pressure,
            data.skin_thickness,
            data.insulin,
            data.bmi,
            data.diabetes_pedigree_function,
            data.age
        ]
        
        # Dự đoán (thay bằng hàm Naive Bayes của bạn)
        result = nb_predict(model, convertData)

        # Lưu kết quả vào MongoDB (tùy chọn)
        data_dict = data.dict()
        data_dict["result"] = result
        collection.insert_one(data_dict)

        return {"prediction": result, "status": "success"}
    except Exception as e:
        return {"message": str(e), "status": "error"}

@app.get("/patients")
async def get_all_patients():
    patients = list(collection.find())
    for patient in patients:
        patient["_id"] = str(patient["_id"])
    return {"patients": patients}
