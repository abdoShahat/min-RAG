from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignal

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576

    def Validate_Uploaded_File(self,file:UploadFile):
        
        if file.content_type not in self.app_settings.FILE_ALLOW_EXTENSIONS:
            return False, ResponseSignal.File_Type_Not_Support

        if file.size > self.app_settings.FILE_MAX_SIZE *self.size_scale :
            return False, ResponseSignal.File_size_Exceeded
        
        return True, ResponseSignal.File_Upload_Sucess