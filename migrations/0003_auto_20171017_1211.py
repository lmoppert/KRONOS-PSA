# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psa', '0002_auto_20150903_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='psacategory',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
