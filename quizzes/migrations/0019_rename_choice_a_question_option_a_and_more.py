# Generated by Django 4.2.7 on 2023-11-30 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0018_question_choice_a_question_choice_b_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='choice_a',
            new_name='option_a',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='choice_b',
            new_name='option_b',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='choice_c',
            new_name='option_c',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='choice_d',
            new_name='option_d',
        ),
    ]
