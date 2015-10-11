from django.db import models


class List(models.Model):
    pass


class Item(models.Model):
    text = models.TextField(default='')
    to_do_list = models.ForeignKey(List, default=1)
