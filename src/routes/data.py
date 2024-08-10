from fastapi import FastAPI, APIRouter, Depends,UploadFile,status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController,ProjectController,ProcessController
import os 
import aiofiles
from models import ResponseSignal
import logging
from .schemes.data import ProcessRequest


logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=['API_V1','DATA']
    )

@data_router.post("/upload/{project_id}")
async def upload_data(project_id:str, file:UploadFile,
                      app_settings: Settings = Depends(get_settings)):
    

    # Validate the file properties
    is_valid,result_signal = DataController().Validate_Uploaded_File(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"Signal":result_signal.value}
                            )
    
    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path = os.path.join(
        project_dir_path,
        file.filename
                            )
    
    try:
        async with aiofiles.open(file_path,'wb') as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error While Uploading file {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"Signal":ResponseSignal.File_size_Exceeded.value}
                            )
    
    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"Signal":ResponseSignal.File_Upload_Sucess.value}
                        )

@data_router.post("/process/{project_id}")
async def process_endpoint(project_id:str, process_request:ProcessRequest):
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size

    
    process_controller = ProcessController(project_id=project_id)

    file_content = process_controller.get_file_content(file_id=file_id)

    file_chunks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size
    )

    if file_chunks is None or len(file_chunks)==0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content = {
                "Signal": ResponseSignal.PROCESSING_FAILED  
            }
        )
    
    return file_chunks