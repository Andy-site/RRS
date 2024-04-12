from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class TableManager(models.Manager):
    pass


class OrderManager(models.Manager):
    pass


class FoodManager(models.Manager):
    pass


class StaffAdminManager(models.Manager):
    pass


class Order(models.Model):
    username = models.CharField(max_length=150, default=None)
    date = models.DateField()
    time = models.TimeField()
    number_of_people = models.IntegerField()
    message = models.TextField()
    confirmed = models.BooleanField(default=False)  # New field
    completed = models.BooleanField(default=False)  # New field

    objects = OrderManager()


class Food(models.Model):
    type = models.CharField(default=None)
    food = models.CharField()
    price = models.IntegerField()

    objects = FoodManager()


class RevManager(models.Manager):
    def create_user(self, username, text=None, **extra_fields):
        if not username:
            raise ValueError('The username must be set')

        user = self.model(username=username, text=text, **extra_fields)
        user.save(using=self._db)
        return user

    pass


class Table(models.Model):
    id = models.AutoField(primary_key=True)  # Add this line
    date = models.DateField()
    size = models.IntegerField()
    number = models.IntegerField(default=0)
    reserved = models.BooleanField(default=False)

    objects = TableManager()


class Rev(models.Model):
    # id = models.AutoField(primary_key=True)  # Add this line
    username = models.CharField(max_length=150, unique=True)
    text = models.CharField(max_length=300, unique=True)

    objects = RevManager()


class MyUserManager(BaseUserManager):
    def create_user(self, username, email=None, phone=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The username must be set')

        # Normalize the email address if provided
        if email:
            email = self.normalize_email(email)

        user = self.model(username=username, email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, phone=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        return self.create_user(username, email, phone, password, **extra_fields)


class MyUser123(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff


class Staff(models.Model):
    objects = StaffAdminManager()
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
