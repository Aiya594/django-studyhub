from rest_framework import serializers 
from .models import * 


class CourseSerializer(serializers.ModelSerializer):
    owner_name=serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model=Course
        fields=[
            'id',
            'owner_name',
            'title',
            'description',
            'difficulty',
            'created_at',
            'updated_at',
        ]
        
        read_only_fields=[
            'id',
            'owner_name',
            'created_at',
            'updated_at',
        ]
        
    def validate_title(self,title):
        title=title.strip()
        if len(title)<3:
            raise serializers.ValidationError("Title must contain at least 3 characters.")
        return title 
    
    def validate_description(self,descrip):
        descrip=descrip.strip()
        if len(descrip)<10:
            raise serializers.ValidationError("Description must contain at least 10 characters.")
        return descrip
    
    
    
class LessonSerializer(serializers.ModelSerializer):
    course_title=serializers.ReadOnlyField(source='course.title')
    
    class Meta:
        model=Lesson
        fields=[
            'id',
            'course_title',
            'title',
            'content',
            'order',
            'created_at',
            'updated_at',
        ]
        
        read_only_fields=[
            'id',
            'course_title',
            'created_at',
            'updated_at',
        ]
        
    def validate(self, attrs):
        view = self.context.get("view")
        course_id = view.kwargs.get("course_id")

        title = attrs.get("title")
        order = attrs.get("order")

        lessons = Lesson.objects.filter(course_id=course_id)

        if lessons.filter(title=title).exists():
            raise serializers.ValidationError({
            "title": "Lesson with this title already exists in this course."
        })

        if lessons.filter(order=order).exists():
            raise serializers.ValidationError({
            "order": "Lesson with this order already exists in this course."
        })

        return attrs
    
    
class EnrollmentSerializer(serializers.ModelSerializer):
    student_name=serializers.ReadOnlyField(source='student.username')
    course_title=serializers.ReadOnlyField(source='course.title')

    class Meta:
        model=Enrollment
        fields=[
            'id',
            'course_title',
            'course',
            'student',
            'student_name',
            'created_at',
        ]
        read_only_fields=[
            "id",
            "student",
            "student_name",
            "course_title",
            "created_at",
        ]
        
    def validate(self, attrs):
        request = self.context.get("request")
        user = request.user
        course = attrs.get("course")

        if course.owner == user:
            raise serializers.ValidationError({
                "course": "You cannot enroll in your own course."
            })

        if Enrollment.objects.filter(student=user, course=course).exists():
            raise serializers.ValidationError({
                "course": "You are already enrolled in this course."
            })

        return attrs
    
    