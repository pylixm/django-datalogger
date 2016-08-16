# -*- coding:utf-8 -*-
import uuid
from datalogger import globals


class DataUpadataDeleteMiddleware(object):

    def process_request(self, request):
        """
        定义request 事件 id 和 操作人
        """
        globals.event_id = uuid.uuid1()
        globals.username = request.user.username
