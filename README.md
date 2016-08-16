
Datalogger
=====

[![ENV](https://img.shields.io/badge/release-v0.1.1-blue.svg)](https://github.com/pylixm/django-datalogger)
[![ENV](https://img.shields.io/badge/python-2.7-green.svg)](https://github.com/pylixm/django-datalogger)
[![ENV](https://img.shields.io/badge/django-1.7+-green.svg)](https://github.com/pylixm/django-datalogger)
[![LICENSE](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/pylixm/django-datalogger/master/LICENSE.txt)

Datalogger is a simple Django app to record data changes.

[中文说明](docs/README_zh.md)



Quick start
-----------

1. Installation.
```bash
    pip install django-datalogger
```
1. Add `django-datalogger` to your INSTALLED_APPS setting like this::
```python
    INSTALLED_APPS = [
        ...
        'django-datalogger',
    ]
```
1. Add `datalogger.middleware.common.DataUpadataDeleteMiddleware` to your MIDDLEWARE_CLASSES setting like this::
```python
    MIDDLEWARE_CLASSES = (
    ...
    'datalogger.middleware.common.DataUpadataDeleteMiddleware',
    )
```
1. Run `python manage.py makemigrations` and `python manage.py migrate` to create the `django-datalogger` models.

1. Start your models inherit `LogOnUpdateDeleteModel` abstract model like this:
```python
class TestA(LogOnUpdateDeleteModel):
    name = models.CharField( max_length=128, blank=True)
    memo = models.TextField()
    create_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now=True)
```
1. Change the test model data by the model api.

1. You will find the data change log in datalogger models.You can visit http://127.0.0.1:8000/admin/
   to see these changer.
