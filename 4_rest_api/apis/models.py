from django.db import models

# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)
    address = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'school'
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_school_name')
        ]

        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

class Classroom(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classrooms')
    year = models.IntegerField(default=1)
    number = models.IntegerField(default=1)
    class Meta:
        db_table = 'classroom'
        constraints = [
            models.UniqueConstraint(fields=['school', 'year', 'number'], name='unique_classroom_per_school')
        ]
        indexes = [
            models.Index(fields=['school', 'year', 'number']),
        ]

    def __str__(self):
        return f"{self.school.short_name} - ม.{self.year}/{self.number}"

class Teacher(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='M')
    classrooms = models.ManyToManyField(Classroom, related_name='teachers', blank=True)

    class Meta:
        db_table = 'teacher'
        indexes = [
            models.Index(fields=['first_name', 'last_name'])
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='M') # 👈 โจทย์ระบุ: เพศ
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='students')

    class Meta:
        db_table = 'student'
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['classroom']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
