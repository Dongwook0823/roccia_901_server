# Generated by Django 4.2.9 on 2024-03-26 13:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workout_location', models.CharField(choices=[('더클라임 일산', '더클라임 일산'), ('더클라임 연남', '더클라임 연남'), ('더클라임 양재', '더클라임 양재'), ('더클라임 신림', '더클라임 신림')], help_text='운동 지점', max_length=100)),
                ('start_time', models.DateTimeField(help_text='운동 시작 시간')),
                ('end_time', models.DateTimeField(help_text='운동 종료 시간')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='생성 일시')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='수정 일시')),
                ('user', models.ForeignKey(help_text='사용자 ID', on_delete=django.db.models.deletion.CASCADE, related_name='records', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'record',
            },
        ),
        migrations.CreateModel(
            name='BoulderProblem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workout_level', models.IntegerField(choices=[(1, '하얀색'), (2, '노란색'), (3, '주황색'), (4, '초록색'), (5, '파란색'), (6, '빨간색'), (7, '보라색'), (8, '회색'), (9, '갈색'), (10, '검정색')], help_text='운동 난이도')),
                ('count', models.PositiveIntegerField(help_text='푼 문제 개수')),
                ('record', models.ForeignKey(help_text='운동 기록 ID', on_delete=django.db.models.deletion.CASCADE, related_name='boulder_problems', to='record.record')),
            ],
            options={
                'db_table': 'boulder_problem',
            },
        ),
    ]
