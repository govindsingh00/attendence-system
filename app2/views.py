from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import *
from django.core.files.storage import FileSystemStorage
import os
import time

# Create your views here.
def login(request):
    if request.method == "POST":
        em=request.POST["T1"]
        paswrd=request.POST["T2"]
        obj = Logindata.objects.get(email=em,password=paswrd)
        ut=obj.usertype
        request.session["ut"]=ut
        request.session["email"]=em
        if ut=="admin":
            return HttpResponseRedirect("/admin_home/")
        elif ut=="student":
            return HttpResponseRedirect("/student_home/")
        elif ut=="teacher":
            return HttpResponseRedirect("/teacher_home/")
        else:
            return render(request, "Login.html",{"msg":"Either Email or Password is Incorrect"})
    else:
        return render(request,"Login.html")

def logout(request):
    try:
        del request.session["email"]
        del request.session["ut"]
    except:
        pass
    return HttpResponseRedirect("/")

def autherror(request):
    return render(request,"AuthError.html")

def admin_reg(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut == "admin":
            if request.method=="POST":
                adm = Admindata()
                lgn = Logindata()

                nm=request.POST["t1"]
                a=request.POST["t2"]
                b=request.POST["t3"]
                c=request.POST["t4"]
                d=request.POST["t5"]
                e=request.POST["t6"]
                add=a+" "+b+" "+c+" "+d+" "+e
                mob=request.POST["t7"]
                em=request.POST["t8"]
                paswrd=request.POST["t9"]

                adm.name = nm
                adm.email = em
                adm.contact = mob
                adm.address = add

                lgn.email = em
                lgn.password = paswrd
                lgn.usertype = "admin"

                adm.save()
                lgn.save()
                return render(request,"AdminReg.html",{"msg":"Data Saved"})
            else:
                return render(request,"AdminReg.html")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")


def student_reg(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut != "student":
            if request.method=="POST":
                st = Studentdata()
                lgn = Logindata()

                a=request.POST["t1"]
                b=request.POST["t2"]
                nm=a+" "+b
                fnm=request.POST["t111"]
                dob=request.POST["t3"]
                gender=request.POST["R1"]
                c=request.POST["t4"]
                d=request.POST["t5"]
                e=request.POST["t6"]
                f=request.POST["t7"]
                g=request.POST["t8"]
                add = c +" "+ d +" "+ e+" "+f+" "+g
                lq=request.POST["t9"]
                mob=request.POST["t222"]
                em=request.POST["t11"]
                pswrd=request.POST["t12"]

                st.stname= nm
                st.fname= fnm
                st.dob = dob
                st.gender = gender
                st.address = add
                st.lastquali = lq
                st.contact = mob
                st.email = em

                lgn.email = em
                lgn.password = pswrd
                lgn.usertype = "student"

                st.save()
                lgn.save()

                return render(request,"StudentReg.html",{"msg":"Data Saved"})
            else:
                return render(request, "StudentReg.html" )
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def teacher_reg(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]

        if ut == "admin":
            courses = Coursedata.objects.all()

            if request.method == "POST":
                t = Teacherdata()
                lgn = Logindata()
                ph = Photodata()

                nm = request.POST["t1"] + " " + request.POST["t2"]
                add = request.POST["t5"] + " " + request.POST["t6"] + " " + request.POST["t7"] + " " + request.POST["t8"] + " " + request.POST["t9"]

                em = request.POST["t11"]

                t.name = nm
                t.crid = request.POST["t3"]
                t.email = em
                t.phone = request.POST["t10"]
                t.gender = request.POST["R1"]
                t.dob = request.POST["t4"]
                t.address = add

                lgn.email = em
                lgn.password = request.POST["t12"]
                lgn.usertype = "teacher"

                # ✅ Photo Handling
                file = request.FILES["photo"]
                import os
                from django.conf import settings

                filepath = os.path.join(settings.MEDIA_ROOT, file.name)
                with open(filepath, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                ph.email = em
                ph.photo = file.name

                t.save()
                lgn.save()
                ph.save()

                return render(request, "TeacherReg.html", {"msg": "Teacher Registered Successfully", "courses": courses})
            else:
                return render(request, "TeacherReg.html", {"courses": courses})
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def admin_home(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        em = request.session["email"]
        if ut == "admin":
            adm = Admindata.objects.filter(email=em)
            pic = Photodata.objects.filter(email=em)
            return render(request,"AdminHome.html",{"data":adm,"data1":pic})
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def teacher_home(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        em = request.session["email"]

        if ut == "teacher":
            tchr = Teacherdata.objects.filter(email=em)
            pic = Photodata.objects.filter(email=em)

            return render(request, "TeacherHome.html", {"data": tchr, "data1": pic})
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def editadminprofile(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        em = request.session["email"]
        if ut == "admin":
            admin = Admindata.objects.filter(email=em)
            return render(request, "EditAdmin.html", {"data": admin})
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def editadminprofile1(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut == "admin":
            if request.method == "POST":
                nm = request.POST["t1"]
                ad = request.POST["t2"]
                mob = request.POST["t3"]
                em = request.POST["t4"]

                data = Admindata.objects.get(email=em)

                data.name = nm
                data.address = ad
                data.contact = mob

                data.save()
                return render(request, "EditAdmin.html", {"msg": "Profile Updated Successfully"})
            else:
                return HttpResponseRedirect("/admin_home/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def admin_pass_change(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        em = request.session["email"]
        if ut == "admin":
            data = Logindata.objects.filter(email=em)
            return render(request, "AdminPassChange.html", {"data":data})
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def admin_pass_change1(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        em = request.session["email"]
        if ut == "admin":
            if request.method == "POST":
                old = request.POST["t1"]
                new = request.POST["t2"]
                ACC = Logindata.objects.get(email=em,password=old)
                ACC.password = new
                ACC.save()
                return render(request, "AdminPassChange.html", {"msg":"PASSWORD CHANGED"})
            else:
                return HttpResponseRedirect("/admin_home/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def student_home(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        em = request.session["email"]
        if ut == "student":
            std = Studentdata.objects.filter(email=em)
            pic = Photodata.objects.filter(email=em)
            return render(request,"StudentHome.html",{"data":std,"data1":pic})
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def editstprofile(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut == "student":
            if request.method == "POST":
                sid = request.POST["S1"]
                std = Studentdata.objects.filter(stid=sid)
                if ut == "admin":
                    return render(request,"EditStudentad.html",{"data":std})

                elif ut == "student":
                    return render(request, "EditStudent.html", {"data": std})
            else:
                return HttpResponseRedirect("/student_home/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def editstprofile1(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut == "student":
            if request.method == "POST":
                sid = request.POST["t1"]
                add = request.POST["t6"]
                cont = request.POST["t8"]

                std = Studentdata.objects.get(stid=sid)

                std.address = add
                std.contact = cont

                std.save()
                if ut == "admin":
                    return render(request, "EditStudentad.html", {"msg": "details edited Successfully"})

                elif ut == "student":
                    return render(request, "EditStudent.html", {"msg": "details edited Successfully"})
            else:
                return HttpResponseRedirect("/student_home/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def student_pass_change(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut == "student":
            if request.method=="POST":
                sid = request.POST["S1"]
                stdata = Studentdata.objects.filter(stid=sid)
                return render(request,"StudentPassChange.html",{"data":stdata})
            else:
                return HttpResponseRedirect("/student_home/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def student_pass_change1(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut == "student":
            if request.method=="POST":
                em = request.POST["E1"]
                old = request.POST["t1"]
                new = request.POST["t2"]
                stdata = Logindata.objects.get(email=em,password=old)
                stdata.password = new
                stdata.save()
                return render(request,"StudentPassChange.html",{"msg":"Password Changed Successfully"})
            else:
                return HttpResponseRedirect("/student_home/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def course_reg(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut == "admin":
            if request.method == "POST":
                crse = Coursedata()
                cr = request.POST["t1"]
                fee = request.POST["t2"]
                dr = request.POST["t3"]
                rmk = request.POST["t4"]

                crse.crname = cr.upper()
                crse.fee = fee
                crse.duration = dr
                crse.remark = rmk

                crse.save()
                return render(request, "CourseReg.html",{"msg":"Course Registered Succesfully"})
            else:
                return render(request, "CourseReg.html")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def allcourses(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut=="admin":
            crdt = Coursedata.objects.all()
            return render(request,"AllCourses.html",{"data":crdt})
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def edit_course(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut == "admin":
            if request.method == "POST":
                crseid=request.POST["C1"]
                crdata = Coursedata.objects.filter(cid=crseid)
                return render(request,"EditCourse.html",{"data":crdata})
            else:
                return HttpResponseRedirect("/allcourses/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def edit_course1(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut == "admin":
            if request.method == "POST":
                crseid=request.POST["C1"]
                nm = request.POST["t1"]
                fee = request.POST["t2"]
                dr = request.POST["t3"]
                rm = request.POST["t4"]

                crdata = Coursedata.objects.get(cid=crseid)

                crdata.crname = nm
                crdata.fee = fee
                crdata.duration = dr
                crdata.remark = rm

                crdata.save()

                return render(request,"EditCourse.html",{"mssg":"Course Updated Successfully"})
            else:
                return HttpResponseRedirect("/allcourses/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def delete_course(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut == "admin":
            if request.method == "POST":
                crseid=request.POST["C1"]
                crdata = Coursedata.objects.filter(cid=crseid)
                return render(request,"DeleteCourse.html",{"data":crdata})
            else:
                return HttpResponseRedirect("/allcourses/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def delete_course1(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut == "admin":
            if request.method == "POST":
                crseid=request.POST["C1"]

                crdata = Coursedata.objects.get(cid=crseid)

                crdata.delete()

                return render(request,"DeleteCourse.html",{"mssg":"Course Deleted Successfully"})
            else:
                return HttpResponseRedirect("/allcourses/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def alladmins(request):
    records = Admindata.objects.all()
    photo = Photodata.objects.all()
    return render(request,'AllAdmins.html',{"data":records,"photo":photo})

def allteachers(request):
    records = Teacherdata.objects.all()
    data = []

    for t in records:
        try:
            p = Photodata.objects.get(email=t.email)
            photo = p.photo
        except:
            photo = None

        data.append({
            "teacher": t,
            "photo": photo
        })

    return render(request, 'AllTeachers.html', {"data": data})

# for photo
def uploadphoto(request):
    if request.session.has_key("email"):
        em = request.session["email"]
        ut = request.session["ut"]
        if request.method == "POST":
            file=request.FILES["F1"]
            path = os.path.basename(file.name)
            file_ext = os.path.splitext(path)[1][1:]
            filename = str(int(time.time()))+'.'+file_ext

            fs = FileSystemStorage()

            fs.save(filename, file)

            obj = Photodata()

            obj.email = em
            obj.photo = filename
            obj.save()

            if(ut=="admin"):
                return HttpResponseRedirect("/admin_home/")
            elif(ut=="teacher"):
                return HttpResponseRedirect("/teacher_home/")

        else:

            return render(request,"UploadPhoto.html")

    else:
        return HttpResponseRedirect("/autherror/")

def chngephoto(request):
    if request.session.has_key("email"):
        em = request.session["email"]
        ut = request.session["ut"]
        if request.method == "POST":
            pic = request.POST["C1"]
            dlt = Photodata.objects.filter(photo=pic,email=em)
            return render(request, "ChangePhoto.html",{"data":dlt})
        else:
            return HttpResponseRedirect("/admin_home/")
    else:
        return HttpResponseRedirect("/autherror/")

def chngephoto1(request):
    if request.session.has_key("email"):
        em = request.session["email"]
        ut = request.session["ut"]
        if request.method == "POST":
            fs1 = FileSystemStorage()
            old = request.POST["IMG1"]
            pic = Photodata.objects.get(photo=old,email=em)
            picname = pic.photo
            fs1.delete(picname)

            file=request.FILES["F1"]
            path = os.path.basename(file.name)
            file_ext = os.path.splitext(path)[1][1:]
            filename = str(int(time.time()))+'.'+file_ext
            fs = FileSystemStorage()
            fs.save(filename, file)

            pic.photo = filename
            pic.save()
            if ut=="admin":
                return HttpResponseRedirect("/admin_home/")

            elif ut=="student":
                return HttpResponseRedirect("/student_home/")
        else:
            if ut=="admin":
                return render(request,"ChangePhoto.html")

    else:
        return HttpResponseRedirect("/autherror/")

def deletephoto(request):
    if request.session.has_key("email"):
        em = request.session["email"]
        ut = request.session["ut"]
        if request.method == "POST":
            pic = request.POST["C1"]
            dlt = Photodata.objects.filter(photo=pic,email=em)
            if ut=="admin":
                return render(request, "DeletePhoto.html",{"data":dlt})

        else:
            return HttpResponseRedirect("/admin_home/")
    else:
        return HttpResponseRedirect("/autherror/")

def deletephoto1(request):
    if request.session.has_key("email"):
        em = request.session["email"]
        ut = request.session["ut"]
        if request.method == "POST":
            fs1 = FileSystemStorage()
            old = request.POST["IMG1"]
            pic = Photodata.objects.get(photo=old,email=em)
            picname = pic.photo
            fs1.delete(picname)
            pic.delete()
            if ut=="admin":
                return HttpResponseRedirect("/admin_home/")

            elif ut=="student":
                return HttpResponseRedirect("/student_home/")
        else:
            if ut=="admin":
                return render(request,"ChangePhoto.html")

    else:
        return HttpResponseRedirect("/autherror/")

# for student
def student_course_info(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut == "student":
            if request.method=="POST":
                sid = request.POST["S1"]
                stcrse = StudentCoursedata.objects.filter(stid=sid)
                stinstall = Installmentdata.objects.filter(stid=sid)
                list = []
                crf = 0
                crinst = 0
                for d1 in stcrse:
                    crf=crf+int(d1.fee)
                list.append(crf)
                for d2 in stinstall:
                    crinst = crinst + int(d2.inst)
                due = crf-crinst
                list.append(crinst)
                list.append(due)
                return render(request,"StudentCourseInfo.html",{"data1":stcrse,"data2":stinstall,"data3":list})
            else:
                return HttpResponseRedirect("/student_home/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

# for student by admin
def studentuploadphoto(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut != "student":
            if request.method == "POST":
                file = request.FILES["F1"]
                em = request.POST["E1"]

                path = os.path.basename(file.name)
                file_ext = os.path.splitext(path)[1][1:]
                filename = str(int(time.time())) + '.' + file_ext
                fs = FileSystemStorage()
                fs.save(filename, file)
                obj = Photodata()
                obj.email = em
                obj.photo = filename
                obj.save()
                if ut == "admin":
                    return HttpResponseRedirect("/allstudentsAD/")
                else:
                    return HttpResponseRedirect("/allstudentsACC/")
            else:
                return HttpResponseRedirect("/allstudentsAD/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def studentchngephoto(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut != "student":
            if request.method == "POST":
                pic = request.POST["C1"]
                em = request.POST["C2"]
                dlt = Photodata.objects.filter(photo=pic, email=em)

                if ut == "admin":
                    return render(request, "ChangePhotoStudent1.html", {"data": dlt})
            else:
                if ut == "admin":
                    return HttpResponseRedirect("/allstudentsAD/")

        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def studentchngephoto1(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut != "student":
            if request.method == "POST":
                fs1 = FileSystemStorage()
                old = request.POST["IMG1"]
                em = request.POST["E1"]
                pic = Photodata.objects.get(photo=old, email=em)
                picname = pic.photo
                fs1.delete(picname)

                file = request.FILES["F1"]
                path = os.path.basename(file.name)
                file_ext = os.path.splitext(path)[1][1:]
                filename = str(int(time.time())) + '.' + file_ext
                fs = FileSystemStorage()
                fs.save(filename, file)
                pic.photo = filename
                pic.save()
                if ut == "admin":
                    return HttpResponseRedirect("/allstudentsAD/")

            else:
                if ut=="admin":
                    return HttpResponseRedirect("/allstudentsAD/")

        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def studentdeletephoto(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut !="student":
            if request.method == "POST":
                pic = request.POST["C1"]
                em = request.POST["C2"]
                dlt = Photodata.objects.filter(photo=pic,email=em)
                return render(request, "DeletePhotoStudent.html",{"data":dlt})
            else:
                if ut=="admin":
                    return HttpResponseRedirect("/allstudentsAD/")

        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def studentdeletephoto1(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut != "student":
            if request.method == "POST":
                fs1 = FileSystemStorage()
                old = request.POST["IMG1"]
                em = request.POST["E1"]
                pic = Photodata.objects.get(photo=old,email=em)
                picname = pic.photo
                fs1.delete(picname)
                pic.delete()
                if ut=="admin":
                    return HttpResponseRedirect("/allstudentsAD/")
                else:
                    return HttpResponseRedirect("/allstudentsACC/")
            else:
                return render(request,"ChangePhoto.html")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def ADviewstudent(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut=="admin":
            if request.method == "POST":
                sid = request.POST["S1"]
                em = request.POST["S2"]

                pic = Photodata.objects.filter(email=em)
                stprofile = Studentdata.objects.filter(stid=sid)
                stcrse = StudentCoursedata.objects.filter(stid=sid)
                stinstall = Installmentdata.objects.filter(stid=sid)
                list = []
                crf = 0
                crinst = 0
                for d1 in stcrse:
                    crf = crf + int(d1.fee)
                list.append(crf)
                for d2 in stinstall:
                    crinst = crinst + int(d2.inst)
                due = crf - crinst
                list.append(crinst)
                list.append(due)
                return render(request,"ADviewstudent.html",{"data1":stprofile,"data2":stcrse,"data3":stinstall,"data4":pic,"data5":list})
            else:
                return HttpResponseRedirect("/admin_home/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def deletestudentprofile(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut=="admin":
            if request.method == "POST":
                sid = request.POST["S1"]
                em = request.POST["S2"]
                try:
                    data1 = Studentdata.objects.filter(stid=sid, email=em)
                    data2 = StudentCoursedata.objects.filter(stid=sid)
                    data3 = Installmentdata.objects.filter(stid=sid)
                    data4 = Photodata.objects.filter(email=em)
                    return render(request,"DeleteStudentProfile.html",{"data1":data1,"data2":data2,"data3":data3,"data4":data4,})
                except:
                    return render(request, "DeleteStudentProfile.html",
                                  {"msg":"No Data FOUND"})
            else:
                return HttpResponseRedirect("/allstudentsAD/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def deletestudentprofile1(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut=="admin":
            if request.method == "POST":
                sid = request.POST["S1"]
                em = request.POST["S2"]
                data1 = Studentdata.objects.get(stid=sid,email=em)
                data2 = Logindata.objects.get(email=em)
                data3 = StudentCoursedata.objects.filter(stid=sid)
                data4 = Installmentdata.objects.filter(stid=sid)

                data1.delete()
                data2.delete()
                if data3:
                    data3.delete()
                if data4:
                    data4.delete()

                old = request.POST["IMG1"]
                if old:
                    fs1 = FileSystemStorage()
                    pic = Photodata.objects.get(photo=old, email=em)
                    picname = pic.photo
                    fs1.delete(picname)
                    pic.delete()
                return render(request,"DeleteStudentProfile.html",{"msg":"Student All Data Deleted Succeffully"})
            else:
                return HttpResponseRedirect("/allstudentsAD/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def allstudentsAD(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut=="admin":
            stdata = Studentdata.objects.all()
            return render(request,"AllStudentsAD.html",{"data":stdata})
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def studentcourseadd(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut == "admin":
            if request.method=="POST":
                obj = Coursedata.objects.all()
                list=[]
                sid = request.POST["A1"]
                list.append(sid)
                return render(request,"StudentCourseregADMIN.html",{"data":obj,"data1":list})
            else:
                return HttpResponseRedirect("/ADviewstudent/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def studentcourseadd1(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut == "admin":
            if request.method=="POST":
                sid = request.POST["A1"]
                crnm = request.POST["t1"]
                fee = request.POST["t2"]
                joind = request.POST["t3"]
                rmk = request.POST["t4"]

                obj = StudentCoursedata()
                obj.crname = crnm
                obj.fee = fee
                obj.joining = joind
                obj.remark = rmk
                obj.stid = sid

                obj.save()

                return render(request,"StudentCourseregADMIN.html",{"msg":"Course Added in Student Profile"})
            else:
                return HttpResponseRedirect("/ADviewstudent/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def studentinstallmentadd(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut == "admin":
            if request.method=="POST":
                sid = request.POST["A1"]
                crid = request.POST["A2"]
                obj = StudentCoursedata.objects.filter(stid=sid,st_crid=crid)
                return render(request,"AddInstallmentAdmin.html",{"data":obj})
            else:
                return HttpResponseRedirect("/ADviewstudent/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def studentinstallmentadd1(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut == "admin":
            if request.method=="POST":
                sid = request.POST["A1"]
                crid = request.POST["A2"]
                am = request.POST["t1"]
                dt = request.POST["t2"]
                rmk = request.POST["t3"]

                obj = Installmentdata()
                obj.stid = sid
                obj.stcrid = crid
                obj.inst = am
                obj.sub_date = dt
                obj.remark = rmk

                obj.save()

                return render(request,"AddInstallmentAdmin.html",{"msg":"Installment Added"})

            else:
                return HttpResponseRedirect("/ADviewstudent/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def editstudentcoursedata(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut == "admin":
            if request.method=="POST":
                stid = request.POST["A1"]
                crid = request.POST["A2"]
                crdata = StudentCoursedata.objects.filter(st_crid=crid,stid=stid)
                allcrse = Coursedata.objects.all()
                return render(request,"EditStudentCourseData.html",{"data":crdata,"data1":allcrse})
            else:
                return HttpResponseRedirect("/ADviewstudent/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def editstudentcoursedata1(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut == "admin":
            if request.method=="POST":
                crid = request.POST["T1"]
                stid = request.POST["T2"]
                crse = request.POST["T3"]
                fee = request.POST["T4"]
                dt = request.POST["T5"]
                rmk = request.POST["T6"]

                data = StudentCoursedata.objects.get(st_crid=crid,stid=stid)

                data.crname = crse
                data.fee = fee
                data.joining = dt
                data.remark = rmk

                data.save()
                return render(request,"EditStudentCourseData.html",{"msg":"Course Updated Successfully"})
            else:
                return HttpResponseRedirect("/ADviewstudent/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def deletestudentcoursedata(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut == "admin":
            if request.method=="POST":
                stid = request.POST["A1"]
                crid = request.POST["A2"]
                crdata = StudentCoursedata.objects.filter(st_crid=crid,stid=stid)
                return render(request,"DeleteStudentCourseData.html",{"data":crdata})
            else:
                return HttpResponseRedirect("/ADviewstudent/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def deletestudentcoursedata1(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut == "admin":
            if request.method=="POST":
                crid = request.POST["T1"]
                stid = request.POST["T2"]
                crdata = StudentCoursedata.objects.filter(st_crid=crid, stid=stid)
                trdata = Installmentdata.objects.filter(stcrid=crid, stid=stid)

                crdata.delete()
                trdata.delete()

                return render(request, "DeleteStudentCourseData.html", {"msg": "Course Data Deleted Successfully"})
            else:
                return HttpResponseRedirect("/ADviewstudent/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def editstudentinstdata(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut == "admin":
            if request.method=="POST":
                tid = request.POST["T1"]
                trndata = Installmentdata.objects.filter(tid=tid)
                return render(request,"EditStudentInstallment.html",{"data":trndata})
            else:
                return HttpResponseRedirect("/ADviewstudent/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def editstudentinstdata1(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut == "admin":
            if request.method=="POST":
                trid = request.POST["T1"]
                amnt = request.POST["T2"]
                dt = request.POST["T3"]
                rmk = request.POST["T4"]

                data = Installmentdata.objects.get(tid=trid)

                data.inst = amnt
                data.sub_date = dt
                data.remark = rmk

                data.save()
                return render(request,"EditStudentInstallment.html",{"msg":"Transection Updated Successfully"})
            else:
                return HttpResponseRedirect("/ADviewstudent/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def deletestudentinstdata(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut == "admin":
            if request.method=="POST":
                trid = request.POST["T1"]
                trdata = Installmentdata.objects.filter(tid=trid)
                return render(request,"DeleteStudentInstallment.html",{"data":trdata})
            else:
                return HttpResponseRedirect("/ADviewstudent/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def deletestudentinstdata1(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut == "admin":
            if request.method=="POST":
                trid = request.POST["T1"]

                trdata = Installmentdata.objects.filter(tid=trid)

                trdata.delete()

                return render(request, "DeleteStudentInstallment.html", {"msg": "Transection Deleted Successfully"})
            else:
                return HttpResponseRedirect("/ADviewstudent/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def editstdata(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut != "student":
            if request.method=="POST":
                stid = request.POST["STID1"]
                stdata = Studentdata.objects.filter(stid=stid)
                if ut == "admin":
                    return render(request,"EditStDataad.html",{"data":stdata})

            else:
                if ut == "admin":
                    return HttpResponseRedirect("/ADviewstudent/")
                else:
                    return HttpResponseRedirect("/allstudentsACC/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")

def editstdata1(request):
    if request.session.has_key("email"):
        ut = request.session["ut"]
        if ut != "student":
            if request.method=="POST":
                sid = request.POST["T1"]
                nm = request.POST["T2"]
                fnm = request.POST["T3"]
                dob = request.POST["T4"]
                gndr = request.POST["T5"]
                add = request.POST["T6"]
                quali = request.POST["T7"]
                mob = request.POST["T8"]
                em = request.POST["T9"]

                data = Studentdata.objects.get(stid=sid)

                data.stname = nm
                data.fname  = fnm
                data.dob = dob
                data.gender = gndr
                data.address = add
                data.lastquali = quali
                data.contact = mob
                data.email = em

                data.save()
                if ut == "admin":
                    return render(request,"EditStDataad.html",{"msg":"Student Data Updated Successfully"})

            else:
                if ut == "admin":
                    return HttpResponseRedirect("/ADviewstudent/")
                else:
                    return HttpResponseRedirect("/viewstudentACC/")
        else:
            return HttpResponseRedirect("/autherror/")
    else:
        return HttpResponseRedirect("/autherror/")
