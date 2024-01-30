import re

from rest_framework import serializers

from config.exceptions import InvalidFieldException
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirmation = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = (
            'email', 'password', 'password_confirmation', 'username', 'generation', 'role',
            'workout_location', 'workout_level', 'profile_number', 'introduction'
        )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise InvalidFieldException("이미 존재하는 이메일입니다.")
        return value

    def validate_username(self, value):
        pattern = r'^[가-힣]{2,4}$'
        if not re.match(pattern, value):
            raise InvalidFieldException("이름이 정확하지 않습니다.")
        return value

    def validate(self, data):
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')

        if password != password_confirmation:
            raise InvalidFieldException({"비밀번호가 일치하지 않습니다."})

        if len(password) < 7:
            raise InvalidFieldException({"비밀번호는 최소 7자 이상이어야 합니다."})

        if not any(char.isupper() for char in password):
            raise InvalidFieldException({"비밀번호에는 최소 1개 이상의 대문자가 포함되어야 합니다."})

        if not any(char.islower() for char in password):
            raise InvalidFieldException({"비밀번호에는 최소 1개 이상의 소문자가 포함되어야 합니다."})

        if not any(char.isdigit() for char in password):
            raise InvalidFieldException({"비밀번호에는 최소 1개 이상의 숫자가 포함되어야 합니다."})

        special_characters = r"[~!@#$%^&*()_+{}\":;'<>?,./]"
        if not any(char in special_characters for char in password):
            raise InvalidFieldException({"비밀번호에는 최소 1개 이상의 특수 문자가 포함되어야 합니다."})

        pattern = re.compile(r'[가-힣ㄱ-ㅎㅏ-ㅣ]')
        if pattern.search(password):
            raise InvalidFieldException("비밀번호에는 한글이 포함될 수 없습니다.")

        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation', None)
        user = User.objects.create_user(**validated_data)
        return user