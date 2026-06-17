
from django.contrib.auth import get_user_model 
from django.contrib.auth.password_validation import validate_password 
from rest_framework import serializers 
from .models import CustomUser

User=get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        min_length=8,
        validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model=CustomUser
        fields=(
            'id','username','first_name','last_name',
            'email','password','password_confirm',
            'date_joined',
        )
        read_only_fields=('id','date_joined')
        
    def validate_email(self,value):
        email=value.strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                    "User with this email already exists."
                )

        return email
        
    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
                raise serializers.ValidationError({
                    "password": "Passwords do not match."
                })

        return attrs
        
    def create(self,validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password_confirm")
        user=User.objects.create_user(
                username=validated_data.get("username"),
                email=validated_data.get("email"),
                first_name=validated_data.get("first_name", ""),
                last_name=validated_data.get("last_name", ""),
                password=password)

        return user
        
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=(            
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "date_joined",
            )
        read_only_fields=('id','date_joined')        
        
    
    