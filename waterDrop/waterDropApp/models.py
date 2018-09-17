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
class UserManager(BaseUserManager):
    def create_user(self, employ_number, password=None, **extra_fields):
        if not employ_number:
            raise ValueError('Users must have a email address')
            #employ_number = UserManager.normalize_email(employ_number)
        user = self.model(employ_number=employ_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, employ_number, password):
        return self.create_user(employ_number, password)


class User(AbstractBaseUser):
    employ_number = models.CharField(max_length=32, primary_key=True, null=False)
    kaCode = models.CharField(max_length=32, null=False,default="0000")


    USERNAME_FIELD = 'employ_number'

    objects = UserManager()

    class Meta:
        db_table = 'waterdropapp_user'
        swappable = 'AUTH_USER_MODEL'

'''
class User(AbstractUser):
    class Meta:
        verbose_name = "社員情報"
        verbose_name_plural = '社員情報'

    kaCode = models.ForeignKey(KaTable, on_delete=models.CASCADE, null=True, verbose_name="課コード", help_text="所属課を選択してください")


'''単にこれは課に属することを表すテーブルだからイマイチ価値がない'''
'''やっぱり継承するかカスタムするかのどっちかだな・・・
class SyainTable(models.Model):
    class Meta:
        verbose_name = "社員所属課情報"
        verbose_name_plural = '社員所属課情報'

    #複数課に所属するときはどうするべかな
    kaCode = models.ForeignKey(KaTable, on_delete=models.CASCADE, null=False, verbose_name="所属課", help_text="社員が所属する課を選択してください")
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="社員ナンバー", help_text="社員ナンバーを選択してください")

    def __str__(self):
        return str(self.user)
'''
'''
タイムカードテーブル
'''
class TimeCardTable(models.Model):
    '''このテーブルは別のページで編集できるようにする'''
    class Meta:
        verbose_name = "タイムカード"
        verbose_name_plural = 'タイムカード'

    id = models.BigAutoField(primary_key=True, null=False)
    day = models.DateField(null=False)
    employ_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, verbose_name="社員番号")
    start = models.TimeField(verbose_name="出社時間")
    end = models.TimeField(verbose_name="退社時間")

    def __str__(self):
        return str(self.day)

'''
作番テーブル
'''
class WorkCodeTable(models.Model):
    work_code = models.CharField(max_length=32, primary_key=True, null=False)
    name = models.CharField(max_length=128)

'''
作業内容テーブル
'''
class WorkDetailCodeTable(models.Model):
    work_detail_code = models.CharField(max_length=32, primary_key=True, null=False)
    contents = models.CharField(max_length=512)

'''
作業テーブル
'''
class WorkTable(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    time_card_id = models.ForeignKey(TimeCardTable, on_delete=models.CASCADE, null=False)
    work_code = models.ForeignKey(WorkCodeTable, on_delete=models.CASCADE, null=False)
    work_detail_code = models.ForeignKey(WorkDetailCodeTable, on_delete=models.CASCADE, null=False)
    work_time = models.FloatField()

'''
単価テーブル
'''
class PriceTable(models.Model):
    tanka_id = models.BigAutoField(primary_key=True, null=False)
    name = models.CharField(max_length=32, null=False)
    tanka = models.FloatField()

'''
区分テーブル
'''
class KubunTable(models.Model):
    kubunid = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=32, null=False)
    div = models.FloatField()

'''
カレンダーテーブル
'''
class CalendarTable(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    name = models.CharField(max_length=32, null=False)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    kubunid = models.ForeignKey(KubunTable, on_delete=models.CASCADE, null=False)

'''
明細テーブル
'''
class MeisaiTable(models.Model):
    id = models.BigAutoField(primary_key=True)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    calendar_id = models.ForeignKey(CalendarTable, on_delete=models.CASCADE, null=False)
    employ_number = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    tana_id = models.ForeignKey(PriceTable, on_delete=models.CASCADE, null=False)