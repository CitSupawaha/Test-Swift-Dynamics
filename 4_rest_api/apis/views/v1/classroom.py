from rest_framework import viewsets

from apis.models import Classroom
from apis.serializers import ClassroomListSerializer, ClassroomDetailSerializer, ClassroomWriteSerializer
from apis.filters import ClassroomFilter


class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.select_related("school").prefetch_related(
        "teachers", "students",
    ).all()
    filterset_class = ClassroomFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ClassroomDetailSerializer
        if self.action in ("create", "update", "partial_update"):
            return ClassroomWriteSerializer
        return ClassroomListSerializer
