from django.db import models
from django.utils.translation import gettext
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class MyAccountManager(BaseUserManager):
    def create_user(self, email, name=None, username=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            name=name,
            # photoUrl=photoUrl,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
        )
        user.is_superuser = True
        user.save(using=self._db)

class User(AbstractBaseUser):
    username = models.CharField(primary_key=True, max_length=16, unique=True)
    email = models.EmailField(max_length=32, unique=True)
    name = models.TextField(null=True)
    photoUrl = models.TextField(
        null=True,
        default="https://lh3.googleusercontent.com/drive-viewer/AJc5JmSvH1nyYwDdbjl693wDu--xM8gZ7GB3O_lc47RmZNAe-JbZqNT-C2-ePtQzMIAzA9fty0bBvHs=w1366-h625")
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyAccountManager()

    class Meta:
        db_table = "user"

    def __str__(self):
        return str(self.username)

    @property
    def is_staff(self): return self.is_superuser

    def has_perm(self, perm, obj=None): return self.is_superuser

    def has_module_perms(self, app_label): return self.is_superuser

class Category(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    name = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name = gettext('category')
        verbose_name_plural = gettext('categories')

class Promo(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    description = models.TextField()
    discount = models.PositiveIntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'promo'

class Mentor(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    name = models.TextField()
    job = models.TextField(null=True)
    photoUrl = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'mentor'

class Course(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    mentor = models.ForeignKey(Mentor, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    name = models.TextField()
    description = models.TextField()
    photoUrl = models.TextField()
    price = models.PositiveIntegerField()
    project_instruction = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'course'

class Order(models.Model):
    id = models.CharField(primary_key=True, max_length=16)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=12)
    total = models.PositiveIntegerField()
    url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'order'

class Material(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    title = models.TextField()
    body = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'material'

class Project(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    url = models.TextField(null=True)
    feedback = models.TextField(null=True)
    score = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'project'
