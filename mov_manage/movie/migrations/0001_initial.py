# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('comment_user', models.CharField(max_length=50)),
                ('comment_time', models.CharField(max_length=50)),
                ('comment_like', models.CharField(max_length=10)),
                ('comment_content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('mov_name', models.CharField(max_length=50)),
                ('mov_rate', models.CharField(max_length=10)),
                ('mov_url', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='comments',
            name='mov_id',
            field=models.ForeignKey(to='movie.Detail'),
        ),
    ]
