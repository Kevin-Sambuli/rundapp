from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, username, first_name, last_name, gender, dob,
                    kra_pin, id_no, phone, password):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a Users must have a first name')
        if not gender:
            raise ValueError('Users must select his/her gender')
        if not kra_pin:
            raise ValueError('Users must have a KRA PIN')
        if not id_no:
            raise ValueError('Users must have National Identity Number')
        if not phone:
            raise ValueError('Users must have a working telephone number')
        if not dob:
            raise ValueError('Users must provide his/her age')

        user = self.model(
            email=self.normalize_email(email), username=username, first_name=first_name,
            last_name=last_name, gender=gender, dob=dob, kra_pin=kra_pin, id_no=id_no, phone=phone
            )

        # password=self.make_random_password(length=10,
        #                       allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'),
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, gender, kra_pin, dob,
                         id_no, phone, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            dob=dob,
            kra_pin=kra_pin,
            id_no=id_no,
            phone=phone,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    MALE = 'm'
    FEMALE = 'f'
    GENDER = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]
    first_name = models.CharField('First Name', max_length=30)
    last_name = models.CharField('Last Name', max_length=30)
    email = models.EmailField(verbose_name='Email', blank=False, max_length=100, unique=True)
    username = models.CharField('Username', max_length=30, unique=True)
    gender = models.CharField('Gender', max_length=1, choices=GENDER, default=MALE)
    kra_pin = models.CharField('KRA PIN', max_length=20, unique=True, blank=False)
    id_no = models.CharField('ID NO', max_length=10, unique=True, blank=False)
    dob = models.DateField('Date of Birth', blank=False)
    phone = models.CharField('Contact Phone', max_length=10, blank=False)
    date_joined = models.DateTimeField('Date Joined', auto_now_add=True)

    # permissions
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField('admin', default=False)
    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('staff', default=False)
    is_superuser = models.BooleanField('superuser', default=False)

    # unique parameter that will be used to login in the user
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'gender', 'kra_pin', 'id_no',
                       'dob', 'phone']

    # hooking the New customized Manager to our Model
    objects = UserManager()

    class Meta:
        db_table = 'accounts'
        verbose_name = "accounts"
        verbose_name_plural = "accounts"

    # def __str__(self):
    #     return self.username.title()

    def __str__(self):
        return '{}'.format(self.get_full_name())  # ,self.email)

    def get_full_name(self):
        """ Returns the first_name plus the last_name, with a space in between. """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    # For checking permissions. to keep it simple all admin have ALL permissions
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

    @property
    def full_name(self):
        """Returns the person's full name. """
        return '%s %s' % (self.first_name, self.last_name)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Sends an email to this User. """
        send_mail(subject, message, from_email, [self.email], **kwargs)

        # sending email
        # message = "your message here"
        # subject = "your subject here"
        # send_mail(subject, message, from_email, ['to_email', ])
        # password = rand_string
        # send_mail('Subject here', 'Here is the password: .' + password,
        #           'from@example.com', ['someone@gmail.com'],
        #           fail_silently=False)


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
#
#
# @receiver(post_save, sender=Account)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Account.objects.create(user=instance)
#
#
# @receiver(post_save, sender=Account)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
