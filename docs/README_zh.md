Datalogger
=====

[![ENV](https://img.shields.io/badge/release-v0.1.1-blue.svg)](https://github.com/pylixm/django-datalogger)
[![ENV](https://img.shields.io/badge/python-2.7-green.svg)](https://github.com/pylixm/django-datalogger)
[![ENV](https://img.shields.io/badge/django-1.7+-green.svg)](https://github.com/pylixm/django-datalogger)
[![LICENSE](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/pylixm/django-datalogger/master/LICENSE.txt)

Datalogger 是一个记录 `django model` 的数据变更的app。记录了model数据的整个生命周期的变动，可以利用这些数据做数据回溯的功能。

[English Docs](https://github.com/pylixm/django-datalogger)



快速入门
-----------

1. 安装
```python
    pip install django-datalogger
```
1. 将app `django-datalogger` 添加到你的 setting 文件 `INSTALLED_APPS` 中:
```python
    INSTALLED_APPS = [
        ...
        'django-datalogger',
    ]
```
1. 将中间件 `datalogger.middleware.common.DataUpadataDeleteMiddleware` 添加到你setting文件的 `MIDDLEWARE_CLASSES`中:
```python
    MIDDLEWARE_CLASSES = (
    ...
    'datalogger.middleware.common.DataUpadataDeleteMiddleware',
    )
```
1. 运行 `python manage.py makemigrations` 和 `python manage.py migrate` 来创建 `django-datalogger` 的数据记录model。

1. 开始编写你自己的model，使其继承 `LogOnUpdateDeleteModel`抽象类:
```python
class TestA(LogOnUpdateDeleteModel):
    name = models.CharField( max_length=128, blank=True)
    memo = models.TextField()
    create_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now=True)
```
1. 使用 django的 model api 来修改 `TextA` 的数据。
```python
a = TestA.object.get(id=1)
a.name = 'test1'
a.save()
```
1.  你可以从  `datalogger models` 表中看到数据修改记录。
