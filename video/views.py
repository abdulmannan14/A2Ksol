from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .models import Video
from .serializers import Video_serializer



class Get_videos(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        user_id = request.user.id
        try:
            videos=Video.objects.all()
            count=Video.objects.all().count()

            serializer=Video_serializer(videos,many=True).data
            return Response({'message': 'All Videos',
                             'status': status.HTTP_200_OK,
                             'count':count,
                             'data': serializer},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': e},
                            status=status.HTTP_200_OK)
