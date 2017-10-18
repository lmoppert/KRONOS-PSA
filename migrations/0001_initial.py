# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import filer.fields.image
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        # ('filer', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='PSACart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('processed', models.BooleanField(default=False, verbose_name='Processed')),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PSACartItems',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField(default=1, verbose_name='Quantity')),
                ('cart', models.ForeignKey(related_name='psaitems', verbose_name='PSA Cart', to='psa.PSACart')),
            ],
        ),
        migrations.CreateModel(
            name='PSACategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Category')),
                ('description', models.TextField(default=b'', verbose_name='Description', blank=True)),
                ('teaser', models.TextField(default=b'', verbose_name='Teaser', blank=True)),
                ('order', models.PositiveIntegerField(default=1)),
                ('active', models.BooleanField(default=False)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='psa.PSACategory', null=True)),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='PSAProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='PSA Item')),
                ('number', models.CharField(max_length=50, verbose_name='Article Number')),
                ('description', models.TextField(default=b'', help_text=b'Use Markdown to format text. If you want to force a line break,\n        use two spaces at the end of the line.', verbose_name='Description', blank=True)),
                ('location', models.CharField(default=b'KRO', max_length=3, verbose_name='Location', choices=[(b'KRO', b'KRONOS'), (b'LEV', b'Leverkusen'), (b'NHM', b'Nordenham')])),
                ('active', models.BooleanField(default=False)),
                ('category', models.ForeignKey(verbose_name='Category', to='psa.PSACategory')),
                ('image', filer.fields.image.FilerImageField(verbose_name='Image', blank=True, to='filer.Image', null=True)),
            ],
            options={
                'ordering': ('number',),
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
            },
        ),
        migrations.CreateModel(
            name='PSAProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.CharField(default=b'KRO', max_length=3, null=True, verbose_name='Location', choices=[(b'LEV', b'Leverkusen'), (b'NHM', b'Nordenham')])),
                ('building', models.CharField(max_length=100, null=True, verbose_name='Building')),
                ('phone', models.CharField(max_length=100, null=True, verbose_name='Phone')),
                ('fax', models.CharField(max_length=100, null=True, verbose_name='FAX')),
                ('user', models.OneToOneField(verbose_name='PSAProfile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PSARequisition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Building')),
                ('building', models.CharField(max_length=100, verbose_name='Building')),
                ('phone', models.CharField(max_length=100, verbose_name='Phone')),
                ('fax', models.CharField(max_length=100, null=True, verbose_name='FAX')),
                ('number', models.CharField(max_length=100, verbose_name='Order Number')),
                ('email', models.CharField(max_length=100, null=True, verbose_name='Order Number')),
                ('location', models.CharField(default=b'KRO', max_length=3, verbose_name='Location', choices=[(b'LEV', b'Leverkusen'), (b'NHM', b'Nordenham')])),
                ('cart', models.ForeignKey(verbose_name='PSA Cart', to='psa.PSACart')),
            ],
        ),
        migrations.AddField(
            model_name='psacartitems',
            name='item',
            field=models.ForeignKey(verbose_name='PSA Item', to='psa.PSAProduct'),
        ),
    ]
