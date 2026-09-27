from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from apis.models import School, Classroom, Teacher, Student


class BaseAPITest(TestCase):
    """Base test class setup client ไว้ให้ใช้"""
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=None)


class SchoolAPITest(BaseAPITest):
    
    def setUp(self):
        super().setUp()
        self.school = School.objects.create(
            name="โรงเรียนทดสอบ",
            abbreviation="ทส.",
            address="123 ถ.ทดสอบ กรุงเทพฯ",
        )

    def test_create_school(self):
        data = {"name": "โรงเรียนใหม่", "abbreviation": "ใหม่", "address": "456 กรุงเทพฯ"}
        response = self.client.post("/api/v1/schools/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(School.objects.count(), 2)

    def test_list_school(self):
        response = self.client.get("/api/v1/schools/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_school_by_name(self):
        School.objects.create(name="โรงเรียนอื่น", abbreviation="อ.", address="789")
        response = self.client.get("/api/v1/schools/", {"name": "ทดสอบ"})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "โรงเรียนทดสอบ")

    def test_detail_school(self):
        classroom = Classroom.objects.create(school=self.school, grade=1, section=1)
        teacher = Teacher.objects.create(first_name="ครู", last_name="ทดสอบ", gender="M")
        teacher.classrooms.add(classroom)
        Student.objects.create(first_name="นร.", last_name="ทดสอบ", gender="F", classroom=classroom)

        response = self.client.get(f"/api/v1/schools/{self.school.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["classroom_count"], 1)
        self.assertEqual(response.data["teacher_count"], 1)
        self.assertEqual(response.data["student_count"], 1)

    def test_update_school(self):
        data = {"name": "ชื่อใหม่", "abbreviation": "ใหม่", "address": "ที่อยู่ใหม่"}
        response = self.client.put(f"/api/v1/schools/{self.school.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.school.refresh_from_db()
        self.assertEqual(self.school.name, "ชื่อใหม่")

    def test_delete_school(self):
        response = self.client.delete(f"/api/v1/schools/{self.school.id}/")
        self.assertIn(response.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK])
        self.assertEqual(School.objects.count(), 0)


class ClassroomAPITest(BaseAPITest):
    
    def setUp(self):
        super().setUp()
        self.school = School.objects.create(name="รร.ทดสอบ", abbreviation="ทส.", address="123")
        self.classroom = Classroom.objects.create(school=self.school, grade=1, section=1)

    def test_create_classroom(self):
        data = {"school": self.school.id, "grade": 2, "section": 1}
        response = self.client.post("/api/v1/classrooms/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_filter_by_school(self):
        school2 = School.objects.create(name="รร.อื่น", abbreviation="อ.", address="456")
        Classroom.objects.create(school=school2, grade=1, section=1)
        
        response = self.client.get("/api/v1/classrooms/", {"school": self.school.id})
        self.assertEqual(len(response.data), 1)

    def test_detail_classroom(self):
        teacher = Teacher.objects.create(first_name="ครู", last_name="A", gender="M")
        teacher.classrooms.add(self.classroom)
        Student.objects.create(first_name="นร.", last_name="B", gender="F", classroom=self.classroom)

        response = self.client.get(f"/api/v1/classrooms/{self.classroom.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["teachers"]), 1)
        self.assertEqual(len(response.data["students"]), 1)


class TeacherAPITest(BaseAPITest):
    
    def setUp(self):
        super().setUp()
        self.school = School.objects.create(name="รร.ทดสอบ", abbreviation="ทส.", address="123")
        self.classroom = Classroom.objects.create(school=self.school, grade=1, section=1)
        self.teacher = Teacher.objects.create(first_name="สมชาย", last_name="ใจดี", gender="M")
        self.teacher.classrooms.add(self.classroom)

    def test_create_teacher(self):
        data = {
            "first_name": "สมหญิง",
            "last_name": "ใจดี",
            "gender": "F",
            "classrooms": [self.classroom.id],
        }
        response = self.client.post("/api/v1/teachers/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_filter_teacher_by_school(self):
        response = self.client.get("/api/v1/teachers/", {"school": self.school.id})
        self.assertEqual(len(response.data), 1)

    def test_filter_teacher_by_gender(self):
        Teacher.objects.create(first_name="หญิง", last_name="A", gender="F")
        response = self.client.get("/api/v1/teachers/", {"gender": "M"})
        self.assertEqual(len(response.data), 1)

    def test_detail_teacher(self):
        response = self.client.get(f"/api/v1/teachers/{self.teacher.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["classrooms"]), 1)


class StudentAPITest(BaseAPITest):
    
    def setUp(self):
        super().setUp()
        self.school = School.objects.create(name="รร.ทดสอบ", abbreviation="ทส.", address="123")
        self.classroom = Classroom.objects.create(school=self.school, grade=1, section=1)
        self.student = Student.objects.create(
            first_name="นักเรียน", last_name="ทดสอบ", gender="M", classroom=self.classroom
        )

    def test_create_student(self):
        data = {
            "first_name": "นักเรียนใหม่",
            "last_name": "A",
            "gender": "F",
            "classroom": self.classroom.id,
        }
        response = self.client.post("/api/v1/students/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_filter_student_by_school(self):
        response = self.client.get("/api/v1/students/", {"school": self.school.id})
        self.assertEqual(len(response.data), 1)

    def test_detail_student(self):
        response = self.client.get(f"/api/v1/students/{self.student.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("classroom", response.data)
        self.assertEqual(response.data["classroom"]["id"], self.classroom.id)
