from django.db import models, transaction

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group, Permission
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

import logging
logger = logging.getLogger(__name__)

# Login and user setup
class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError('A valid Email must be provided')

        # Ensuring the default for is_active is True unless specified
        extra_fields.setdefault('is_active', True)

        with transaction.atomic():
            user = self.model(email=self.normalize_email(email), **extra_fields)
            user.set_password(password)
            user.save(using=self._db)

            # Example of a post-creation action
            # send_welcome_email(user)

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# Creation of ENUM for industry
class Industry(models.TextChoices):
    IB = 'IB', 'Investment Banking'
    ST = 'ST', 'Sales & Trading'
    BS = 'BS', 'Buy-Side'
    NA = 'NA', 'Non Chosen'

class Account(AbstractBaseUser, PermissionsMixin):
    objects = AccountManager()
    
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255) # max_length must be there, or else error
    last_name = models.CharField(max_length=255)
    industry_interest = models.CharField(
        max_length=2,
        choices=Industry.choices,
        default=Industry.NA
    )
    school = models.TextField(null=True) # PLACEHOLDER TYPE
    school_startdate = models.TextField(null=True) # PLACEHOLDER TYPE
    associated_client = models.TextField(null=True) # PLACEHOLDER TYPE


    is_interviewer = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True) # ============================= TO BE REMOVED
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username' # must be the main reference when accessing this database
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email'] # Added for CustomUserModel definition

    # Modify the groups and user_permissions fields with unique related names
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="custom_user_groups", # This is the most important, if not defined, clashes with Django OG name
        related_query_name="user",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_permissions", # This is the most important, if not defined, clashes with Django OG name
        related_query_name="user",
    )

