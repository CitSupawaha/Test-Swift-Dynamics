from django.db import models


class School(models.Model):
    name = models.CharField(max_length=255, verbose_name="ชื่อโรงเรียน")
    abbreviation = models.CharField(max_length=50, verbose_name="ตัวย่อชื่อโรงเรียน")
    address = models.TextField(verbose_name="ที่อยู่")

    class Meta:
        verbose_name = "โรงเรียน"
        verbose_name_plural = "โรงเรียน"

    def __str__(self):
        return self.name


class Classroom(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="classrooms",
    )
    grade = models.IntegerField(verbose_name="ชั้นปี")
    section = models.IntegerField(verbose_name="ทับ")

    class Meta:
        verbose_name = "ห้องเรียน"
        verbose_name_plural = "ห้องเรียน"
        unique_together = ("school", "grade", "section")

    def __str__(self):
        return f"{self.school.abbreviation} ป.{self.grade}/{self.section}"


class Teacher(models.Model):

    class Gender(models.TextChoices):
        MALE = "M", "ชาย"
        FEMALE = "F", "หญิง"

    first_name = models.CharField(max_length=255, verbose_name="ชื่อ")
    last_name = models.CharField(max_length=255, verbose_name="นามสกุล")
    gender = models.CharField(max_length=1, choices=Gender.choices, verbose_name="เพศ")
    classrooms = models.ManyToManyField(
        Classroom,
        related_name="teachers",
        blank=True,
    )

    class Meta:
        verbose_name = "ครู"
        verbose_name_plural = "ครู"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):

    class Gender(models.TextChoices):
        MALE = "M", "ชาย"
        FEMALE = "F", "หญิง"

    first_name = models.CharField(max_length=255, verbose_name="ชื่อ")
    last_name = models.CharField(max_length=255, verbose_name="นามสกุล")
    gender = models.CharField(max_length=1, choices=Gender.choices, verbose_name="เพศ")
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
    )

    class Meta:
        verbose_name = "นักเรียน"
        verbose_name_plural = "นักเรียน"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
