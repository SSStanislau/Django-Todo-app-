from datetime import datetime, date, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

TASK_PRIORITIES = (
    (0, 'Low'),
    (1, 'Normal'),
    (2, 'High')
)

TASKS_STATUSES = (
    ('DL', 'Deleted'),
    ('NW', 'New'),
    ('EXP', 'Expired'),
    ('OK', 'Completed')
)


class Category(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150,  unique=True)
    slug = models.SlugField(max_length=150)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    @classmethod
    def get_user_categories(cls, request):
        return cls.objects.filter(owner=request.user)

    def get_absolute_url(self):
        return reverse('task:category', args=[self.slug])

    def __str__(self):
        return self.name


class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    priority = models.PositiveIntegerField(choices=TASK_PRIORITIES, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    day_to_perform = models.DateField()
    status = models.CharField(choices=TASKS_STATUSES, default='NW', max_length=3)
    day_of_status_change = models.DateField(blank=True, null=True)

    @classmethod
    def get_user_tasks(cls, request):
        return cls.objects.filter(owner=request.user)

    def get_filtered_by_category_tasks(self, category):
        return super(Task, self).objects.filter(category=category)

    @classmethod
    def change_status(cls, task_id, status):
        try:
            task = cls.objects.get(id=task_id)
            task.status = status
            task.day_of_status_change = date.today()
            task.save()
        except: ObjectNotFound

    class Meta:
        ordering = ["day_to_perform"]

    def __str__(self):
        return self.title

    @classmethod
    def get_completed_tasks_per_day(cls, request):
        days = []
        count = []
        for i in range(5):
            day = date.today() - timedelta(days=i)
            c = cls.get_user_tasks(request).filter(status='OK').filter(day_of_status_change=day).count()
            days.append(day.strftime("%d/%m/%Y"))
            count.append(c)
        return days, count

    @classmethod
    def get_number_of_tasks_by_status(cls, request):
        label = ['Completed', 'Deleted', 'Expired']
        users_tasks = cls.get_user_tasks(request)
        data = []
        data.append(users_tasks.filter(status='OK').count())
        data.append(users_tasks.filter(status='DL').count())
        data.append(users_tasks.filter(status='EXP').count())
        return label, data
