from rest_framework import viewsets

from apis.models import Teacher
from apis.serializers import TeacherListSerializer, TeacherDetailSerializer, TeacherWriteSerializer
from apis.filters import TeacherFilter


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.prefetch_related("classrooms", "classrooms__school").all()
    filterset_class = TeacherFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TeacherDetailSerializer
        if self.action in ("create", "update", "partial_update"):
            return TeacherWriteSerializer
        return TeacherListSerializer
