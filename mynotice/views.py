from mydatabase.models import Notice,UserDatas
from mynotice.serializers import NoticeSerializer
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import  IsAuthenticated

class NoticeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]

    serializer_class = NoticeSerializer
    queryset = Notice.objects.all()

    def get_queryset(self):                                            # added string
        return super().get_queryset().filter(userData=UserDatas.objects.get(id=self.request.user.id))
    def create(self, request, *args, **kwargs):
        noticedata=request.data
        
        try:
                new_notice = Notice.objects.create(
                userData=UserDatas.objects.get(id=self.request.user.id),
                notice=noticedata['notice'],
                read=noticedata['read'])
                new_notice.save()
                return Response(status=status.HTTP_201_CREATED) 
        except:
                return Response(status=status.HTTP_400_BAD_REQUEST) 
