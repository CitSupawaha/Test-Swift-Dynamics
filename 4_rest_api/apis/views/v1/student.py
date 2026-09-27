from rest_framework import viewsets

from apis.models import Student
from apis.serializers import StudentListSerializer, StudentDetailSerializer, StudentWriteSerializer
from apis.filters import StudentFilter


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related("classroom", "classroom__school").all()
    filterset_class = StudentFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return StudentDetailSerializer
        if self.action in ("create", "update", "partial_update"):
            return StudentWriteSerializer
        return StudentListSerializer
