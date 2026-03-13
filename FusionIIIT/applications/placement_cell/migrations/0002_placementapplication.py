from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic_information', '0001_initial'),
        ('placement_cell', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlacementApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placement_cell.PlacementRecord')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic_information.Student')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='placementapplication',
            unique_together={('student', 'record')},
        ),
    ]
