# Generated by Django 4.2.6 on 2023-11-04 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_rename_post_board_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='comment',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Study',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('contents', models.TextField()),
                ('hashtags', models.TextField()),
                ('is_recruited', models.BooleanField(default=False)),
                ('post_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('delete_date', models.DateTimeField(null=True)),
                ('comment', models.IntegerField(default=0)),
                ('like', models.IntegerField(default=0)),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='main.user')),
            ],
        ),
    ]
