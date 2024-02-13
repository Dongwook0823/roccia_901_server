import re

from rest_framework import serializers

from django.contrib.auth import get_user_model, authenticate
from config.exceptions import InvalidFieldException, InvalidAccountException

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
                                   error_messages={"required": "이메일은 필수 입력 항목입니다.", "blank": "이메일은 비워 둘 수 없습니다."})
    username = serializers.CharField(required=True,
                                     error_messages={"required": "이름은 필수 입력 항목입니다.", "blank": "이름은 비워 둘 수 없습니다."})
    generation = serializers.CharField(required=True,
                                       error_messages={"required": "기수는 필수 입력 항목입니다.", "blank": "기수는 비워 둘 수 없습니다."})
    role = serializers.CharField(required=True,
                                 error_messages={"required": "역할은 필수 입력 항목입니다.", "blank": "역할은 비워 둘 수 없습니다."})
    workout_location = serializers.CharField(required=True,
                                             error_messages={"required": "운동 지점은 필수 입력 항목입니다.", "blank": "운동 지점은 비워 둘 수 없습니다."})
    workout_level = serializers.CharField(required=True,
                                          error_messages={"required": "운동 난이도는 필수 입력 항목입니다.", "blank": "운동 난이도는 비워 둘 수 없습니다."})
    profile_number = serializers.IntegerField(required=True,
                                              error_messages={"required": "프로필 번호는 필수 입력 항목입니다.", "blank": "프로필 번호는 비워 둘 수 없습니다."})
    password = serializers.CharField(write_only=True, required=True,
                                     error_messages={"required": "비밀번호는 필수 입력 항목입니다.", "blank": "비밀번호는 비워 둘 수 없습니다."})
    password_confirmation = serializers.CharField(write_only=True, required=True,
                                                  error_messages={"required": "비밀번호 확인은 필수 입력 항목입니다.", "blank": "비밀번호 확인은 비워 둘 수 없습니다."})

    class Meta:
        model = User
        fields = (
            'email', 'password', 'password_confirmation', 'username', 'generation', 'role',
            'workout_location', 'workout_level', 'profile_number', 'introduction'
        )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise InvalidFieldException({"message": "이미 존재하는 이메일입니다."})
        return value

    def validate_username(self, value):
        pattern = r'^[가-힣]{2,4}$'
        if not re.match(pattern, value):
            raise InvalidFieldException({"message": "이름이 정확하지 않습니다."})
        return value

    def validate(self, data):
        password = data.get("password")
        password_confirmation = data.get("password_confirmation")

        if password != password_confirmation:
            raise InvalidFieldException({"message": "비밀번호가 일치하지 않습니다."})

        if len(password) < 7:
            raise InvalidFieldException({"message": "비밀번호는 최소 7자 이상이어야 합니다."})

        if not any(char.isupper() for char in password):
            raise InvalidFieldException({"message": "비밀번호에는 최소 1개 이상의 대문자가 포함되어야 합니다."})

        if not any(char.islower() for char in password):
            raise InvalidFieldException({"message": "비밀번호에는 최소 1개 이상의 소문자가 포함되어야 합니다."})

        if not any(char.isdigit() for char in password):
            raise InvalidFieldException({"message": "비밀번호에는 최소 1개 이상의 숫자가 포함되어야 합니다."})

        special_characters = r"[~!@#$%^&*()_+{}\":;'<>?,./]"
        if not any(char in special_characters for char in password):
            raise InvalidFieldException({"message": "비밀번호에는 최소 1개 이상의 특수 문자가 포함되어야 합니다."})

        pattern = re.compile(r'[가-힣ㄱ-ㅎㅏ-ㅣ]')
        if pattern.search(password):
            raise InvalidFieldException({"message": "비밀번호에는 한글이 포함될 수 없습니다."})

        return data

    def create(self, validated_data):
        validated_data.pop("password_confirmation", None)
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True,
                                   error_messages={"required": "이메일은 필수 입력 항목입니다.", "blank": "이메일은 비워 둘 수 없습니다."})
    password = serializers.CharField(required=True,
                                     error_messages={"required": "비밀번호는 필수 입력 항목입니다.", "blank": "비밀번호는 비워 둘 수 없습니다."})

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise InvalidAccountException({"message": "등록되지 않은 이메일입니다."})
        return value

    def validate(self, data):
        user = authenticate(email=data["email"], password=data["password"])
        if user is None:
            raise InvalidFieldException({"message": "이메일 또는 비밀번호가 유효하지 않습니다."})

        data["user"] = user
        return data
