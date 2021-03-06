from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, BuTable, KaTable, CalendarTable, TimeCardTable, WorkCodeTable
from .models import WorkDetailCodeTable, WorkTable, PriceTable, HolidayKindTable, User
from .models import WorkClassTable, TransportExpense, HowToMove, ApproveStatus
from .models import PersonalWorkStatusTable, BelongsTable, OptionTable


@admin.register(User)
class UserModelAdmin(UserAdmin):
    """
    社員情報の定義
    編集はここが参考になる
    https://qiita.com/okoppe8/items/10ae61808dc3056f9c8e
    """
    list_display = ('username', 'last_name', 'first_name', 'is_active', 'lock')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('ユーザ情報', {'fields': ('last_name', 'first_name', 'email', 'is_active', 'lock')}),
        # ('サイトの権限', {'fields': ('is_active', 'is_staff', 'is_superuser',
        #                                 'groups', 'user_permissions')}),
        ('データ登録情報', {'fields': ('last_login', 'date_joined')}),
    )

    """
    override
    保存前に呼び出される
    """
    def save_model(self, request, obj, form, change):
        print("保存前に呼ばれました")
        # 仮パスワード状態
        obj.is_active = False
        obj.count = 0
        # アンロック
        obj.lock = 0

        # メールを送信する
        try:
            super().save_model(request, obj, form, change)
            user = obj
            if user.email != "":
                # メールを送信する
                TEMP_URL = "http://localhost:8000/create_complete000"
                user.email_user("subject", "message", from_email="konishi@basis-corp.jp")
            else:
                # ユーザ名とパスワードだけ入力した
                print("ユーザ名とパスワードだけ")
        except:
            print("ユーザ登録でエラーが発生")


class BuModelAdmin(admin.ModelAdmin):
    # 部テーブルの定義
    list_display = ('bu_code', 'name')


admin.site.register(BuTable, BuModelAdmin)


# 課テーブルの定義
class KaModelAdmin(admin.ModelAdmin):
    list_display = ('ka_code', 'name', "bu_code")


admin.site.register(KaTable, KaModelAdmin)


# 所属テーブルの定義
class BelogModelAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'ka_code')


admin.site.register(BelongsTable, BelogModelAdmin)


# タイムカードの定義
admin.site.register(TimeCardTable)


# カレンダーの定義
class CalendarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'remark', "holiday")


admin.site.register(CalendarTable, CalendarModelAdmin)


# 個人ステータスの定義
admin.site.register(PersonalWorkStatusTable)


# 勤務区分の定義
admin.site.register(WorkClassTable)


# 作業コードの定義
admin.site.register(WorkCodeTable)


class WorkDetailCodeModelAdmin(admin.ModelAdmin):
    # 作業内容の定義
    list_display = ('work_detail_code', 'contents')


admin.site.register(WorkDetailCodeTable, WorkDetailCodeModelAdmin)


# ワークテーブルの定義
admin.site.register(WorkTable)


class PriceModelAdmin(admin.ModelAdmin):
    # 単価の定義
    list_display = ('name', 'tanka')


admin.site.register(PriceTable, PriceModelAdmin)

# 休暇区分の定義
admin.site.register(HolidayKindTable)

# 交通手段の定義
admin.site.register(HowToMove)

# 審査承認ステータスの定義
admin.site.register(ApproveStatus)


class TransportModelAdmin(admin.ModelAdmin):
    # 交通費申請の定義
    list_display = ('date', 'entry_date', 'start', 'end', "expense")


admin.site.register(TransportExpense, TransportModelAdmin)


# オプションテーブル
admin.site.register(OptionTable)
