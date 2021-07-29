from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, birth_day,password=None):
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username.")  
        if not birth_day:
            raise ValueError("Users must have a Birth Day.")
        user = self.model(
            email = self.normalize_email(email),
            birth_day = birth_day,
            username = username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, username, birth_day, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username=username,
            birth_day = birth_day,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self.db)
        return user



class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30)
    birth_day = models.DateField()
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(max_length=255, null=True, blank=True, default="default.jpg")
    hide_email = models.BooleanField(default=True)
    hide_birth_day = models.BooleanField(default=True)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','birth_day']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f"profile_images/{self.pk}/"):]


class Notifications(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(blank=True, null=False, default=True)

    def __str__(self):
        return f"{self.user} : {self.title}"

