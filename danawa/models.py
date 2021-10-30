from django.db import models


# Create your models here.
class Company(models.Model):
    co_id = models.AutoField(primary_key=True, db_column="CO_ID")
    co_kor_name = models.CharField(max_length=100, db_column="CO_KOR_NAME")
    co_eng_name = models.CharField(max_length=100, db_column="CO_ENG_NAME")

    class Meta:
        managed = False
        db_table = "COMPANY"
