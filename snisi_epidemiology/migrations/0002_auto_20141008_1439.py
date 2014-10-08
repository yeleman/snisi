# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_epidemiology', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='acute_flaccid_paralysis_case',
            field=models.IntegerField(verbose_name='Suspected AFP cases'),
        ),
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='acute_flaccid_paralysis_death',
            field=models.IntegerField(verbose_name='Suspected AFP death'),
        ),
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='acute_measles_diarrhea_case',
            field=models.IntegerField(verbose_name='Suspected Acute Measles Diarrhea cases'),
        ),
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='acute_measles_diarrhea_death',
            field=models.IntegerField(verbose_name='Suspected Acute Measles Diarrhea death'),
        ),
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='cholera_case',
            field=models.IntegerField(verbose_name='Suspected Cholera cases'),
        ),
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='cholera_death',
            field=models.IntegerField(verbose_name='Suspected Cholera death'),
        ),
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='ebola_case',
            field=models.IntegerField(verbose_name='Suspected Ebola cases'),
        ),
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='ebola_death',
            field=models.IntegerField(verbose_name='Suspected Ebola death'),
        ),
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='influenza_a_h1n1_case',
            field=models.IntegerField(verbose_name='Suspected Influenza A H1N1 cases'),
        ),
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='influenza_a_h1n1_death',
            field=models.IntegerField(verbose_name='Suspected Influenza A H1N1 death'),
        ),
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='measles_case',
            field=models.IntegerField(verbose_name='Suspected Measles cases'),
        ),
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='measles_death',
            field=models.IntegerField(verbose_name='Suspected Measles death'),
        ),
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='meningitis_case',
            field=models.IntegerField(verbose_name='Suspected Meningitis cases'),
        ),
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='meningitis_death',
            field=models.IntegerField(verbose_name='Suspected Meningitis death'),
        ),
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='neonatal_tetanus_case',
            field=models.IntegerField(verbose_name='Suspected NNT cases'),
        ),
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='neonatal_tetanus_death',
            field=models.IntegerField(verbose_name='Suspected NNT death'),
        ),
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='other_notifiable_disease_case',
            field=models.IntegerField(verbose_name='Suspected Other Notifiable Diseases cases'),
        ),
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='other_notifiable_disease_death',
            field=models.IntegerField(verbose_name='Suspected Other Notifiable Diseases death'),
        ),
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='rabies_case',
            field=models.IntegerField(verbose_name='Suspected Rabies cases'),
        ),
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='rabies_death',
            field=models.IntegerField(verbose_name='Suspected Rabies death'),
        ),
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='red_diarrhea_case',
            field=models.IntegerField(verbose_name='Suspected Red Diarrhea cases'),
        ),
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='red_diarrhea_death',
            field=models.IntegerField(verbose_name='Suspected Red Diarrhea death'),
        ),
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='yellow_fever_case',
            field=models.IntegerField(verbose_name='Suspected Yellow Fever cases'),
        ),
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='yellow_fever_death',
            field=models.IntegerField(verbose_name='Suspected Yellow Fever death'),
        ),
        migrations.AlterField(
            model_name='epidemiologyr',
            name='acute_flaccid_paralysis_case',
            field=models.IntegerField(verbose_name='Suspected AFP cases'),
        ),
        migrations.AlterField(
            model_name='epidemiologyr',
            name='acute_flaccid_paralysis_death',
            field=models.IntegerField(verbose_name='Suspected AFP death'),
        ),
        migrations.AlterField(
            model_name='epidemiologyr',
            name='acute_measles_diarrhea_case',
            field=models.IntegerField(verbose_name='Suspected Acute Measles Diarrhea cases'),
        ),
        migrations.AlterField(
            model_name='epidemiologyr',
            name='acute_measles_diarrhea_death',
            field=models.IntegerField(verbose_name='Suspected Acute Measles Diarrhea death'),
        ),
        migrations.AlterField(
            model_name='epidemiologyr',
            name='cholera_case',
            field=models.IntegerField(verbose_name='Suspected Cholera cases'),
        ),
        migrations.AlterField(
            model_name='epidemiologyr',
            name='cholera_death',
            field=models.IntegerField(verbose_name='Suspected Cholera death'),
        ),
        migrations.AlterField(
            model_name='epidemiologyr',
            name='ebola_case',
            field=models.IntegerField(verbose_name='Suspected Ebola cases'),
        ),
        migrations.AlterField(
            model_name='epidemiologyr',
            name='ebola_death',
            field=models.IntegerField(verbose_name='Suspected Ebola death'),
        ),
        migrations.AlterField(
            model_name='epidemiologyr',
            name='influenza_a_h1n1_case',
            field=models.IntegerField(verbose_name='Suspected Influenza A H1N1 cases'),
        ),
        migrations.AlterField(
            model_name='epidemiologyr',
            name='influenza_a_h1n1_death',
            field=models.IntegerField(verbose_name='Suspected Influenza A H1N1 death'),
        ),
        migrations.AlterField(
            model_name='epidemiologyr',
            name='measles_case',
            field=models.IntegerField(verbose_name='Suspected Measles cases'),
        ),
        migrations.AlterField(
            model_name='epidemiologyr',
            name='measles_death',
            field=models.IntegerField(verbose_name='Suspected Measles death'),
        ),
        migrations.AlterField(
            model_name='epidemiologyr',
            name='meningitis_case',
            field=models.IntegerField(verbose_name='Suspected Meningitis cases'),
        ),
        migrations.AlterField(
            model_name='epidemiologyr',
            name='meningitis_death',
            field=models.IntegerField(verbose_name='Suspected Meningitis death'),
        ),
        migrations.AlterField(
            model_name='epidemiologyr',
            name='neonatal_tetanus_case',
            field=models.IntegerField(verbose_name='Suspected NNT cases'),
        ),
        migrations.AlterField(
            model_name='epidemiologyr',
            name='neonatal_tetanus_death',
            field=models.IntegerField(verbose_name='Suspected NNT death'),
        ),
        migrations.AlterField(
            model_name='epidemiologyr',
            name='other_notifiable_disease_case',
            field=models.IntegerField(verbose_name='Suspected Other Notifiable Diseases cases'),
        ),
        migrations.AlterField(
            model_name='epidemiologyr',
            name='other_notifiable_disease_death',
            field=models.IntegerField(verbose_name='Suspected Other Notifiable Diseases death'),
        ),
        migrations.AlterField(
            model_name='epidemiologyr',
            name='rabies_case',
            field=models.IntegerField(verbose_name='Suspected Rabies cases'),
        ),
        migrations.AlterField(
            model_name='epidemiologyr',
            name='rabies_death',
            field=models.IntegerField(verbose_name='Suspected Rabies death'),
        ),
        migrations.AlterField(
            model_name='epidemiologyr',
            name='red_diarrhea_case',
            field=models.IntegerField(verbose_name='Suspected Red Diarrhea cases'),
        ),
        migrations.AlterField(
            model_name='epidemiologyr',
            name='red_diarrhea_death',
            field=models.IntegerField(verbose_name='Suspected Red Diarrhea death'),
        ),
        migrations.AlterField(
            model_name='epidemiologyr',
            name='yellow_fever_case',
            field=models.IntegerField(verbose_name='Suspected Yellow Fever cases'),
        ),
        migrations.AlterField(
            model_name='epidemiologyr',
            name='yellow_fever_death',
            field=models.IntegerField(verbose_name='Suspected Yellow Fever death'),
        ),
    ]
