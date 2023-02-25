# from rest_framework import serializers

# from .models import User
# from django.contrib.auth import get_user_model # If used custom user model

# User = get_user_model()


# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             password=validated_data['password'],
#         )
#         return user
#     class Meta:
#         model = User
#         # Tuple of serialized model fields (see link [2])
#         fields = ( "id", "username", 'email', "password", )