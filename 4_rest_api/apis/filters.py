from django_filters import FilterSet, filters

from apis.models import School, Classroom, Teacher, Student


class SchoolFilter(FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = School
        fields = ["name"]


class ClassroomFilter(FilterSet):
    school = filters.NumberFilter(field_name="school__id")

    class Meta:
        model = Classroom
        fields = ["school"]


class TeacherFilter(FilterSet):
    school = filters.NumberFilter(field_name="classrooms__school__id", distinct=True)
    classroom = filters.NumberFilter(field_name="classrooms__id", distinct=True)
    first_name = filters.CharFilter(field_name="first_name", lookup_expr="icontains")
    last_name = filters.CharFilter(field_name="last_name", lookup_expr="icontains")
    gender = filters.CharFilter(field_name="gender")

    class Meta:
        model = Teacher
        fields = ["school", "classroom", "first_name", "last_name", "gender"]


class StudentFilter(FilterSet):
    school = filters.NumberFilter(field_name="classroom__school__id")
    classroom = filters.NumberFilter(field_name="classroom__id")
    first_name = filters.CharFilter(field_name="first_name", lookup_expr="icontains")
    last_name = filters.CharFilter(field_name="last_name", lookup_expr="icontains")
    gender = filters.CharFilter(field_name="gender")

    class Meta:
        model = Student
        fields = ["school", "classroom", "first_name", "last_name", "gender"]
