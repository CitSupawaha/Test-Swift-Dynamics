from django.contrib import admin

from apis.models import School, Classroom, Teacher, Student


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "abbreviation")
    search_fields = ("name", "abbreviation")


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ("id", "school", "grade", "section")
    list_filter = ("school", "grade")


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "gender")
    search_fields = ("first_name", "last_name")
    list_filter = ("gender",)
    filter_horizontal = ("classrooms",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "gender", "classroom")
    search_fields = ("first_name", "last_name")
    list_filter = ("gender", "classroom")
