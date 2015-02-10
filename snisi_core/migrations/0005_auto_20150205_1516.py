# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_core', '0004_auto_20150114_1650'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accreditation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.ForeignKey(to='snisi_core.Entity')),
            ],
            options={
                'verbose_name': 'Accreditation',
                'verbose_name_plural': 'Accreditations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Privilege',
            fields=[
                ('slug', models.SlugField(serialize=False, verbose_name='Slug', primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Privilege',
                'verbose_name_plural': 'Privileges',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='accreditation',
            name='privilege',
            field=models.ForeignKey(to='snisi_core.Privilege'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='accreditation',
            name='provider',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='provider',
            name='privileges',
            field=models.ManyToManyField(to='snisi_core.Privilege', through='snisi_core.Accreditation'),
            preserve_default=True,
        ),
    ]
