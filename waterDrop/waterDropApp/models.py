from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser, User
from django.contrib.auth.validators import UnicodeUsernameValidator

# Create your models here.


class BuTable(models.Model):
    """
    部テーブル
    """
    class Meta:
        verbose_name = "部門情報"
        verbose_name_plural = '部門情報'

    bu_code = models.AutoField(primary_key=True,
                               verbose_name="部コード", help_text="部コードを入力してください(0001など)")

    name = models.CharField(max_length=32, null=False,
                            verbose_name="部名", help_text="部名を入力してください")

    def __str__(self):
        return self.name


class KaTable(models.Model):
    """
    課テーブル
    """
    class Meta:
        verbose_name = "課情報"
        verbose_name_plural = '課情報'

    ka_code = models.AutoField(primary_key=True,
                               verbose_name="課コード", help_text="課コードを入力してください(0001など)")

    name = models.CharField(max_length=32, null=False,
                            verbose_name="課名", help_text="課名を入力してください")

    bu_code = models.ForeignKey(BuTable, on_delete=models.CASCADE, null=False,
                                verbose_name="所属部門", help_text="課が所属する部名を選択してください")

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    社員テーブル AbstractじゃなくてUserテーブルがっつりカスタマイズしたほうが良い気がしてきた
    """
    class Meta:
        verbose_name = "社員情報"
        verbose_name_plural = '社員情報'

    lock = ((0, "正常"), (1, "アカウントロック"))
    lock = models.IntegerField(default=0,
                               verbose_name="アカウントロック", choices=lock)

    err_count = models.IntegerField(default=0,
                                    verbose_name="ログイン失敗回数")

    # emailはデフォルト省略可能だが，WaterDropは省略不可にする
    email = models.EmailField('email address', blank=False)


class BelongsTable(models.Model):
    """
    所属テーブル
    """
    class Meta:
        verbose_name = "所属管理"
        verbose_name_plural = '所属管理'
        unique_together = ("employee", "ka_code")

    id = models.AutoField(primary_key=True,
                          verbose_name="所属コード")

    employee = models.ForeignKey(User, on_delete=models.CASCADE, null=False,
                                 verbose_name="社員番号")
    ka_code = models.ForeignKey(KaTable, on_delete=models.CASCADE, null=True,
                                verbose_name="課コード", help_text="所属課を選択してください")


class HolidayKindTable(models.Model):
    """
    休暇種別テーブル
    """

    class Meta:
        verbose_name = "休暇区分"
        verbose_name_plural = "休暇区分"

    id = models.AutoField(primary_key=True, null=False)

    name = models.CharField(max_length=32,
                            null=False,
                            unique=True,
                            verbose_name="休暇区分名",
                            help_text="土日，祝日，夏季休暇など")

    def __str__(self):
        return self.name


class WorkClassTable(models.Model):
    """
    勤務区分設定テーブル
    """

    class Meta:
        verbose_name = "勤務区分設定"
        verbose_name_plural = "勤務区分設定"

    id = models.BigAutoField(primary_key=True, null=False)

    name = models.CharField(max_length=32, null=False,
                            unique=True,
                            verbose_name="勤務区分名",
                            help_text="一週間単位の出勤日，退勤日を設定します。祝日に関してはカレンダーで設定します")

    # 基本出社時刻
    base_in_time = models.TimeField(null=False, verbose_name="基本出社時刻")

    # 基本退社時刻
    base_off_time = models.TimeField(null=False, verbose_name="基本退社時刻")

    monday = models.ForeignKey(HolidayKindTable,
                               on_delete=models.CASCADE, null=False,
                               verbose_name="月曜日", related_name="monday")

    tuesday = models.ForeignKey(HolidayKindTable,
                                on_delete=models.CASCADE, null=False,
                                verbose_name="火曜日", related_name="tuesday")

    wednesday = models.ForeignKey(HolidayKindTable,
                                  on_delete=models.CASCADE, null=False,
                                  verbose_name="水曜日", related_name="wednesday")

    thursday = models.ForeignKey(HolidayKindTable,
                                 on_delete=models.CASCADE, null=False,
                                 verbose_name="木曜日", related_name="thursday")

    friday = models.ForeignKey(HolidayKindTable,
                               on_delete=models.CASCADE, null=False,
                               verbose_name="金曜日", related_name="friday")

    satday = models.ForeignKey(HolidayKindTable,
                               on_delete=models.CASCADE, null=False,
                               verbose_name="土曜日", related_name="satday")

    sunday = models.ForeignKey(HolidayKindTable,
                               on_delete=models.CASCADE, null=False,
                               verbose_name="日曜日", related_name="sunday")

    def __str__(self):
        return self.name

    def get_id_a(self):
        return str(self.id)


class CalendarTable(models.Model):
    """
    カレンダーテーブル
    """
    class Meta:
        verbose_name = "カレンダー設定"
        verbose_name_plural = 'カレンダー設定'

    id = models.BigAutoField(primary_key=True, null=False)

    name = models.ForeignKey(WorkClassTable, on_delete=models.CASCADE, null=False,
                             verbose_name="カレンダー名", help_text="カレンダー名を選択します")

    date = models.DateField(null=True, unique=True,
                            verbose_name="日付", help_text="休日を指定してください")

    remark = models.CharField(max_length=128, null=True,
                              verbose_name="備考", help_text="祝日名や夏休みなどを記入してください")

    holiday = models.ForeignKey(HolidayKindTable, on_delete=models.CASCADE, null=False,
                                verbose_name="休暇区分", help_text="休暇区分を指定します")

    def __str__(self):
        return str(self.date)

    def get_name(self):
        return self.name


class PersonalWorkStatusTable(models.Model):
    """
    個人出勤ステータステーブル
    """
    class Meta:
        verbose_name = "個人出勤ステータス"
        verbose_name_plural = "個人出勤ステータス"

    id = models.BigAutoField(primary_key=True, null=False)
    name = models.CharField(max_length=128,
                            unique=True,
                            verbose_name="出勤ステータス",
                            help_text="出勤，有休, 慶弔休暇などを作成してください")

    def __str__(self):
        return str(self.name)


class TimeCardTable(models.Model):
    """
    タイムカードテーブル
    """
    class Meta:
        verbose_name = 'タイムカード'
        verbose_name_plural = 'タイムカード'
        unique_together = ("employee", "date")

    id = models.BigAutoField(primary_key=True,
                             null=False)

    date = models.DateField(verbose_name="出社日",
                            null=False,
                            unique=True)

    employee = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 null=False,
                                 verbose_name="社員番号")

    in_time = models.TimeField(null=True,
                               blank=True,
                               verbose_name="出社時間")

    off_time = models.TimeField(null=True,
                                blank=True,
                                verbose_name="退社時間")

    work_class = models.ForeignKey(WorkClassTable,
                                   on_delete=models.CASCADE,
                                   null=False,
                                   default=1,
                                   verbose_name="勤務区分")

    personal_status = models.ForeignKey(PersonalWorkStatusTable,
                                        on_delete=models.CASCADE,
                                        null=True,
                                        verbose_name="出勤のステータスを選択")

    lat = models.FloatField(default=0.0,
                            verbose_name="緯度")

    longi = models.FloatField(default=0.0,
                              verbose_name="経度")


    def __str__(self):
        return str(self.date)


class WorkCodeTable(models.Model):
    """
    作番テーブル
    """
    class Meta:
        verbose_name = "作業番号"
        verbose_name_plural = "作業番号"

    id = models.AutoField(primary_key=True)

    work_code = models.CharField(max_length=32, null=True, unique=True,
                                 verbose_name="作番コード")

    name = models.CharField(max_length=128,
                            verbose_name="作業内容")

    def __str__(self):
        return self.name


class WorkDetailCodeTable(models.Model):
    """
    作業内容テーブル
    """
    class Meta:
        verbose_name = "作業内容"
        verbose_name_plural = "作業内容"

    id = models.AutoField(primary_key=True)

    work_detail_code = models.CharField(max_length=32, unique=True, null=False,
                                        verbose_name="作業コード")

    contents = models.CharField(max_length=512,
                                verbose_name="作業内容の説明")

    def __str__(self):
        return self.contents


class WorkTable(models.Model):
    """
    作業テーブル
    """
    class Meta:
        verbose_name = "作業一覧"
        verbose_name_plural = "作業一覧"

    id = models.BigAutoField(primary_key=True, null=False)

    time_card = models.ForeignKey(TimeCardTable, on_delete=models.CASCADE, null=False)

    work_code = models.ForeignKey(WorkCodeTable, on_delete=models.CASCADE, null=False)

    work_detail_code = models.ForeignKey(WorkDetailCodeTable, on_delete=models.CASCADE, null=False)

    work_time = models.FloatField()

    def __str__(self):
        return self.work_code


class PriceTable(models.Model):
    """
    単価テーブル
    """
    class Meta:
        verbose_name = "単価"
        verbose_name_plural = "単価"

    id = models.BigAutoField(primary_key=True, null=False)

    name = models.CharField(max_length=32, null=False,
                            verbose_name="単価名", help_text="社員の等級を設定します")

    tanka = models.IntegerField(verbose_name="単価", help_text="等級の時給単価を設定します")

    def __str__(self):
        return self.name


class HowToMove(models.Model):
    """
    交通手段
    """
    class Meta:
        verbose_name = "交通手段"
        verbose_name_plural = '交通手段'

    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=128,
                            verbose_name="移動手段", help_text="移動手段を入力します")

    def __str__(self):
        return self.name


class ApproveStatus(models.Model):
    """
    承認ステータス
    """
    class Meta:
        verbose_name = "承認ステータス"
        verbose_name_plural = "承認ステータス"

    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=64, verbose_name="承認ステータス")

    def __str__(self):
        return self.name


class TransportExpense(models.Model):
    """
    交通費
    """
    class Meta:
        verbose_name = "交通費"
        verbose_name_plural = "交通費"

    id = models.BigAutoField(primary_key=True)

    employee_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False,
                                    verbose_name="社員番号")

    date = models.DateField(verbose_name="移動日")

    entry_date = models.DateTimeField(auto_now_add=True, null=True,
                                      verbose_name="申請日")

    expense = models.IntegerField(default=0,
                                  verbose_name="交通費")

    start = models.CharField(max_length=128,
                             verbose_name="出発地")

    end = models.CharField(max_length=128,
                           verbose_name="目的地")

    how = models.ForeignKey(HowToMove, on_delete=models.CASCADE, null=False,
                            verbose_name="交通手段", help_text="交通手段を指定します（電車、タクシーなど)")

    status = models.ForeignKey(ApproveStatus, on_delete=models.CASCADE, null=False,
                               verbose_name="承認ステータス", help_text="承認ステータスを指定します")

    remark = models.CharField(max_length=256, null=False)

    def __str__(self):
        return str(self.date)


class OptionTable(models.Model):
    """
    オプションテーブル
    """
    class Meta:
        verbose_name = "オプション"
        verbose_name_plural = "オプション"

    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=256,
                            verbose_name="オプション名")

    value = models.CharField(max_length=256,
                             verbose_name="値")

    RANGE = ((0, "非公開"), (1, "公開"))
    public = models.IntegerField(choices=RANGE,
                                 verbose_name="公開／非公開")
