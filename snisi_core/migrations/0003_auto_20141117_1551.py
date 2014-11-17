# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_core', '0002_auto_20141031_1400'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('slug', models.SlugField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
            },
            bases=(models.Model,),
        ),
        # migrations.RemoveField(
        #     model_name='snisigroup',
        #     name='group_ptr',
        # ),
        migrations.DeleteModel(
            name='SNISIGroup',
        ),
    ]
