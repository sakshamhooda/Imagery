from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import pytesseract
from PIL import Image
import base64
import uvicorn
import io

app=FastAPI()

class BoundingBoxRequest(BaseModel):
    image: str
    type: str

@app.post("/get-text")
async def get_text(file: UploadFile = File(...)):
    try:
        image = Image.open(file.file)
        text = pytesseract.image_to_string(image)
        return {"text" : text}
    except Exception as e: 
        raise HTTPException(status_code=400, detail="Error processing image")
    
@app.post("/get-boxes")
async def get_bboxes(request: BoundingBoxRequest):
    try:
        image_data=base64.b64decode(request.image)
        image = Image.open(io.BytesIO(image_data))
        box_type = request.type

        if box_type not in ["word", "line", "paragraph", "block", "page"]:
            raise HTTPException(status_code=400, detail='Invalid bounding box type')
        
        boxes = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        return {"boxes" : boxes}
    except Exception as e: 
        raise HTTPException(status_code=400, detail="Error processing the image")
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0" , port=8000)
    
