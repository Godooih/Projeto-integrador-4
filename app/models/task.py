from django.db import models

class URGENCY_LEVELS(models.TextChoices):
    LOW = 'LOW', 'low' #permite múltiplas opções
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
    urgency_level = models.CharField(max_length=50,
                                     choices=URGENCY_LEVELS.choices,
                                     default=URGENCY_LEVELS.LOW)
    creator_FK = models.ForeignKey('CustomUser',
                                related_name='Task_creator_FK',
                                on_delete=models.SET_NULL,
                                null=True)
    equipments_FK = models.ManyToManyField('Equipment')
    assignees_FK = models.ManyToManyField('CustomUser')

    def __str__(self):
        return f'{self.id}-{self.name}'


class TaskStatus(models.Model):
    status = models.CharField(max_length=50,
                                     choices=STATUS.choices,
                                     default=STATUS.OPEN)
    status_date = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=300, null=True, blank=True)
    task_FK = models.ForeignKey('Task',
                                related_name='TaskStatus_task_FK',
                                on_delete=models.CASCADE)
    user_FK = models.ForeignKey('CustomUser',
                                related_name='TaskStatus_user_FK',
                                on_delete=models.SET_NULL,
                                null=True)
    
    def __str__(self):
        return f'{self.task_FK.id}-{self.status}'



class TaskStatusImage(models.Model):
    image = models.FileField(upload_to='task_images')
    task_FK = models.ForeignKey('Task',
                                related_name='TaskStatusImage_task_FK',
                                on_delete=models.CASCADE)
    

    def __str__(self):
        return f'{self.task_FK.id}-{self.id}'
