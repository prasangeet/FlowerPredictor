from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
from .predict import predict_image

@api_view(['POST'])
def predict_view(request):
    if 'file' not in request.FILES:
        return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

    image_file = request.FILES['file']
    file_path = os.path.join('/tmp', image_file.name)

    with open(file_path, 'wb+') as f:
        for chunk in image_file.chunks():
            f.write(chunk)

    result = predict_image(file_path)
    print(f"Predicted flower: {result['class']} ({result['confidence']*100:.2f}% confidence)", flush=True)

    return Response(result, status=status.HTTP_200_OK)
