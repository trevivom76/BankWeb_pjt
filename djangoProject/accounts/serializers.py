from dataclasses import fields
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from accounts.models import User

# 회원가입
class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(max_length=20, required=True)
    name = serializers.CharField(max_length=50)
    email = serializers.EmailField(required=False)
    age = serializers.IntegerField(required=False)
    money = serializers.IntegerField(required=False)
    salary = serializers.IntegerField(required=False)
    
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            'nickname': self.validated_data.get('nickname', ''),
            'name': self.validated_data.get('name', ''),
            'age': self.validated_data.get('age', 0),
            'salary': self.validated_data.get('salary', 0),
            'money': self.validated_data.get('money', 0)
        })
        return data

    def save(self, request):
        user = super().save(request)

        # 커스텀된 user 모델 수정
        user.name = self.cleaned_data.get('name')
        user.nickname = self.cleaned_data.get('nickname')
        user.age = self.cleaned_data.get('age')
        user.salary = self.cleaned_data.get('salary')
        user.money = self.cleaned_data.get('money')

        # 커스텀된 user 모델 저장
        user.save()

        return user


# 유저 프로필
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('profile_img', 'nickname', 'username', 'name', 'email', 'age', 'money', 'salary')
        read_only_fields = ('id', 'username', 'name',)


# 유저 정보
class UserInfoSerializer(serializers.ModelSerializer):
    profile_img = serializers.ImageField(use_url=True)
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id', 'username', 'name',)