from rest_framework import serializers

from mobile.models import (
    Category,
    Promo,
    Mentor,
    User,
    Course,
    Material,
    Order,
    Project,
)


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)


class PromoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = ('id', 'description', 'discount', 'available')


class MentorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = ('id', 'name', 'job', 'photoUrl')


class CourseListSerializer(serializers.ModelSerializer):
    mentor = MentorListSerializer()
    category = CategoryListSerializer()

    class Meta:
        model = Course
        fields = [
            "id",
            "mentor",
            "category",
            "name",
            "description",
            "photoUrl",
            "price",
            "project_instruction",
            "created_at",
            "updated_at",
            "available"
        ]


class MaterialListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('id', 'course', 'title', 'body')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "name",
            "photoUrl",

        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        account = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['name'],
        )
        account.set_password(validated_data['password'])
        account.save()
        return account


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"message": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = User.objects.get(
            username=self.context.get('request').parser_context.get('kwargs').get('pk'))
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"message": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class ForgetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"message": "Password fields didn't match."})

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id", "user", "course", "status", "total",
            "url", "created_at", "updated_at",
        ]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id", "course", "user", "url", "feedback", "score",
            "created_at", "updated_at"
        ]