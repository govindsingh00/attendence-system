from django.db import models
# Create your models here.

class Admindata(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=100,primary_key=True)
    def __str__(self):
        return self.name

class Studentdata(models.Model):
    stid = models.AutoField(primary_key=True)
    stname = models.CharField(max_length=100)
    fname = models.CharField(max_length=100)
    dob = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    lastquali = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    def __str__(self):
        return self.stname

class Logindata(models.Model):
    email = models.CharField(max_length=100,primary_key=True)
    password = models.CharField(max_length=100)
    usertype = models.CharField(max_length=100)
    def __str__(self):
        return self.email

class Coursedata(models.Model):
    cid = models.AutoField(primary_key=True)
    crname = models.CharField(max_length=100)
    fee = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    remark = models.CharField(max_length=100000)
    def __str__(self):
        return "%s %s" % (self.cid,self.crname)

class StudentCoursedata(models.Model):
    st_crid = models.AutoField(primary_key=True)
    stid = models.CharField(max_length=100)
    crname = models.CharField(max_length=100)
    fee = models.CharField(max_length=100)
    joining = models.CharField(max_length=100)
    remark = models.CharField(max_length=100)
    def __str__(self):
        return "%s %s" % (self.st_crid,self.crname)

class Installmentdata(models.Model):
    tid = models.AutoField(primary_key=True)
    stid = models.CharField(max_length=100)
    stcrid = models.CharField(max_length=100)
    inst = models.CharField(max_length=100)
    sub_date = models.CharField(max_length=100)
    remark = models.CharField(max_length=100)
    def __str__(self):
        return "%s" % (self.tid)

class Photodata(models.Model):
    photo = models.CharField(max_length=100)
    email = models.CharField(max_length=100,primary_key=True)
    def __str__(self):
        return self.email
