# Generated by Django 3.0.3 on 2021-04-29 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20210429_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='TextForAuthor',
            field=models.TextField(default=None, null=True, verbose_name='دلیل برگشت'),
        ),
    ]