from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.core.validators import MinLengthValidator

# Create your models here.
GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Others'),
)
STATUS_CHOICES=(
    ('A', 'Available'),
    ('W', 'Away'),
    ('O', 'Occupied'),
)
PATIENT_CHOICES=(
    ('N', 'New Patient'),
    ('E', 'Existing Patient'),
)
class UserAccountManager(BaseUserManager):
   
    # patients
    def create_user(self,dob,gender,primary_contact,alternate_contact,email,user_id, firstname,lastname,address, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        # formatting text after @
        email = self.normalize_email(email)
        # formatting text before @
        email = email.lower()
        user = self.model(
            email=email,
            firstname=firstname,
            lastname= lastname, 
            dob =dob,
            user_id=user_id,
            gender = gender,
            primary_contact=primary_contact,
            alternate_contact=alternate_contact,
            address=address,
        )
        # hashed pswd
        user.set_password(password)
        user.save(using=self._db)
        return user

    # assistant doctor
    def create_as_doc(self, dob,gender,primary_contact,alternate_contact,email,user_id, firstname,lastname,address,password=None):
        user = self.create_user(
            email=email, 
            firstname=firstname,
            lastname= lastname, 
            password = password,
            dob = dob,
            user_id=user_id,
            primary_contact=primary_contact,
            alternate_contact=alternate_contact,
            gender=gender,
            address=address,
        )

        # assistant doctor marker
        user.is_as_doc = True
        user.is_admin_doc = False
        user.save(using=self._db)
        return user

    # admin doctor
    def create_admin_doc(self, dob,gender,primary_contact,alternate_contact,email,user_id, firstname,lastname,address, password=None):
        user = self.create_user(
            email=email, 
            firstname=firstname,
            lastname= lastname,  
            password = password,
            dob = dob,
            user_id=user_id,
            primary_contact=primary_contact,
            alternate_contact=alternate_contact,
            address=address,
            gender=gender)

        # admin doctor marker
        user.is_admin_doc = True
        # is_as_doc = False
        user.save(using=self._db)
        return user
    
    # super user
    # setting up default values esp. for superadmin
    def create_superuser(self,email, firstname,lastname,user_id='000',dob = '1599-01-01',gender = 'O',primary_contact = '0000000000',alternate_contact = '0000000000',address="",password=None):
        user = self.create_user(
            email=email, 
            firstname=firstname,
            lastname= lastname, 
            password=password,
            user_id=user_id,
            dob = '1599-01-01',
            gender = 'O',
            primary_contact = '0000000000',
            alternate_contact = '0000000000',
            address=address,
            )
        user.is_superuser = True
        user.is_admin_doc = True
        user.is_staff = True
        user.save(using=self._db)
        return user

# customized user fields
class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    firstname = models.CharField(max_length=255)
    lastname= models.CharField(max_length=255,null=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,null=True,blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser =  models.BooleanField(default=False)
    # doctor tag
    is_as_doc = models.BooleanField(default=False)
    is_admin_doc = models.BooleanField(default=False)
    # custom user fields
    user_id = models.CharField(max_length=10)
    dob = models.DateField(auto_now=False, auto_now_add=False,null=True);
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,null=True)
    primary_contact = models.CharField(max_length=10,validators=[MinLengthValidator(10)],null=True)
    alternate_contact = models.CharField(null=True,blank=True,max_length=10,validators=[MinLengthValidator(10)])
    date_joined = models.DateField(auto_now_add=True)
    address = models.TextField(blank=True,null=True)
    patient_type = models.CharField(max_length=1,choices=PATIENT_CHOICES,null=True,blank=True)
    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname','lastname']

    def __str__(self):
        return self.email
