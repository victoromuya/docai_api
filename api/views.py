from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from .serializers import DocumentUploadSerializer
from django.conf import settings
import os
from .tasks import process_document
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class DocumentUploadView(APIView):
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="Upload a document file (PDF, image, text) for AI processing and analysis",
        consumes=['multipart/form-data'],
        request_body=DocumentUploadSerializer,
        responses={
            202: openapi.Response("Document processing started", openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING),
                'document_type': openapi.Schema(type=openapi.TYPE_STRING),
                'text': openapi.Schema(type=openapi.TYPE_STRING),
            })),
            400: "Validation error"
        }
    )
    def post(self, request):
        print(request.FILES)
        serializer = DocumentUploadSerializer(data=request.data)
        if serializer.is_valid():
            file_obj = serializer.validated_data['file']

            
            # Save uploaded file
            file_path = os.path.join(settings.MEDIA_ROOT, file_obj.name)
            with open(file_path, 'wb+') as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)

            # Trigger async processing
            task = process_document(file_path)
            print(task)

            return Response({
                "message": "Document is being processed",
                "document_type": task.get("document_type"),
                # "confidence": task.get("confidence"),
                # "entities": task.get("entities"),
                "text": task.get("text"),   
            }, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
