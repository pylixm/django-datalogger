from django.contrib import admin
from models import Datalogger


class DataloggerAdmin(admin.ModelAdmin):
    list_display = ('event_id','event_type','object_id','model_name','field_name','before_value','after_value','operator','create_at','update_at')
    search_fields = ('event_id','event_type','object_id','model_name','field_name','before_value','after_value','operator')


admin.site.register(Datalogger, DataloggerAdmin)