from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DocumentUploadSerializer
from django.conf import settings
import os
from .tasks import process_document



class DocumentUploadView(APIView):
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
