from .BaseController import BaseController
from .ProjectController import ProjectController
import os 
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import ProcessingEnum
import logging
logger = logging.getLogger("uvicorn.error")


class ProcessController(BaseController):
    def __init__(self,project_id:str):
        super().__init__()

        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    def get_file_extension(self, file_id:str):
        return os.path.splitext(file_id)[-1]
    
    def get_file_loader(self, file_id:str):
        file_path = os.path.join(self.project_path,
                                 file_id
                                 )

        file_ext = self.get_file_extension(file_id=file_id)
        
        if file_ext == ProcessingEnum.TXT.value:
            return TextLoader(file_path, encoding="utf-8")
        
        if file_ext == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        return None
    
    def get_file_content(self,file_id:str):
        try:
            loader = self.get_file_loader(file_id=file_id)
            return loader.load()
        except Exception as e:
            print(f"Error in get_file_content {e}")
            logger.error(f"Error when load file {e}")
    def process_file_content(self,file_content:list,file_id:str,
                             chunk_size:int = 100, overlap_size:int = 20):
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=overlap_size,
                length_function = len,
            )

            file_content_texts =[
                rec.page_content
                for rec in file_content
            ] 
            file_content_metadata = [
                rec.metadata
                for rec in file_content
            ]

            chunks = text_splitter.create_documents(
                file_content_texts,
                metadatas = file_content_metadata
            ) 

            return chunks
        except Exception as e:
            print(f"Error in process_file_Content {e}")
            logger.error(f"Error when process content file {e}")