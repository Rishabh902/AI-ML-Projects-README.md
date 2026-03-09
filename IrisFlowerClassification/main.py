from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.datasets import load_iris
from sklearn.svm import SVC

# Create FastAPI app
app = FastAPI(title="Iris Flower Classification API")

# Load dataset and train model at startup
iris = load_iris()
X = iris.data
y = iris.target

model = SVC()
model.fit(X, y)

# Request body structure
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


# Home route
@app.get("/")
def home():
    return {"message": "Iris Flower Classification API is running 🌸"}


# Prediction route
@app.post("/predict")
def predict(data: IrisInput):
    input_data = [[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]]
    
    prediction = model.predict(input_data)
    species = iris.target_names[prediction][0]
    
    return {
        "predicted_class_index": int(prediction[0]),
        "predicted_species": species
    }