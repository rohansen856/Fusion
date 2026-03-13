from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placement_cell', '0003_recruitercompanyaccess'),
    ]

    operations = [
        migrations.AddField(
            model_name='placementapplication',
            name='recruiter_status',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='placementapplication',
            name='status_updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
