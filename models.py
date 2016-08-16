# -*- coding:utf-8 -*-
from django.db import models
from django.forms.models import model_to_dict
from datalogger import globals

# Create your models here.


class ModelDiffMixin(object):
    """
    model 获取变更字段扩展
    """
    def __init__(self, *args, **kwargs):
        super(ModelDiffMixin, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        super(ModelDiffMixin, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields if field.name !='id'])


class LogOnUpdateDeleteModel(ModelDiffMixin, models.Model):
    """
    重写 model 方法，记录日志操作
    """

    def delete(self, *args, **kwargs):
        if globals.event_id:
            for key, value in model_to_dict(self, fields=[field.name for field in self._meta.fields if
                                                          field.name != 'id']).items():
                dataloger = {'event_id': globals.event_id, 'event_type': 'delete',
                             'model_name': self._meta.model.__name__, 'object_id': self.pk,
                             'field_name': key, 'before_value': value, 'operator': globals.username}
                Datalogger.objects.create(**dataloger)
        super(LogOnUpdateDeleteModel, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # 更新
        if self.pk:
            if globals.event_id and self.changed_fields:
                dataloger = {}
                dataloger['event_id'] = globals.event_id  
                dataloger['event_type'] = 'update'
                dataloger['model_name'] = self._meta.model.__name__
                dataloger['object_id'] = self.pk
                for name in self.changed_fields:
                    dataloger['field_name'] = name
                    before = self.get_field_diff(name)[0] # (变化前的值，变化后的值)
                    after = self.get_field_diff(name)[1] # (变化前的值，变化后的值)
                    dataloger['before_value'] = before
                    dataloger['after_value'] = after
                    dataloger['operator'] = globals.username 
                    Datalogger.objects.create(**dataloger)
            super(LogOnUpdateDeleteModel, self).save(*args, **kwargs)
        else:
            super(LogOnUpdateDeleteModel, self).save(*args, **kwargs)
            # 新增
            if globals.event_id:
                for key, value in model_to_dict(self, fields=[field.name for field in self._meta.fields if field.name != 'id']).items():
                    dataloger = {'event_id': globals.event_id, 'event_type': 'add',
                                 'model_name': self._meta.model.__name__, 'object_id': self.pk,
                                 'field_name': key, 'after_value': value, 'operator': globals.username}
                    Datalogger.objects.create(**dataloger)

    class Meta:
        abstract = True


class Datalogger(models.Model):
    event_id = models.CharField(u'事件ID', max_length=100, blank=True, null=True)
    type_choices = (('delete', u'删除'),
                    ('add', u'新增'),
                    ('update', u'更新'))
    event_type = models.CharField(u'事件类型', choices=type_choices, max_length=10, blank=True, null=True)
    object_id = models.IntegerField(u'数据ID', blank=True, null=True)
    model_name = models.CharField(u'修改对象名称', max_length=100, blank=True, null=True)
    field_name = models.CharField(u'修改的字段名称', max_length=100, blank=True, null=True)
    before_value = models.TextField(u'修改前的值', blank=True, null=True)
    after_value = models.TextField(u'修改后的值', blank=True, null=True)
    operator = models.CharField(u'操作人', max_length=100, blank=True, null=True)
    create_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now=True)

    def __unicode__(self):
        return '%s - %s - %s' % (self.event_id, self.model_name, self.field_name)
