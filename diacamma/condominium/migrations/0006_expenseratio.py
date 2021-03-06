# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-28 14:27
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


def convert_expense_ratio(*args):
    from diacamma.condominium.models import ExpenseDetail, ExpenseRatio, Owner
    for expense_detail in ExpenseDetail.objects.filter(expense__status__in=(1, 2)):
        if expense_detail.expense.expensetype == 0:
            is_asset = 1
        else:
            is_asset = -1
        if expense_detail.entry is None:
            expense_detail.generate_ratio(is_asset)
        else:
            try:
                for line in expense_detail.entry.entrylineaccount_set.filter(third__isnull=False).order_by('third_id'):
                    owner = Owner.objects.get(third=line.third)
                    ExpenseRatio.objects.create(expensedetail=expense_detail, value=is_asset * line.amount, owner=owner)
            except:
                expense_detail.generate_ratio(is_asset)


class Migration(migrations.Migration):

    dependencies = [
        ('condominium', '0005_migrate_classload'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseRatio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, default=0.0, max_digits=7, validators=[
                 django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1000.0)], verbose_name='value')),
                ('expensedetail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                    to='condominium.ExpenseDetail', verbose_name='detail of expense')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='condominium.Owner', verbose_name='owner')),
            ],
            options={
                'verbose_name': 'detail of expense',
                'default_permissions': [],
                'ordering': ['owner__third_id'],
                'verbose_name_plural': 'details of expense',
            },
        ),
        migrations.RunPython(convert_expense_ratio),
    ]
