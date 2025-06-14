from gridfs import GridFS
from config.db import get_mongodb_connection
from bson import ObjectId
import os
from werkzeug.utils import secure_filename

class VideoService:
    def __init__(self):
        self.db = get_mongodb_connection()
        if self.db is not None:
            self.fs = GridFS(self.db)
        else:
            self.fs = None
    
    def upload_video(self, file, filename, metadata=None):
        """
        Sube un video a GridFS
        """
        if self.fs is None:
            return None, "Database connection failed"
        
        try:
            # Validar que sea un archivo de video
            allowed_extensions = {'mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mkv'}
            if not self._allowed_file(filename, allowed_extensions):
                return None, "File type not allowed"
            
            # Preparar metadata
            file_metadata = {
                'filename': secure_filename(filename),
                'content_type': file.content_type,
                'upload_date': None  # GridFS añade esto automáticamente
            }
            
            if metadata:
                file_metadata.update(metadata)
            
            # Subir archivo
            file_id = self.fs.put(
                file,
                filename=secure_filename(filename),
                metadata=file_metadata
            )
            
            return str(file_id), "Video uploaded successfully"
            
        except Exception as e:
            return None, f"Error uploading video: {str(e)}"
    
    def get_video(self, file_id):
        """
        Obtiene un video de GridFS
        """
        if self.fs is None:
            return None, "Database connection failed"
        
        try:
            file_data = self.fs.get(ObjectId(file_id))
            return file_data, "Video retrieved successfully"
        except Exception as e:
            return None, f"Error retrieving video: {str(e)}"
    
    def delete_video(self, file_id):
        """
        Elimina un video de GridFS
        """
        if self.fs is None:
            return False, "Database connection failed"
        
        try:
            self.fs.delete(ObjectId(file_id))
            return True, "Video deleted successfully"
        except Exception as e:
            return False, f"Error deleting video: {str(e)}"
    
    def list_videos(self, limit=10, skip=0):
        """
        Lista videos almacenados
        """
        if self.fs is None:
            return [], "Database connection failed"
        
        try:
            files = []
            for file in self.fs.find().limit(limit).skip(skip):
                files.append({
                    'id': str(file._id),
                    'filename': file.filename,
                    'upload_date': file.upload_date,
                    'length': file.length,
                    'metadata': file.metadata
                })
            return files, "Videos retrieved successfully"
        except Exception as e:
            return [], f"Error retrieving videos: {str(e)}"
    
    def get_video_info(self, file_id):
        """
        Obtiene información de un video sin descargar el contenido
        """
        if self.fs is None:
            return None, "Database connection failed"
        
        try:
            file_info = self.fs.find_one({"_id": ObjectId(file_id)})
            if file_info:
                return {
                    'id': str(file_info._id),
                    'filename': file_info.filename,
                    'upload_date': file_info.upload_date,
                    'length': file_info.length,
                    'content_type': file_info.metadata.get('content_type') if file_info.metadata else None,
                    'metadata': file_info.metadata
                }, "Video info retrieved successfully"
            else:
                return None, "Video not found"
        except Exception as e:
            return None, f"Error retrieving video info: {str(e)}"
    
    def _allowed_file(self, filename, allowed_extensions):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions