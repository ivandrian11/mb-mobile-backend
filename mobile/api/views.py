from rest_framework import status, generics
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.filters import OrderingFilter

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from django.db import IntegrityError

import json
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login

from mobile.helpers import generate_order_id, create_transaction

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

from .serializers import (
    CategoryListSerializer,
    PromoListSerializer,
    MentorListSerializer,
    RegisterSerializer,
    CourseListSerializer,
    MaterialListSerializer,
    ChangePasswordSerializer,
    ForgetPasswordSerializer,
    OrderSerializer,
    ProjectSerializer,
)


class CategoryListView(ListAPIView):
    serializer_class = CategoryListSerializer
    queryset = Category.objects.all()
    ordering_fields = ['id']
    filter_backends = [OrderingFilter]


class PromoListView(ListAPIView):
    serializer_class = PromoListSerializer
    queryset = Promo.objects.all()


class MentorListView(ListAPIView):
    serializer_class = MentorListSerializer
    queryset = Mentor.objects.all()


class CourseListView(ListAPIView):
    serializer_class = CourseListSerializer
    queryset = Course.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['created_at']
    filterset_fields = ['category']


class MaterialListView(ListAPIView):
    serializer_class = MaterialListSerializer
    queryset = Material.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['id']
    filterset_fields = ['course']


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()


# @permission_classes([AllowAny])
@api_view(["POST"])
def register_user(request):
    try:
        data = {}
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            account.save()
            data["message"] = "user registered successfully"
            data["username"] = account.username
            data["email"] = account.email
            data["name"] = account.name
        else:
            error = []
            for i in serializer.errors:
                error.append(serializer.errors[i][0])
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        return Response(data)
    except IntegrityError as e:
        account = User.objects.get(username='')
        account.delete()
        return Response(f"{e}", status=status.HTTP_400_BAD_REQUEST)

    except KeyError as e:
        return Response(f"Field {e} missing", status=status.HTTP_400_BAD_REQUEST)


# @permission_classes([AllowAny])
@api_view(["POST"])
def login_user(request):
    data = {}
    reqBody = json.loads(request.body)
    email = reqBody['email']
    password = reqBody['password']
    try:
        account = User.objects.get(email=email)
    except BaseException as e:
        return Response("Email doesnt exist", status=status.HTTP_401_UNAUTHORIZED)

    token = Token.objects.get_or_create(user=account)[0].key
    if not check_password(password, account.password):
        return Response("Incorrect Login credentials", status=status.HTTP_401_UNAUTHORIZED)

    if account:
        if account.is_active:
            login(request, account)
            data["message"] = "user logged in"
            data["username"] = account.username
            data["email"] = account.email
            data["name"] = account.name
            data["photoUrl"] = account.photoUrl

            res = {"data": data, "token": token}

            return Response(res)

        else:
            return Response("Account not active", status=status.HTTP_401_UNAUTHORIZED)

    else:
        return Response("Account doesnt exist", status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
def check_email(request):
    reqBody = json.loads(request.body)
    email = reqBody['email']
    try:
        account = User.objects.get(email=email)
        return Response(account.username)
    except BaseException as e:
        return Response("Email doesnt exist", status=status.HTTP_401_UNAUTHORIZED)


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer


class ForgetPasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ForgetPasswordSerializer


class OrderListApiView(ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['created_at']
    filterset_fields = ['user', 'status', 'course']


class ProjectListApiView(ListAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['user', 'course']


class ProjectView(APIView):
    # 2. Create
    def post(self, request, *args, **kwargs):
        obj = Project.objects.all()

        data = {
            'id': "P" + str(len(obj)+1).zfill(4),
            'user': request.data.get('user'),
            'course': request.data.get('course'),
            'url': request.data.get('url'),
        }

        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProjectView(APIView):
    # 4. Update
    def put(self, request, *args, **kwargs):
        instance = Project.objects.get(id=self.kwargs['project_id'])
        if not instance:
            return Response(
                {"message": "Object doesnt exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {'url': request.data.get('url')}

        serializer = ProjectSerializer(
            instance=instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderView(APIView):
    # 2. Create
    def post(self, request, *args, **kwargs):
        if (request.data.get('total') > 0):
            user_obj = User.objects.get(username=request.data.get('user'))
            course_obj = Course.objects.get(id=request.data.get('course'))
            total = request.data.get('total')
            result = create_transaction(user_obj, course_obj, total)

            data = {
                'id': result["id"],
                'user': request.data.get('user'),
                'course': request.data.get('course'),
                'status': "pending",
                'total': total,
                'url': result["url"]
            }
        else:
            data = {
                'id': generate_order_id(),
                'user': request.data.get('user'),
                'course': request.data.get('course'),
                'status': "success",
                'total': request.data.get('total'),
                'url': "-"
            }

        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateOrderView(APIView):
    # 4. Update
    def put(self, request, *args, **kwargs):
        instance = Order.objects.get(id=self.kwargs['order_id'])
        if not instance:
            return Response(
                {"message": "Object doesnt exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {'status': request.data.get('status')}

        serializer = OrderSerializer(
            instance=instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
