# Generated by Django 5.0.3 on 2024-06-29 10:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_teacher_class_mapp'),
    ]

    operations = [
        migrations.CreateModel(
            name='teacher_sub_mapp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=20)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.teacher_info')),
            ],
        ),
    ]
