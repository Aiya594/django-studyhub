from django.db import models
from django.conf import settings

# Create your models here.
class Course(models.Model):
    class Level(models.TextChoices):
        BEGINNER='beginner','Beginner'
        INTERMEDIATE='intermediate','Intermediate'
        ADVANCED='advanced','Advanced'
    
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='courses')
    title=models.CharField(max_length=255)
    description=models.TextField()
    difficulty=models.CharField(max_length=20,choices=Level.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'courses'
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'title'],
                name='unique_course_title_per_owner'
            )]
        
    def __str__(self):
        return self.title
    
class Lesson(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='lessons')
    title=models.CharField(max_length=255)
    content=models.TextField()
    order=models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='lessons'
        ordering=['order']
        constraints = [
            models.UniqueConstraint(
                fields=['order','course'],
                name='unique_order_num_per_course'
            ),
            models.UniqueConstraint(
                fields=['course', 'title'],
                name='unique_lesson_title_per_course')]

    
class Enrollment(models.Model):
    student=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='enrollments')
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='enrollments')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='enrollments'
        constraints = [
            models.UniqueConstraint(
                fields=["student", "course"],
                name="unique_student_course_enrollment"
            )]

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"
    
    
"""

Assignment : {
    lesson - fk(lesson)
    title
    description
    max_score
    created_at
    updated_at
    }
Submission - {
    assignment - fk(assignment)
    student
    answer_text
    score
    feedback
    created_at
    updated_at
}
"""
