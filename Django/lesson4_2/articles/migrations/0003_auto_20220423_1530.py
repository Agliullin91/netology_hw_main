# Generated by Django 3.1.2 on 2022-04-23 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20220420_1604'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articlescope',
            options={'ordering': ['-is_main']},
        ),
        migrations.AlterModelOptions(
            name='scope',
            options={'verbose_name': 'Раздел', 'verbose_name_plural': 'Разделы'},
        ),
        migrations.RenameField(
            model_name='article',
            old_name='scope',
            new_name='scopes',
        ),
        migrations.AlterField(
            model_name='articlescope',
            name='is_main',
            field=models.BooleanField(default=False, verbose_name='Основной'),
        ),
        migrations.AlterField(
            model_name='scope',
            name='title',
            field=models.CharField(max_length=50, verbose_name='Название'),
        ),
    ]
