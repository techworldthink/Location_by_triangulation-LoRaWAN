# Generated by Django 4.1.7 on 2023-05-22 10:39

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0005_alter_livedata_bvoc_alter_livedata_co2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livedata',
            name='bus_stop',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='adminapp.busstops'),
        ),
        migrations.AlterField(
            model_name='livedata',
            name='bvoc',
            field=models.DecimalField(decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='livedata',
            name='co2',
            field=models.DecimalField(decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='livedata',
            name='device',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='adminapp.deviceeui'),
        ),
        migrations.AlterField(
            model_name='livedata',
            name='humidity',
            field=models.DecimalField(decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='livedata',
            name='iaq',
            field=models.DecimalField(decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='livedata',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='livedata',
            name='live_time',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='livedata',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='livedata',
            name='pressure',
            field=models.DecimalField(decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='livedata',
            name='temperature',
            field=models.DecimalField(decimal_places=2, max_digits=15, null=True),
        ),
    ]