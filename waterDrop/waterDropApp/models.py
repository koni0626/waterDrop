from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser, User
from django.contrib.auth.validators import UnicodeUsernameValidator
# Create your models here.

'''
部テーブル
'''
class BuTable(models.Model):
    class Meta:
        verbose_name = "部門情報"
        verbose_name_plural = '部門情報'

    buCode = models.AutoField(primary_key=True, verbose_name="部コード", help_text="部コードを入力してください(0001など)")
    name = models.CharField(max_length=32, null=False, verbose_name="部名", help_text="部名を入力してください")

    def __str__(self):
        return self.name

'''
課テーブル
'''
class KaTable(models.Model):
    class Meta:
        verbose_name = "課情報"
        verbose_name_plural = '課情報'

    kaCode = models.AutoField(primary_key=True, verbose_name="課コード", help_text="課コードを入力してください(0001など)")
    name = models.CharField(max_length=32, null=False, verbose_name="課名", help_text="課名を入力してくっださい")
    buCode = models.ForeignKey(BuTable, on_delete=models.CASCADE, null=False, verbose_name="所属部門", help_text="課が所属する部コードを選択してください")
    def __str__(self):
        return self.name

'''
社員テーブル
'''
class User(AbstractUser):
    class Meta:
        verbose_name = "社員情報"
        verbose_name_plural = '社員情報'

    kaCode = models.ForeignKey(KaTable, on_delete=models.CASCADE, null=True, verbose_name="課コード", help_text="所属課を選択してください")


'''
タイムカードテーブル
'''
class TimeCardTable(models.Model):
    '''このテーブルは別のページで編集できるようにする'''
    class Meta:
        verbose_name = "タイムカード"
        verbose_name_plural = 'タイムカード'

    id = models.BigAutoField(primary_key=True, null=False)
    day = models.DateField(null=False, unique=True)
    employ_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, verbose_name="社員番号")
    inTime = models.TimeField(verbose_name="出社時間", null=True, blank=True)
    offTime = models.TimeField(verbose_name="退社時間", null=True, blank=True)

    def __str__(self):
        return str(self.day)

    def getEmployeeid(self):
        return str(self.employ_id)

    def getInTime(self):
        return str(self.inTime)

    def getOffTime(self):
        return str(self.offTime)

'''
作番テーブル
'''
class WorkCodeTable(models.Model):
    class Meta:
        verbose_name = "作業番号"
        verbose_name_plural = "作業番号"
    dummy_id = models.AutoField(primary_key=True)
    work_code = models.CharField(max_length=32, null=True, unique=True, verbose_name="作番コード")
    name = models.CharField(max_length=128, verbose_name="作業内容")

'''
作業内容テーブル
'''
class WorkDetailCodeTable(models.Model):
    class Meta:
        verbose_name = "作業内容"
        verbose_name_plural = "作業内容"

    dummy_id = models.AutoField(primary_key=True)
    work_detail_code = models.CharField(max_length=32, unique=True, null=False, verbose_name="作業コード")
    contents = models.CharField(max_length=512, verbose_name="作業内容の説明")

    def __str__(self):
        return self.work_detail_code

'''
作業テーブル
'''
class WorkTable(models.Model):
    class Meta:
        verbose_name = "作業一覧"
        verbose_name_plural = "作業一覧"

    id = models.BigAutoField(primary_key=True, null=False)
    time_card_id = models.ForeignKey(TimeCardTable, on_delete=models.CASCADE, null=False)
    work_code = models.ForeignKey(WorkCodeTable, on_delete=models.CASCADE, null=False)
    work_detail_code = models.ForeignKey(WorkDetailCodeTable, on_delete=models.CASCADE, null=False)
    work_time = models.FloatField()

'''
単価テーブル
'''
class PriceTable(models.Model):
    class Meta:
        verbose_name = "単価"
        verbose_name_plural = "単価"

    tanka_id = models.BigAutoField(primary_key=True, null=False)
    name = models.CharField(max_length=32, null=False, verbose_name="単価名", help_text="社員の等級を設定します")
    tanka = models.IntegerField(verbose_name="単価", help_text="等級の時給単価を設定します")

    def __str__(self):
        return self.name

'''
休暇区分テーブル
'''
class HolidayKubunTable(models.Model):
    class Meta:
        verbose_name = "休暇区分"
        verbose_name_plural = "休暇区分"

    kubunid = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=32, null=False, verbose_name="休暇区分名", help_text="土日，祝日，夏季休暇など")

    def __str__(self):
        return self.name

'''
オフィステーブル
'''
class OfficeTable(models.Model):
    class Meta:
        verbose_name = "オフィス"
        verbose_name_plural = "オフィス"

    id = models.BigAutoField(primary_key=True, null=False)
    name = models.CharField(max_length=32, null=False,verbose_name="オフィス名", help_text="事務所ごとに休日カレンダーを指定できます")

    def __str__(self):
        return self.name

'''
カレンダーテーブル
休みだけ登録する
'''
class CalendarTable(models.Model):
    class Meta:
        verbose_name = "休日カレンダー"
        verbose_name_plural = '休日カレンダー'

    id = models.BigAutoField(primary_key=True, null=False)
    name = models.ForeignKey(OfficeTable, on_delete=models.CASCADE, null=False, verbose_name="オフィス名", help_text="カレンダーを適用するオフィスを選択します")
    date = models.DateField( verbose_name="日付", help_text="休日を指定してください", null=True, unique=True)
    Remark = models.CharField(max_length=128, null=True, verbose_name="備考", help_text="祝日名や夏休みなどを記入してください")
    kubunid = models.ForeignKey(HolidayKubunTable, on_delete=models.CASCADE, null=False, verbose_name="休暇区分", help_text="休暇区分を指定します")

    def __str__(self):
        return str(self.date)

'''
交通手段
'''
class HowToMove(models.Model):
    class Meta:
        verbose_name = "交通手段"
        verbose_name_plural = '交通手段'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, verbose_name="移動手段", help_text="移動手段を入力します")

    def __str__(self):
        return self.name

'''承認ステータス'''
class ApproveStatus(models.Model):
    class Meta:
        verbose_name = "承認ステータス"
        verbose_name_plural = "承認ステータス"
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, verbose_name="承認ステータス")

    def __str__(self):
        return self.name

class TransportExpense(models.Model):
    class Meta:
        verbose_name = "交通費"
        verbose_name_plural = "交通費"

    id = models.BigAutoField(primary_key=True)
    employee_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, verbose_name="社員番号")
    date = models.DateField(verbose_name="移動日")
    adddate = models.DateTimeField(auto_now_add=True, verbose_name="申請日", null=True)
    expense = models.IntegerField(default=0, verbose_name="交通費")
    start = models.CharField(max_length=128,verbose_name="出発地")
    end = models.CharField(max_length=128,verbose_name="目的地")
    how = models.ForeignKey(HowToMove, on_delete=models.CASCADE, null=False, verbose_name="交通手段", help_text="交通手段を指定します（電車、タクシーなど)")
    status = models.ForeignKey(ApproveStatus, on_delete=models.CASCADE, null=False, verbose_name="承認ステータス", help_text="承認ステータスを指定します")
    remark = models.CharField(max_length=256, null=False)

    def __str__(self):
        return str(self.date)

