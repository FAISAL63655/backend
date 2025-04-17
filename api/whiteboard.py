from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import WhiteboardDrawing
from .serializers import WhiteboardDrawingSerializer

@api_view(['GET', 'POST'])
def whiteboard_drawings_list(request):
    """
    List all whiteboard drawings or create a new one
    """
    if request.method == 'GET':
        drawings = WhiteboardDrawing.objects.all()
        serializer = WhiteboardDrawingSerializer(drawings, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = WhiteboardDrawingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def whiteboard_drawing_detail(request, pk):
    """
    Retrieve, update or delete a whiteboard drawing
    """
    try:
        drawing = WhiteboardDrawing.objects.get(pk=pk)
    except WhiteboardDrawing.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = WhiteboardDrawingSerializer(drawing)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = WhiteboardDrawingSerializer(drawing, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        drawing.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
