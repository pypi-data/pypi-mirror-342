import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0003_project_project_manager_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactHistoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pseudonym', models.CharField(max_length=64, verbose_name='Pseudonym')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Invited by email'), (1, 'Invited by phone'), (2, 'Did not answer the phone'), (3, 'Phone callback scheduled')], verbose_name='Status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.project', verbose_name='Project')),
            ],
            options={
                'verbose_name': 'Contact history item',
                'verbose_name_plural': 'Contact history items',
                'ordering': ('-created_at',),
            },
        ),
    ]
