from rest_framework import serializers

from apis.models import School, Classroom, Teacher, Student


# === School ===

class SchoolListSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ["id", "name", "abbreviation", "address"]


class SchoolDetailSerializer(serializers.ModelSerializer):
    classroom_count = serializers.SerializerMethodField()
    teacher_count = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = [
            "id", "name", "abbreviation", "address",
            "classroom_count", "teacher_count", "student_count",
        ]

    def get_classroom_count(self, obj):
        return obj.classrooms.count()

    def get_teacher_count(self, obj):
        return Teacher.objects.filter(classrooms__school=obj).distinct().count()

    def get_student_count(self, obj):
        return Student.objects.filter(classroom__school=obj).count()


class SchoolWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ["id", "name", "abbreviation", "address"]


# === Classroom ===

class TeacherMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["id", "first_name", "last_name", "gender"]


class StudentMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "gender"]


class ClassroomListSerializer(serializers.ModelSerializer):
    school = serializers.StringRelatedField()

    class Meta:
        model = Classroom
        fields = ["id", "school", "grade", "section"]


class ClassroomDetailSerializer(serializers.ModelSerializer):
    school = SchoolListSerializer(read_only=True)
    teachers = TeacherMiniSerializer(many=True, read_only=True)
    students = StudentMiniSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = ["id", "school", "grade", "section", "teachers", "students"]


class ClassroomWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ["id", "school", "grade", "section"]


# === Teacher ===

class ClassroomMiniSerializer(serializers.ModelSerializer):
    school = serializers.StringRelatedField()

    class Meta:
        model = Classroom
        fields = ["id", "school", "grade", "section"]


class TeacherListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["id", "first_name", "last_name", "gender"]


class TeacherDetailSerializer(serializers.ModelSerializer):
    classrooms = ClassroomMiniSerializer(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = ["id", "first_name", "last_name", "gender", "classrooms"]


class TeacherWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["id", "first_name", "last_name", "gender", "classrooms"]


# === Student ===

class StudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "gender", "classroom"]


class StudentDetailSerializer(serializers.ModelSerializer):
    classroom = ClassroomMiniSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "gender", "classroom"]


class StudentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "gender", "classroom"]
