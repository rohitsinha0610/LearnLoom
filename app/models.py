from django.db import models
from django.contrib.auth.models import User
import string
import random

# Create your models here.
def generate_class_code():
    # Generate a random 6-character alphanumeric code for the class
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(6))
    return code

class Classroom(models.Model):
    class_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    subject_name = models.CharField(max_length=100)
    teacher = models.ManyToManyField(User, related_name='classes_taught')
    class_creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_classrooms')
    code = models.CharField(max_length=6, default=generate_class_code, unique=True)

    def __str__(self):
        return f"{self.class_name} - {self.code}"
    

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.username} - {self.course.class_name}"


class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_score = models.IntegerField()
    classroom = models.ForeignKey(Classroom, related_name='assignments', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name='created_assignments', on_delete=models.CASCADE)

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, related_name='submissions', on_delete=models.CASCADE)
    student = models.ForeignKey(User, related_name='submissions', on_delete=models.CASCADE)
    submission_time = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='submissions/', blank=True, null=True)

class Grade(models.Model):
    assignment = models.OneToOneField(Assignment, related_name='grade', on_delete=models.CASCADE)
    student = models.ForeignKey(User, related_name='grades', on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    feedback = models.TextField()

class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, related_name='comments', on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)


class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    classroom = models.ForeignKey(Classroom, related_name='announcements', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name='created_announcements', on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)

class ReportCard(models.Model):
    student = models.ForeignKey(User, related_name='report_cards', on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, related_name='report_cards', on_delete=models.CASCADE)
    overall_grade = models.DecimalField(max_digits=5, decimal_places=2)
    # Add more fields as needed, such as grades for specific assignments or subjects
    # For example:
    # math_grade = models.DecimalField(max_digits=5, decimal_places=2)
    # science_grade = models.DecimalField(max_digits=5, decimal_places=2)
    # english_grade = models.DecimalField(max_digits=5, decimal_places=2)
