# Generated by Django 4.2.6 on 2023-11-02 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_post_delete_date_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Post',
            new_name='Board',
        ),
        migrations.RenameModel(
            old_name='Post_bookmark',
            new_name='Board_bookmark',
        ),
        migrations.RenameModel(
            old_name='Post_Comment',
            new_name='Board_Comment',
        ),
        migrations.RenameModel(
            old_name='Post_Like',
            new_name='Board_Like',
        ),
    ]
