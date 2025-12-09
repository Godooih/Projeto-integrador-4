# app/models.py (ARQUIVO UNIFICADO)

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# ==================================================
# 1. USUÁRIOS (CustomUser)
# ==================================================

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, name, nif, **extra_fields):
        if None in (email, password, name, nif):
            raise ValueError("Email, Password, Name or Nif are invalid!")
        
        extra_fields.setdefault('is_active', True)
        user = self.model(email=self.normalize_email(email),
                          nif=nif,
                          name=name,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, name, nif, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, name, nif, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250, unique=True)
    nif = models.CharField(max_length=15, unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    photo = models.FileField(upload_to='user_images', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'nif']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# ==================================================
# 2. CATEGORIAS E AMBIENTES
# ==================================================

class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Environment(models.Model):
    name = models.CharField(max_length=150)
    user_FK = models.ForeignKey(CustomUser,
                                related_name='Environment_user_FK',
                                on_delete=models.SET_NULL,
                                null=True)

    def __str__(self):
        return self.name


# ==================================================
# 3. EQUIPAMENTOS
# ==================================================

class Equipment(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    creation_date = models.DateTimeField(auto_now_add=True)
    category_FK = models.ForeignKey(Category,
                                    related_name='Equipment_category_FK',
                                    on_delete=models.SET_NULL,
                                    null=True)
    environment_FK = models.ForeignKey(Environment,
                                       related_name='Equipment_environment_FK',
                                       on_delete=models.SET_NULL,
                                       null=True)

    def __str__(self):
        return f'{self.code}-{self.name}'


# ==================================================
# 4. TAREFAS (TASKS) E STATUS
# ==================================================

class URGENCY_LEVELS(models.TextChoices):
    LOW = 'LOW', 'low' 
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    EXTRA_HIGH = 'EXTRA_HIGH'

class STATUS(models.TextChoices):
    OPEN = 'OPEN'
    WAITING_ASSIGNEE = 'WAITING_ASSIGNEE'
    ONGOING = 'ONGOING'
    DONE = 'DONE'
    CLOSED = 'CLOSED'
    CANCELLED = 'CANCELLED'

class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    creation_date = models.DateTimeField(auto_now_add=True)
    suggested_date = models.DateTimeField()
    urgency_level = models.CharField(
        max_length=50,
        choices=URGENCY_LEVELS.choices,
        default=URGENCY_LEVELS.LOW
    )
    
    # Campo de imagem adicionado
    image = models.ImageField(upload_to='task_images/', null=True, blank=True)

    creator_FK = models.ForeignKey(CustomUser,
                                related_name='Task_creator_FK',
                                on_delete=models.SET_NULL,
                                null=True)
    equipments_FK = models.ManyToManyField(Equipment)
    assignees_FK = models.ManyToManyField(CustomUser)

    def __str__(self):
        return f'{self.id}-{self.name}'


class TaskStatus(models.Model):
    status = models.CharField(max_length=50,
                                choices=STATUS.choices,
                                default=STATUS.OPEN)
    status_date = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=300, null=True, blank=True)
    task_FK = models.ForeignKey(Task,
                                related_name='TaskStatus_task_FK',
                                on_delete=models.CASCADE)
    user_FK = models.ForeignKey(CustomUser,
                                related_name='TaskStatus_user_FK',
                                on_delete=models.SET_NULL,
                                null=True)
    
    def __str__(self):
        return f'{self.task_FK.id}-{self.status}'


class TaskStatusImage(models.Model):
    image = models.FileField(upload_to='task_images')
    task_FK = models.ForeignKey(Task,
                                related_name='TaskStatusImage_task_FK',
                                on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.task_FK.id}-{self.id}'


# ==================================================
# 5. NOTIFICAÇÕES
# ==================================================

class Notification(models.Model):
    text = models.CharField(max_length=500)
    task_FK = models.ForeignKey(Task,
                                related_name='Notification_task_FK',
                                on_delete=models.CASCADE)
    user_FK = models.ForeignKey(CustomUser,
                                related_name='Notification_user_FK',
                                on_delete=models.SET_NULL,
                                null=True)
    creation_date = models.DateTimeField(auto_now_add=True)    
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.task_FK.id}-{self.text}'