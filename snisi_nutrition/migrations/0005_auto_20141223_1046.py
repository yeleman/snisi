# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_core', '0003_auto_20141117_1551'),
        ('snisi_nutrition', '0004_auto_20141205_1853'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpectedCaseload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('u59o6_sam', models.PositiveIntegerField()),
                ('u59_sam', models.PositiveIntegerField()),
                ('u59o6_mam', models.PositiveIntegerField()),
                ('u59_mam', models.PositiveIntegerField()),
                ('pw_mam', models.PositiveIntegerField()),
                ('u59o6_mam_80pc', models.PositiveIntegerField()),
                ('u59_mam_80pc', models.PositiveIntegerField()),
                ('u59o6_sam_80pc', models.PositiveIntegerField()),
                ('u59_sam_80pc', models.PositiveIntegerField()),
                ('pw_mam_80pc', models.PositiveIntegerField()),
                ('entity', models.ForeignKey(related_name='exp_caseloads', blank=True, to='snisi_core.Entity', null=True)),
                ('period', models.ForeignKey(related_name='exp_caseloads', blank=True, to='snisi_core.Period', null=True)),
            ],
            options={
                'verbose_name': 'Expected Caseload',
                'verbose_name_plural': 'Expected Caseloads',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='expectedcaseload',
            unique_together=set([('period', 'entity')]),
        ),
    ]
