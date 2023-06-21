from django.utils.safestring import mark_safe
from django.core.validators import FileExtensionValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.db import models

from . manager import UserManager
from main.models import Stack, Cohort, Group, Company


# Create your models here.
class User(AbstractUser):
    class Gender(models.TextChoices):
        SELECT = "", "Select Gender"
        MALE = "Male", "Male"
        FEMALE = "Female", "Female"

    first_name = models.CharField(verbose_name="First Name", max_length=50, blank=False)
    last_name = models.CharField(verbose_name="Last Name", max_length=50, blank=False)
    email = models.EmailField(verbose_name="Email", max_length=255, unique=True, blank=False)
    gender = models.CharField(verbose_name="Gender", choices=Gender.choices, default=Gender.SELECT, max_length=10)
    is_manager = models.BooleanField(verbose_name="Is Manager", default=False)
    is_trainer = models.BooleanField(verbose_name="Is Trainer", default=False)
    is_trainee = models.BooleanField(verbose_name="Is Trainee", default=False)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    # update django about user model
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)



class Trainer(models.Model):
    user = models.OneToOneField(User, verbose_name="User", related_name="trainers", on_delete=models.CASCADE)
    stack = models.OneToOneField(Stack, verbose_name="Stack belonging", related_name="trainers", on_delete=models.SET_DEFAULT, default=None, blank=True, null=True)
    ssn = models.CharField(verbose_name="SSN", max_length=100, blank=True, null=True)
    profilePicture = models.ImageField(
        verbose_name="Image", 
        upload_to="images/profile/", 
        validators=[FileExtensionValidator(['png','jpg','jpeg'])],
        blank=True, null=True
    )
    phone1 = PhoneNumberField(verbose_name="Phone 1", blank=True)
    phone2 = PhoneNumberField(verbose_name="Phone 2", blank=True)
    specialization = models.CharField(verbose_name="Specializations", max_length=100, blank=True, null=True)
    locationAddress = models.CharField(verbose_name="Address", max_length=200)

    def image(self):
        return mark_safe('<img src="/../../media/%s" width="70" />' % (self.profilePicture))

    image.allow_tags = True 

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)



class Trainee(models.Model):
    class Status(models.TextChoices):
        PENDING = "Pending", "Pending"
        AWARDED = "Awarded", "Awarded"

    user = models.OneToOneField(User, verbose_name="User", related_name="trainees", on_delete=models.CASCADE)
    cohort = models.ForeignKey(Cohort, verbose_name="Cohort belonging", related_name="trainees", on_delete=models.CASCADE)
    stack = models.ForeignKey(Stack, verbose_name="Stack belonging", related_name="trainees", on_delete=models.CASCADE)
    group = models.ForeignKey(Group, verbose_name="Group belonging", related_name="trainees", on_delete=models.SET_DEFAULT, default=None, blank=True, null=True)
    git_account = models.URLField(verbose_name="Git Account Link", blank=False, null=False)
    profilePicture = models.ImageField(
        verbose_name="Image", 
        upload_to="images/profile/", 
        validators=[FileExtensionValidator(['png','jpg','jpeg'])],
        blank=True, null=True
    )
    phone1 = PhoneNumberField(verbose_name="Phone 1", blank=True)
    phone2 = PhoneNumberField(verbose_name="Phone 2", blank=True)
    cv_document = models.FileField(
        verbose_name="CV Document",
        upload_to="document/trainees/cv/",
        validators=[FileExtensionValidator(['pdf','doc'])],
        blank=True, null=True
    )
    locationAddress = models.CharField(verbose_name="Address", max_length=200)
    status = models.CharField(verbose_name="Status", choices=Status.choices, default=Status.PENDING, max_length=10)
    companyDeployed = models.ForeignKey(Company, verbose_name="Company Deployed", related_name="trainees", on_delete=models.SET_DEFAULT, default=None, blank=True, null=True)
    deployedDate = models.DateField(verbose_name="When Deployed", blank=True, null=True)

    def image(self):
        return mark_safe('<img src="/../../media/%s" width="70" />' % (self.profilePicture))
    
    image.allow_tags = True 

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)



class ProgramManager(models.Model):
    user = models.OneToOneField(User, verbose_name="User", related_name="managers", on_delete=models.CASCADE)
    ssn = models.CharField(verbose_name="SSN", max_length=100, blank=True, null=True)
    profilePicture = models.ImageField(
        verbose_name="Image", 
        upload_to="images/profile/", 
        validators=[FileExtensionValidator(['png','jpg','jpeg'])],
        blank=True, null=True
    )
    phone1 = PhoneNumberField(verbose_name="Phone 1", blank=True)
    phone2 = PhoneNumberField(verbose_name="Phone 2", blank=True)
    locationAddress = models.CharField(verbose_name="Address", max_length=200)
    
    def image(self):
        return mark_safe('<img src="/../../media/%s" width="70" />' % (self.profilePicture))
    
    image.allow_tags = True 

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)
