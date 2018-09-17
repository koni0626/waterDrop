from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, BuTable, KaTable, CalendarTable, TimeCardTable, WorkCodeTable
from .models import WorkDetailCodeTable, WorkTable, PriceTable, HolidayKubunTable, User
from .models import OfficeTable, TransportExpense, HowToMove, ApproveStatus


'''社員情報の定義'''
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

'''タイムカードの定義'''
admin.site.register(TimeCardTable)

'''カレンダーの定義'''
class CalendarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'Remark', "kubunid")

admin.site.register(CalendarTable, CalendarModelAdmin)

'''オフィスの定義'''
admin.site.register(OfficeTable)

admin.site.register(WorkCodeTable)

admin.site.register(WorkDetailCodeTable)

admin.site.register(WorkTable)

'''単価の定義'''
class PriceModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'tanka')

admin.site.register(PriceTable, PriceModelAdmin)

'''休暇区分の定義'''
admin.site.register(HolidayKubunTable)

'''交通手段の定義'''
admin.site.register(HowToMove)

'''審査承認ステータスの定義'''
admin.site.register(ApproveStatus)

'''交通費申請の定義'''
class TransportModelAdmin(admin.ModelAdmin):
    list_display = ('date', 'adddate', 'start', 'end', "expense")

admin.site.register(TransportExpense, TransportModelAdmin)