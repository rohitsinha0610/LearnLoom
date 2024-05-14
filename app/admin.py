from django.contrib import admin
from .models import Classroom, Enrollment, Assignment, Submission, Grade, Comment, Announcement, ReportCard

# Define admin classes for each model

class ClassroomAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Classroom._meta.fields]  # Display all fields in list view

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Enrollment._meta.fields]  # Display all fields in list view

class AssignmentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Assignment._meta.fields]  # Display all fields in list view

class SubmissionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Submission._meta.fields]  # Display all fields in list view

class GradeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Grade._meta.fields]  # Display all fields in list view

class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.fields]  # Display all fields in list view

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Announcement._meta.fields]  # Display all fields in list view

class ReportCardAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ReportCard._meta.fields]  # Display all fields in list view

# Register each model with its corresponding admin class

admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(ReportCard, ReportCardAdmin)
