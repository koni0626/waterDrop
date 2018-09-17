from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, BuTable, KaTable, CalendarTable, TimeCardTable, WorkCodeTable
from .models import WorkDetailCodeTable, WorkTable, PriceTable, KubunTable, MeisaiTable, User



class UserModelAdmin(UserAdmin):
    list_display = ('username', 'last_name','first_name', 'kaCode')

admin.site.register(User, UserModelAdmin)

#admin.site.register(User, UserAdmin)
'''部テーブルの定義'''
class BuModelAdmin(admin.ModelAdmin):
    list_display = ('buCode', 'name')

admin.site.register(BuTable, BuModelAdmin)

'''課テーブルの定義'''
class KaModelAdmin(admin.ModelAdmin):
    list_display = ('kaCode', 'name', "buCode")

admin.site.register(KaTable, KaModelAdmin)

admin.site.register(TimeCardTable)
admin.site.register(CalendarTable)
admin.site.register(WorkCodeTable)
admin.site.register(WorkDetailCodeTable)
admin.site.register(WorkTable)
admin.site.register(PriceTable)
admin.site.register(KubunTable)
admin.site.register(MeisaiTable)
