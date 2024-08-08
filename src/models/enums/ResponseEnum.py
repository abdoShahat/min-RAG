from enum import Enum

class ResponseSignal(Enum):
    
    File_Type_Not_Support = "File_Type_Not_Support"
    File_size_Exceeded = "File_size_Exceeded"
    File_Upload_Sucess = "File_Upload_Sucess" 
    File_Upload_Failed = "File_Upload_Failed" 
    