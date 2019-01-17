from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.

class Employee(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    employment_position = models.CharField(max_length=200)
    employment_start_date = models.DateTimeField(auto_now_add=False)
    salary = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    employment_photo = models.ImageField(blank=True, upload_to='images/%Y/%m/%d', help_text='150x150px', verbose_name='employment_photo')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    def __str__(self):
        return str(self.id) + ' Name: ' + self.name

    class MPTTMeta:
        order_insertion_by = ['name']
