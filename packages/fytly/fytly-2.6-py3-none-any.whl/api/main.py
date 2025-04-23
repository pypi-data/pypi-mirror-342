from fastapi import FastAPI, UploadFile, File, HTTPException,Body,Form

from fastapi.middleware.cors import CORSMiddleware
from scorer.component import GraderComponent
from io import BytesIO
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/validatecsv")
async def read_input_payload(file: UploadFile = File(...),role_code:str=Form(...)):
    try:
        print(role_code)
        contents = await file.read()
        result =GraderComponent().read_input_payload(BytesIO(contents), file.filename,role_code)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error grading file: {str(e)}")


