

from flask import Blueprint, request, jsonify, Response

from app.services.video_service import VideoService
from werkzeug.utils import secure_filename
import io

video_bp = Blueprint('video', __name__)

@video_bp.route('/upload-video', methods=['POST'])


def upload_video():
    """

    Subir video (sin autenticación)
    ---
    tags:
      - Videos
    consumes:
      - multipart/form-data
    parameters:
      - in: formData
        name: video
        type: file
        required: true
        description: Archivo de video a subir
      - in: formData
        name: title
        type: string
        description: Título del video
      - in: formData
        name: description
        type: string
        description: Descripción del video


      - in: formData
        name: username
        type: string
        description: Nombre del usuario que sube el video
    responses:
      200:
        description: Video subido exitosamente













    """
    try:

        if 'video' not in request.files:
            return jsonify({
                "message": "No video file provided",
                "status_code": 400
            }), 400
        
        file = request.files['video']
        if file.filename == '':
            return jsonify({
                "message": "No file selected",
                "status_code": 400
            }), 400
        




     
        title = request.form.get('title', file.filename)
        description = request.form.get('description', '')
        username = request.form.get('username', 'anonymous')
        
        metadata = {
            'title': title,
            'description': description,


            'uploaded_by': username,
        }
        

        service = VideoService()
        file_id, message = service.upload_video(file, file.filename, metadata)
        
        if file_id:
            return jsonify({
                "message": message,
                "file_id": file_id,
                "status_code": 200
            }), 200
        else:
            return jsonify({
                "message": message,
                "status_code": 400
            }), 400
            
    except Exception as e:
        return jsonify({
            "message": f"Error uploading video: {str(e)}",
            "status_code": 500
        }), 500

@video_bp.route('/videos', methods=['GET'])


def list_videos():
    """

    Listar videos (sin autenticación)
    ---
    tags:
      - Videos
    parameters:
      - in: query
        name: limit
        type: integer
        default: 10

      - in: query
        name: skip
        type: integer
        default: 0



    responses:
      200:
        description: Lista de videos











    """
    try:
        limit = int(request.args.get('limit', 10))
        skip = int(request.args.get('skip', 0))
        
        service = VideoService()
        videos, message = service.list_videos(limit=limit, skip=skip)
        
        return jsonify({
            "videos": videos,
            "message": message,
            "status_code": 200
        }), 200
        
    except Exception as e:
        return jsonify({
            "message": f"Error retrieving videos: {str(e)}",
            "status_code": 500
        }), 500

@video_bp.route('/video/<file_id>', methods=['GET'])


def get_video(file_id):
    """

    Descargar video (sin autenticación)
    ---
    tags:
      - Videos
    parameters:
      - in: path
        name: file_id
        type: string
        required: true



    responses:
      200:
        description: Archivo de video







    """
    try:
        service = VideoService()
        file_data, message = service.get_video(file_id)
        
        if file_data:
            return Response(
                file_data.read(),
                mimetype=file_data.metadata.get('content_type', 'video/mp4'),
                headers={
                    'Content-Disposition': f'inline; filename="{file_data.filename}"'
                }
            )
        else:
            return jsonify({
                "message": message,
                "status_code": 404
            }), 404
            
    except Exception as e:
        return jsonify({
            "message": f"Error retrieving video: {str(e)}",
            "status_code": 500
        }), 500

@video_bp.route('/video/<file_id>/info', methods=['GET'])


def get_video_info(file_id):
    """

    Obtener información del video (sin autenticación)
    ---
    tags:
      - Videos
    parameters:
      - in: path
        name: file_id
        type: string
        required: true



    responses:
      200:
        description: Información del video









    """
    try:
        service = VideoService()
        video_info, message = service.get_video_info(file_id)
        
        if video_info:
            return jsonify({
                "video_info": video_info,
                "message": message,
                "status_code": 200
            }), 200
        else:
            return jsonify({
                "message": message,
                "status_code": 404
            }), 404
            
    except Exception as e:
        return jsonify({
            "message": f"Error retrieving video info: {str(e)}",
            "status_code": 500
        }), 500

@video_bp.route('/video/<file_id>', methods=['DELETE'])


def delete_video(file_id):
    """

    Eliminar video (sin autenticación)
    ---
    tags:
      - Videos
    parameters:
      - in: path
        name: file_id
        type: string
        required: true



    responses:
      200:
        description: Video eliminado exitosamente


    """
    try:
        service = VideoService()
        success, message = service.delete_video(file_id)
        
        if success:
            return jsonify({
                "message": message,
                "status_code": 200
            }), 200
        else:
            return jsonify({
                "message": message,
                "status_code": 404
            }), 404
            
    except Exception as e:
        return jsonify({
            "message": f"Error deleting video: {str(e)}",
            "status_code": 500
        }), 500