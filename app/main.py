
import shutil
from fastapi import FastAPI,File,UploadFile,HTTPException,status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from config import config
from jose import JWTError,jwt
from datetime import datetime,timedelta

SECRET_CHECK = "bfhgf7ytry3qgfbqwjkfgnouqyht83ythwhbgjkrsabngijh349tyhbgjkebng"

manager = config.CertificateEntity()
app = FastAPI(
    title = "Certificate Verification",
    version = "0.0.1"
)


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



async def create_custom_token(phone_no):
    data_to_encode = phone_no.copy()

    expire = datetime.utcnow()+timedelta(minutes=30)
    data_to_encode.update({"exp":expire})

    encode_token = jwt.encode(data_to_encode,SECRET_CHECK,algorithm="HS256")
    
    return encode_token

async def verify_valid_hash(token):
    try:
        payload = jwt.decode(token,SECRET_CHECK,algorithms=["HS256"])
        phone = payload.get("phone")
        if phone is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,detail="The token is in valid please try again"
            )
        return phone
    except JWTError:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,detail="The token is in valid please try again"
            )
    

@app.post("/upload",tags=["Verification and Uplaod"])
async def upload_document(name:str,phone_no:str,certificate_upload:UploadFile = File(...)):
    filename = name+"_"+phone_no+".pdf"
    try:
        with open(filename,"wb") as f:
            shutil.copyfileobj(certificate_upload.file,f)
        manager.add_item(phone_no,filename)
        
        print(manager.get_item())
        return {
        "status":"Success",
        "mesaage":"File uploaded.Please wait for verification"
        }
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={
            "status":"Failure",
            "message":"File upload failed please try again"
        })

@app.put("/verify",tags=["Verification and Uplaod"])
async def verify_docuement(phone_no:str):
    manager.update_item(phone_no)
    token = await create_custom_token(
        {
        "phone":phone_no
    }
    )
    return {
        "status":"Document Verified",
        "message":"We have sent an token to your email.Download the certificate using the token",
        "token":token
    }

@app.get("/status",tags=["Verification and Uplaod"])
async def get_docuement_status(hash_token:str,phone_str:str):
    pathname = manager.get_path(phone_str)
    phone_no = await verify_valid_hash(hash_token)
    if phone_no == phone_str:
        return FileResponse(path="C:\\Users\\nithish\\Desktop\\certificate Backend\\{}".format(pathname),media_type="application/pdf",filename="Certificate")
    else:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,detail="The token is in valid please try again"
            )

@app.get('/get',tags =["Verification and Uplaod"])
async def get_all_data():
    return manager.get_item()