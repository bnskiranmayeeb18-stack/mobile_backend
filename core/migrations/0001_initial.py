from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import datetime
from django.conf import settings

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='IdempotencyKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=128)),
                ('method', models.CharField(max_length=10)),
                ('path', models.CharField(max_length=512)),
                ('request_hash', models.CharField(max_length=64)),
                ('response_status', models.IntegerField()),
                ('response_body', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField(default=datetime.datetime(2026, 10, 16, 0, 0, 0, tzinfo=datetime.timezone.utc))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('key', 'user')},
            },
        ),
        migrations.AddIndex(
            model_name='idempotencykey',
            index=models.Index(fields=['key', 'user'], name='core_idempot_key_9f0e7d_idx'),
        ),
        migrations.AddIndex(
            model_name='idempotencykey',
            index=models.Index(fields=['expires_at'], name='core_idempot_expires_6a3d2b_idx'),
        ),
    ]
