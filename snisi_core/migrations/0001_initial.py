# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import re
import picklefield.fields
import snisi_tools.misc
import mptt.fields
import snisi_core.models.Reporting
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(primary_key=True, serialize=False, max_length=50, validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$'), 'Enter a valid username.', 'invalid')], help_text='Required. 50 characters or fewer. Letters, numbers and @/./+/-/_ characters', verbose_name='username')),
                ('gender', models.CharField(default='unknown', max_length=30, verbose_name='Gender', choices=[('unknown', 'Unknown'), ('male', 'Man'), ('female', 'Woman')])),
                ('title', models.CharField(blank=True, max_length=50, null=True, verbose_name='Title', choices=[('miss', 'Miss'), ('mistress', 'Mrs.'), ('mister', 'Mr.'), ('professor', 'Pr.'), ('doctor', 'Dr.')])),
                ('first_name', models.CharField(max_length=100, null=True, verbose_name='First Name', blank=True)),
                ('middle_name', models.CharField(max_length=100, null=True, verbose_name='Middle Name', blank=True)),
                ('last_name', models.CharField(max_length=100, null=True, verbose_name='Last Name', blank=True)),
                ('maiden_name', models.CharField(max_length=100, null=True, verbose_name='Maiden Name', blank=True)),
                ('position', models.CharField(max_length=250, null=True, verbose_name='Position', blank=True)),
                ('access_since', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Access Since')),
                ('email', models.EmailField(max_length=75, null=True, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'verbose_name': 'Provider',
                'verbose_name_plural': 'Providers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(max_length=250, choices=[('autovalidated_reports', 'Autovalidated Reports'), ('started_in_time_data_collection', 'Started In Time Data Collection'), ('generated_static_files', 'Generated Static Files'), ('changed_provider_role_location', 'Changed Provider Role/Location'), ('uploaded_report', 'Uploaded Report'), ('validated_report', 'Validated Report'), ('created_cluster', 'Created Cluster'), ('added_phone', 'Added Phone Number'), ('sent_unhandled_sms', 'Sent Unhandled SMS'), ('created_participations', 'Created Participations'), ('ended_region_validation', 'Ended Region Validation'), ('logged_out', 'Logged Out'), ('created_aggregated_reports', 'Created Aggregated Reports'), ('enabled_entity', 'Enabled Entity'), ('started_region_validation', 'Started Region Validation'), ('created_entity', 'Created Entity'), ('created_expecteds', 'Created Report Expectations'), ('removed_phone', 'Removed Phone Number'), ('started_late_data_collection', 'Started Late Data Collection'), ('disabled_cluster', 'Disabled Cluster'), ('ended_district_validation', 'Ended District Validation'), ('created_report', 'Created Report'), ('enabled_cluster', 'Enabled Cluster'), ('raised_expection', 'Raised Exception'), ('edited_provider', 'Edited Provider'), ('started_district_validation', 'Started District Validation'), ('edited_report', 'Edited Report'), ('ended_late_data_collection', 'Started Late Data Collection'), ('created_provider', 'Created Provider'), ('enabled_provider', 'Enabled Provider'), ('disabled_provider', 'Disabled Provider'), ('disabled_entity', 'Disabled Entity'), ('edited_entity', 'Edited Entity'), ('changed_passwd', 'Changed Password'), ('created_domain', 'Created domain'), ('asked_for_help', 'Asked for Help'), ('logged_in', 'Logged In'), ('sent_report_sms', 'Sent Report SMS'), ('edited_profile', 'Edited Profile'), ('ended_in_time_data_collection', 'Ended In Time Data Collection'), ('restarted_webserver', 'Restarted Web Server')])),
                ('on', models.DateTimeField(auto_now=True)),
                ('iface', models.CharField(max_length=50, choices=[('web', 'Web'), ('sms', 'SMS'), ('server', 'Server')])),
                ('instance_cls', models.CharField(max_length=500, null=True, blank=True)),
                ('instance_pk', models.CharField(max_length=500, null=True, blank=True)),
                ('payload', picklefield.fields.PickledObjectField(null=True, editable=False, blank=True)),
            ],
            options={
                'verbose_name': 'Action',
                'verbose_name_plural': 'Action',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('slug', models.CharField(max_length=75, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('is_active', models.BooleanField(default=True)),
                ('contact', models.ForeignKey(related_name='clusters_as_contact', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Cluster',
                'verbose_name_plural': 'Clusters',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('slug', models.CharField(max_length=75, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('is_active', models.BooleanField(default=True)),
                ('short_description', models.CharField(max_length=250, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('module_path', models.CharField(unique=True, max_length=200)),
                ('operational_contact', models.ForeignKey(related_name='projects_as_opcontact', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('technical_contact', models.ForeignKey(related_name='projects_as_techcontact', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Domain',
                'verbose_name_plural': 'Domains',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('slug', models.SlugField(max_length=15, serialize=False, verbose_name='Slug', primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('geometry', models.TextField(null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('active_changed_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
            ],
            options={
                'verbose_name': 'Entity',
                'verbose_name_plural': 'Entities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AdministrativeEntity',
            fields=[
                ('entity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='snisi_core.Entity')),
                ('main_entity_distance', models.FloatField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Admin. Entity',
                'verbose_name_plural': 'Admin. Entities',
            },
            bases=('snisi_core.entity',),
        ),
        migrations.CreateModel(
            name='EntityType',
            fields=[
                ('slug', models.SlugField(max_length=15, serialize=False, verbose_name='Slug', primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Entity Type',
                'verbose_name_plural': 'Entity Types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExpectedReporting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('within_period', models.BooleanField(default=False)),
                ('within_entity', models.BooleanField(default=False)),
                ('amount_expected', models.CharField(max_length=30, choices=[('single', 'Single'), ('multiple', 'Multiple'), ('zero_or_more', '0+'), ('single_or_more', '1+')])),
                ('completion_status', models.CharField(max_length=30, choices=[('missing', 'Missing'), ('satisfied', 'Complete'), ('matching', 'Matching')])),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Expected Report',
                'verbose_name_plural': 'Expected Reports',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HealthEntity',
            fields=[
                ('entity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='snisi_core.Entity')),
                ('main_entity', models.ForeignKey(blank=True, to='snisi_core.HealthEntity', null=True)),
            ],
            options={
                'verbose_name': 'Health Entity',
                'verbose_name_plural': 'Health Entities',
            },
            bases=('snisi_core.entity',),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('destination_email', models.EmailField(max_length=75, null=True, blank=True)),
                ('destination_number', models.CharField(max_length=75, null=True, blank=True)),
                ('deliver', models.CharField(max_length=75, choices=[('immediately', 'Immediately'), ('later', 'Later'), ('soon', 'Soon'), ('today', 'Today'), ('quickly', 'Quickly')])),
                ('sent', models.BooleanField(default=False)),
                ('sent_on', models.DateTimeField(null=True, blank=True)),
                ('delivery_status', models.CharField(default='unknown', max_length=75, choices=[('delivered', 'Delivered'), ('expired', 'Expired'), ('unknown', 'Unknown'), ('not_delivered', 'Not delivered')])),
                ('expirate_on', models.DateTimeField(null=True, blank=True)),
                ('method', models.CharField(default='preferred', max_length=75, choices=[('all', 'All methods'), ('sms', 'SMS'), ('email', 'Email'), ('preferred', 'Preferred'), ('all_contacts', 'All contacts')])),
                ('level', models.CharField(default='info', max_length=75, choices=[('info', 'Info'), ('action_required', 'Action Required'), ('warning', 'Warning'), ('success', 'Success'), ('error', 'Error')])),
                ('important', models.BooleanField(default=False)),
                ('category', models.CharField(max_length=75, null=True, blank=True)),
                ('title', models.TextField(null=True, blank=True)),
                ('text', models.TextField()),
                ('text_short', models.TextField(null=True, blank=True)),
                ('provider', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('modified_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('cluster', models.ForeignKey(related_name='participations', to='snisi_core.Cluster')),
                ('entity', models.ForeignKey(related_name='participations', to='snisi_core.Entity')),
            ],
            options={
                'verbose_name': 'Participation',
                'verbose_name_plural': 'Participations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('identifier', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('start_on', models.DateTimeField(verbose_name='Start On')),
                ('end_on', models.DateTimeField(verbose_name='End On')),
                ('period_type', models.CharField(default='custom', max_length=100, verbose_name='Type', choices=[('week', 'Week'), ('custom', 'Custom'), ('month', 'Month'), ('semester', 'Semester'), ('year', 'Year'), ('quarter', 'Quarter'), ('day', 'Day')])),
            ],
            options={
                'verbose_name': 'Period',
                'verbose_name_plural': 'Periods',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PeriodicTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(unique=True, max_length=255)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created')),
                ('category', models.CharField(max_length=300, null=True, blank=True)),
                ('triggered', models.BooleanField(default=False)),
                ('triggered_on', models.DateTimeField(null=True, verbose_name='triggered on', blank=True)),
            ],
            options={
                'verbose_name': 'Periodic Task',
                'verbose_name_plural': 'Periodic Tasks',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('identity', models.CharField(max_length=75, serialize=False, primary_key=True)),
                ('priority', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('provider', '-priority'),
                'verbose_name': 'Phone Number',
                'verbose_name_plural': 'Phone numbers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhoneNumberType',
            fields=[
                ('slug', models.CharField(max_length=75, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('abbr', models.CharField(max_length=10)),
                ('priority', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Phone Number Type',
                'verbose_name_plural': 'Phone number types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReportClass',
            fields=[
                ('slug', models.SlugField(max_length=75, serialize=False, verbose_name='Slug', primary_key=True)),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('cls', models.CharField(max_length=75, verbose_name='cls')),
                ('period_cls', models.CharField(max_length=75, verbose_name='Period Type')),
                ('report_type', models.CharField(max_length=30, choices=[('perioagg', 'Periodical Aggregated'), ('periosrc', 'Periodical Source'), ('occasioagg', 'Occasional Aggregated'), ('occasiosrc', 'Occasional Source')])),
            ],
            options={
                'verbose_name': 'Report Class',
                'verbose_name_plural': 'Report Classes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('slug', models.SlugField(max_length=15, serialize=False, verbose_name='Slug', primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Role',
                'verbose_name_plural': 'Roles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SMSMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('direction', models.CharField(max_length=75, choices=[('outgoing', 'Outgoing'), ('incoming', 'Incoming')])),
                ('identity', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('event_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('text', models.TextField()),
                ('handled', models.BooleanField(default=False)),
                ('validity', models.PositiveIntegerField(null=True, blank=True)),
                ('deferred', models.PositiveIntegerField(null=True, blank=True)),
                ('delivery_status', models.CharField(default='unknown', max_length=75, choices=[('buffered', 'Message Buffered'), ('success', 'Delivery Success'), ('smsc_submit', 'SMSC Submit'), ('smsc_notifications', 'SMSC Intermediate Notifications'), ('unknown', 'Unknown'), ('failure', 'Delivery Failure'), ('smsc_reject', 'SMSC Reject')])),
            ],
            options={
                'verbose_name': 'SMS Message',
                'verbose_name_plural': 'SMS Messages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SNISIGroup',
            fields=[
                ('group_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='auth.Group')),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
            },
            bases=('auth.group',),
        ),
        migrations.CreateModel(
            name='SNISIReport',
            fields=[
                ('uuid', models.CharField(default=snisi_tools.misc.get_uuid, max_length=200, serialize=False, primary_key=True)),
                ('receipt', models.CharField(unique=True, max_length=200)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created On')),
                ('modified_on', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Modified On')),
                ('completion_status', models.CharField(default='incomplete', max_length=40, choices=[('complete', 'Complete'), ('incomplete', 'Incomplete')])),
                ('completed_on', models.DateTimeField(null=True, blank=True)),
                ('integrity_status', models.CharField(default='not_checked', max_length=40, choices=[('incorrect', 'Incorrect'), ('not_checked', 'Not Checked'), ('correct', 'Correct')])),
                ('arrival_status', models.CharField(default='not_applicable', max_length=40, choices=[('arrived_on_time', 'Arrived On Time'), ('not_applicable', 'N/A'), ('arrived_late', 'Arrived Late')])),
                ('validation_status', models.CharField(default='not_applicable', max_length=40, choices=[('not_applicable', 'N/a'), ('validated', 'Validated'), ('not_validated', 'Not Validated'), ('refused', 'Refused')])),
                ('validated_on', models.DateTimeField(null=True, blank=True)),
                ('auto_validated', models.BooleanField(default=False)),
                ('report_cls', models.CharField(max_length=512, null=True, blank=True)),
            ],
            options={
            },
            bases=(snisi_core.models.Reporting.SuperMixin, snisi_core.models.Reporting.InterestingFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ExpectedValidation',
            fields=[
                ('report', models.ForeignKey(related_name='expected_validations', primary_key=True, serialize=False, to='snisi_core.SNISIReport')),
                ('validated_on', models.DateTimeField(null=True, blank=True)),
                ('satisfied', models.BooleanField(default=False)),
                ('validating_entity', models.ForeignKey(to='snisi_core.Entity')),
                ('validating_role', models.ForeignKey(to='snisi_core.Role')),
            ],
            options={
                'verbose_name': 'Expected Validation',
                'verbose_name_plural': 'Expected Validations',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='snisireport',
            name='created_by',
            field=models.ForeignKey(related_name='snisi_core_snisireport_reports', verbose_name='Created By', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='snisireport',
            name='entity',
            field=models.ForeignKey(related_name='snisi_core_snisireport_reports', blank=True, to='snisi_core.Entity', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='snisireport',
            name='modified_by',
            field=models.ForeignKey(related_name='own_modified_reports', verbose_name='Modified By', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='snisireport',
            name='period',
            field=models.ForeignKey(related_name='snisi_core_snisireport_reports', blank=True, to='snisi_core.Period', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='snisireport',
            name='validated_by',
            field=models.ForeignKey(related_name='own_validated_reports', verbose_name='Validated By', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='reportclass',
            unique_together=set([('cls', 'period_cls', 'report_type')]),
        ),
        migrations.AddField(
            model_name='phonenumber',
            name='category',
            field=models.ForeignKey(to='snisi_core.PhoneNumberType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='phonenumber',
            name='provider',
            field=models.ForeignKey(related_name='phone_numbers', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='period',
            unique_together=set([('start_on', 'end_on', 'period_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='participation',
            unique_together=set([('cluster', 'entity')]),
        ),
        migrations.AddField(
            model_name='expectedvalidation',
            name='validation_period',
            field=models.ForeignKey(to='snisi_core.Period'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='expectedreporting',
            name='arrived_reports',
            field=models.ManyToManyField(related_name='expected_reportings', null=True, to='snisi_core.SNISIReport', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='expectedreporting',
            name='entity',
            field=models.ForeignKey(to='snisi_core.Entity'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='expectedreporting',
            name='extended_reporting_period',
            field=models.ForeignKey(related_name='expr_for_ext_reporting_period', blank=True, to='snisi_core.Period', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='expectedreporting',
            name='period',
            field=models.ForeignKey(related_name='expr_for_period', to='snisi_core.Period'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='expectedreporting',
            name='report_class',
            field=models.ForeignKey(to='snisi_core.ReportClass'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='expectedreporting',
            name='reporting_period',
            field=models.ForeignKey(related_name='expr_for_reporting_period', blank=True, to='snisi_core.Period', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='expectedreporting',
            name='reporting_role',
            field=models.ForeignKey(blank=True, to='snisi_core.Role', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entity',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='children', verbose_name='Parent', blank=True, to='snisi_core.Entity', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entity',
            name='type',
            field=models.ForeignKey(related_name='entities', verbose_name='Type', to='snisi_core.EntityType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cluster',
            name='domain',
            field=models.ForeignKey(blank=True, to='snisi_core.Domain', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='administrativeentity',
            name='health_entity',
            field=models.ForeignKey(related_name='admin_entities', blank=True, to='snisi_core.HealthEntity', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='action',
            name='domain',
            field=models.ForeignKey(blank=True, to='snisi_core.Domain', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='action',
            name='provider',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='provider',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='provider',
            name='location',
            field=models.ForeignKey(related_name='contacts', default='mali', verbose_name='Location', to='snisi_core.Entity'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='provider',
            name='role',
            field=models.ForeignKey(default='guest', verbose_name='Role', to='snisi_core.Role'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='provider',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='DayPeriod',
            fields=[
            ],
            options={
                'verbose_name': 'Period',
                'proxy': True,
                'verbose_name_plural': 'Periods',
            },
            bases=('snisi_core.period',),
        ),
        migrations.CreateModel(
            name='FixedDaysPeriod',
            fields=[
            ],
            options={
                'verbose_name': 'Fixed Days Period',
                'proxy': True,
                'verbose_name_plural': 'Fixed Days Periods',
            },
            bases=('snisi_core.period',),
        ),
        migrations.CreateModel(
            name='MonthPeriod',
            fields=[
            ],
            options={
                'verbose_name': 'Period',
                'proxy': True,
                'verbose_name_plural': 'Periods',
            },
            bases=('snisi_core.period',),
        ),
        migrations.CreateModel(
            name='FixedMonthThirdWeekReportingPeriod',
            fields=[
            ],
            options={
                'verbose_name': 'Monthly Reporting Period',
                'proxy': True,
                'verbose_name_plural': 'Monthly Reporting Periods',
            },
            bases=('snisi_core.monthperiod',),
        ),
        migrations.CreateModel(
            name='FixedMonthThirdWeekExtendedReportingPeriod',
            fields=[
            ],
            options={
                'verbose_name': 'Monthly Extended Reporting Period',
                'proxy': True,
                'verbose_name_plural': 'Monthly ExtendedReporting Periods',
            },
            bases=('snisi_core.monthperiod',),
        ),
        migrations.CreateModel(
            name='FixedMonthThirdWeek',
            fields=[
            ],
            options={
                'verbose_name': 'Monthly Reporting Period',
                'proxy': True,
                'verbose_name_plural': 'Monthly Reporting Periods',
            },
            bases=('snisi_core.monthperiod',),
        ),
        migrations.CreateModel(
            name='FixedMonthSecondWeekReportingPeriod',
            fields=[
            ],
            options={
                'verbose_name': 'Monthly Reporting Period',
                'proxy': True,
                'verbose_name_plural': 'Monthly Reporting Periods',
            },
            bases=('snisi_core.monthperiod',),
        ),
        migrations.CreateModel(
            name='FixedMonthSecondWeekExtendedReportingPeriod',
            fields=[
            ],
            options={
                'verbose_name': 'Monthly Extended Reporting Period',
                'proxy': True,
                'verbose_name_plural': 'Monthly ExtendedReporting Periods',
            },
            bases=('snisi_core.monthperiod',),
        ),
        migrations.CreateModel(
            name='FixedMonthSecondWeek',
            fields=[
            ],
            options={
                'verbose_name': 'Monthly Reporting Period',
                'proxy': True,
                'verbose_name_plural': 'Monthly Reporting Periods',
            },
            bases=('snisi_core.monthperiod',),
        ),
        migrations.CreateModel(
            name='FixedMonthFourthWeekReportingPeriod',
            fields=[
            ],
            options={
                'verbose_name': 'Monthly Reporting Period',
                'proxy': True,
                'verbose_name_plural': 'Monthly Reporting Periods',
            },
            bases=('snisi_core.monthperiod',),
        ),
        migrations.CreateModel(
            name='FixedMonthFourthWeekExtendedReportingPeriod',
            fields=[
            ],
            options={
                'verbose_name': 'Monthly Extended Reporting Period',
                'proxy': True,
                'verbose_name_plural': 'Monthly ExtendedReporting Periods',
            },
            bases=('snisi_core.monthperiod',),
        ),
        migrations.CreateModel(
            name='FixedMonthFourthWeek',
            fields=[
            ],
            options={
                'verbose_name': 'Monthly Reporting Period',
                'proxy': True,
                'verbose_name_plural': 'Monthly Reporting Periods',
            },
            bases=('snisi_core.monthperiod',),
        ),
        migrations.CreateModel(
            name='FixedMonthFirstWeekReportingPeriod',
            fields=[
            ],
            options={
                'verbose_name': 'Monthly Reporting Period',
                'proxy': True,
                'verbose_name_plural': 'Monthly Reporting Periods',
            },
            bases=('snisi_core.monthperiod',),
        ),
        migrations.CreateModel(
            name='FixedMonthFirstWeekExtendedReportingPeriod',
            fields=[
            ],
            options={
                'verbose_name': 'Monthly Extended Reporting Period',
                'proxy': True,
                'verbose_name_plural': 'Monthly ExtendedReporting Periods',
            },
            bases=('snisi_core.monthperiod',),
        ),
        migrations.CreateModel(
            name='FixedMonthFirstWeek',
            fields=[
            ],
            options={
                'verbose_name': 'Monthly Reporting Period',
                'proxy': True,
                'verbose_name_plural': 'Monthly Reporting Periods',
            },
            bases=('snisi_core.monthperiod',),
        ),
        migrations.CreateModel(
            name='FixedMonthFifthWeekReportingPeriod',
            fields=[
            ],
            options={
                'verbose_name': 'Monthly Reporting Period',
                'proxy': True,
                'verbose_name_plural': 'Monthly Reporting Periods',
            },
            bases=('snisi_core.monthperiod',),
        ),
        migrations.CreateModel(
            name='FixedMonthFifthWeekExtendedReportingPeriod',
            fields=[
            ],
            options={
                'verbose_name': 'Monthly Extended Reporting Period',
                'proxy': True,
                'verbose_name_plural': 'Monthly ExtendedReporting Periods',
            },
            bases=('snisi_core.monthperiod',),
        ),
        migrations.CreateModel(
            name='FixedMonthFifthWeek',
            fields=[
            ],
            options={
                'verbose_name': 'Fifth Monthly Reporting Period',
                'proxy': True,
                'verbose_name_plural': 'Monthly Reporting Periods',
            },
            bases=('snisi_core.monthperiod',),
        ),
        migrations.CreateModel(
            name='DefaultRegionValidationPeriod',
            fields=[
            ],
            options={
                'verbose_name': 'Region Validation Period',
                'proxy': True,
                'verbose_name_plural': 'Region Validation Periods',
            },
            bases=('snisi_core.monthperiod',),
        ),
        migrations.CreateModel(
            name='DefaultNationalValidationPeriod',
            fields=[
            ],
            options={
                'verbose_name': 'National Validation Period',
                'proxy': True,
                'verbose_name_plural': 'National Validation Periods',
            },
            bases=('snisi_core.monthperiod',),
        ),
        migrations.CreateModel(
            name='DefaultMonthlyReportingPeriod',
            fields=[
            ],
            options={
                'verbose_name': 'Monthly Reporting Period',
                'proxy': True,
                'verbose_name_plural': 'Monthly Reporting Periods',
            },
            bases=('snisi_core.monthperiod',),
        ),
        migrations.CreateModel(
            name='DefaultMonthlyExtendedReportingPeriod',
            fields=[
            ],
            options={
                'verbose_name': 'Monthly Extended Reporting Period',
                'proxy': True,
                'verbose_name_plural': 'Monthly Extended Reporting Periods',
            },
            bases=('snisi_core.monthperiod',),
        ),
        migrations.CreateModel(
            name='DefaultDistrictValidationPeriod',
            fields=[
            ],
            options={
                'verbose_name': 'District Validation Period',
                'proxy': True,
                'verbose_name_plural': 'District Validation Periods',
            },
            bases=('snisi_core.monthperiod',),
        ),
        migrations.CreateModel(
            name='QuarterPeriod',
            fields=[
            ],
            options={
                'verbose_name': 'Period',
                'proxy': True,
                'verbose_name_plural': 'Periods',
            },
            bases=('snisi_core.period',),
        ),
        migrations.CreateModel(
            name='WeekPeriod',
            fields=[
            ],
            options={
                'verbose_name': 'Period',
                'proxy': True,
                'verbose_name_plural': 'Periods',
            },
            bases=('snisi_core.period',),
        ),
        migrations.CreateModel(
            name='YearPeriod',
            fields=[
            ],
            options={
                'verbose_name': 'Period',
                'proxy': True,
                'verbose_name_plural': 'Periods',
            },
            bases=('snisi_core.period',),
        ),
    ]
