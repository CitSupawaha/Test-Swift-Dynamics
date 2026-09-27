from rest_framework import viewsets

from apis.models import School
from apis.serializers import SchoolListSerializer, SchoolDetailSerializer, SchoolWriteSerializer
from apis.filters import SchoolFilter


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    filterset_class = SchoolFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SchoolDetailSerializer
        if self.action in ("create", "update", "partial_update"):
            return SchoolWriteSerializer
        return SchoolListSerializer
