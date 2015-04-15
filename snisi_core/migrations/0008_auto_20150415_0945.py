# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import snisi_core.models.Providers


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_core', '0006_entitytype_short_name'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='provider',
            managers=[
                (b'objects', snisi_core.models.Providers.ProviderManager()),
            ],
        ),
        migrations.AlterField(
            model_name='expectedreporting',
            name='arrived_reports',
            field=models.ManyToManyField(related_name='expected_reportings', to='snisi_core.SNISIReport', blank=True),
        ),
        migrations.AlterField(
            model_name='expectedvalidation',
            name='report',
            field=models.OneToOneField(related_name='expected_validations', primary_key=True, serialize=False, to='snisi_core.SNISIReport'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='destination_email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='provider',
            name='email',
            field=models.EmailField(max_length=254, null=True, verbose_name='email address', blank=True),
        ),
        migrations.AlterField(
            model_name='provider',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='last_login',
            field=models.DateTimeField(null=True, verbose_name='last login', blank=True),
        ),
    ]
