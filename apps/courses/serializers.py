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