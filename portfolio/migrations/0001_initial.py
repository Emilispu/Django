# Generated by Django 4.2.7 on 2023-11-22 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Title')),
                ('author', models.CharField(max_length=100, verbose_name='Author')),
                ('content', models.CharField(max_length=2000, verbose_name='Primary_text')),
                ('text', models.TextField(null=True, verbose_name='Secondary_text')),
                ('images', models.ImageField(blank=True, null=True, upload_to='media/img', verbose_name='Image')),
                ('downloads', models.FileField(blank=True, null=True, upload_to='download')),
                ('href_to_site', models.CharField(max_length=200, null=True, verbose_name='link to site')),
                ('href_to_github', models.CharField(max_length=200, null=True, verbose_name='link to Github')),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
                'ordering': ['title'],
            },
        ),
    ]
