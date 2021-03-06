# Generated by Django 2.1.1 on 2018-09-29 08:11

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20180929_1432'),
        ('goods', '0002_categorymodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255, verbose_name='评论的内容')),
                ('vote_number', models.IntegerField(default=0, verbose_name='点赞数')),
                ('create_time', models.DateTimeField(default=datetime.datetime(2018, 9, 29, 16, 11, 52, 767857), verbose_name='创建时间')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsModel', verbose_name='商品名称')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserModel', verbose_name='评论的用户')),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
                'db_table': 'comment',
            },
        ),
    ]
