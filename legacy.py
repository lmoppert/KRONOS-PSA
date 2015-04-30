from django.db import models


class StoreCategories(models.Model):
    pid = models.IntegerField(db_column='CategoryID', primary_key=True)
    name = models.CharField(db_column='CategoryName', max_length=50)
    description = models.TextField(db_column='CategoryDescription')
    teaser = models.TextField(db_column='Message')
    archived = models.BooleanField(db_column='Archived', default=False)
    parent = models.ForeignKey('StoreCategories', db_column='ParentID')

    class Meta:
        managed = False
        db_table = 'Store_Categories'


class StoreProducts(models.Model):
    pid = models.IntegerField(db_column='ProductID', primary_key=True)
    category = models.ForeignKey('StoreCategories', db_column='CategoryID')
    number = models.CharField(db_column='ModelNumber', max_length=50)
    name = models.CharField(db_column='ModelName', max_length=50)
    description = models.TextField(db_column='Summary')
    image = models.CharField(db_column='ProductImage', max_length=500)
    archived = models.BooleanField(db_column='Archived', default=False)

    class Meta:
        managed = False
        db_table = 'Store_Products'
