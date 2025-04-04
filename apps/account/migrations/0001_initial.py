# Generated by Django 5.1.6 on 2025-02-18 09:14

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='deleted at')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('code', models.CharField(max_length=50, verbose_name='Code')),
            ],
            options={
                'verbose_name': 'Role',
                'verbose_name_plural': 'Roles',
                'db_table': 'roles',
                'constraints': [models.UniqueConstraint(fields=('code',), name='roles_code_idx')],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='deleted at')),
                ('full_name', models.CharField(max_length=50, verbose_name='Full Name')),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='Email')),
                ('phone_number', models.CharField(blank=True, max_length=15, verbose_name='Phone Number')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Is Staff')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('state', models.ForeignKey(blank=True, limit_choices_to={'type': 'account_state'}, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='+', to='core.datalookup')),
                ('type', models.ForeignKey(blank=True, limit_choices_to={'type': 'user_type'}, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='+', to='core.datalookup')),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='+', to='account.role')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'db_table': 'users',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='UserPreferences',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='deleted at')),
                ('notification_enabled', models.BooleanField(default=True, verbose_name='Notification Enabled')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='preferences', related_query_name='preference', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Preference',
                'verbose_name_plural': 'User Preferences',
                'db_table': 'user_preferences',
            },
        ),
    ]
