# Generated by Django 3.0.8 on 2020-10-05 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20201006_0102'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderUpdate',
            fields=[
                ('update_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_id', models.IntegerField(default='')),
                ('update_desc', models.CharField(max_length=5000)),
                ('timestamp', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='items_json',
            field=models.CharField(default=1, max_length=5000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='razorpayid',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='razorpaypaymentid',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='razorpaysignature',
            field=models.CharField(default='', max_length=255),
        ),
    ]
