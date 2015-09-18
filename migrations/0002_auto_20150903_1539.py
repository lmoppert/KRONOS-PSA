# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('psa', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='psaproduct',
            name='description',
            field=models.TextField(default=b'', help_text=b'Use Markdown to format text. Additionally, Place "**Achtung!**" on\n    one line and this line an all following lines until the first empty line\n    will be marked red. If you want to force a line break, use two spaces at the\n    end of the line.', verbose_name='Description', blank=True),
        ),
    ]
