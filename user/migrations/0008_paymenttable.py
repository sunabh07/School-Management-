# Generated by Django 5.0.3 on 2024-07-28 09:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_contactus'),
    ]

    operations = [
        migrations.CreateModel(
            name='paymenttable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.student_info')),
            ],
        ),
    ]
