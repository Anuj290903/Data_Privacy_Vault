from django.db import models

class ID(models.Model):
    data_id = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.data_id

class myData(models.Model):
    key = models.CharField(max_length=100, primary_key=True)
    value = models.CharField(max_length=255)
    id = models.ForeignKey(ID, on_delete=models.CASCADE, related_name='dataId')
    field = models.CharField(max_length=100)