from django.shortcuts import render;
from django.http import HttpResponse;
from django.http import HttpResponseRedirect;
from django.core.urlresolvers import reverse;
from admin import models;
import datetime;
import commons;

# user login
def login(request, data):
	return render(request, 'admin/login.html', data);

def index(request, data):
    return render(request, 'admin/index.html', data);

def auth(request, data):
    username = request.POST['username'];
    password = request.POST['password'];
    try:
        users = models.User.objects.get(username=username.strip(), password=commons.md5(password.strip()));
        users.lastlogintime = datetime.datetime.now();
        users.save();
        request.session['user'] = users.username;
        request.session['user_id'] = users.id;
        return HttpResponseRedirect( reverse("admin.index") );
    except :
        return HttpResponse("error, <a href='javascript:history.go(-1);'>click back</a>");

def logout(request, data):
    if "user" in request.session:
        del request.session['user'];
    if "user_id" in request.session:
        del request.session['user_id'];
    if "own_url" in request.session:
        del request.session['own_url'];
    return HttpResponseRedirect( reverse("login") );

# user info
def userList(request, data):
    search_type = 0;
    if "search_type" in request.POST and "search_value" in request.POST:
        search_type = request.POST['search_type'];
        search_value = request.POST['search_value'];
    if search_type == "1":
        users = models.User.objects.filter(username__contains=search_value, status=1).all().order_by("-id");
    elif search_type == "2":
        users = models.User.objects.filter(status=1,nick__contains=search_value).all().order_by("-id");
    elif search_type == "3":
        users = models.User.objects.filter(status=1,mail__contains=search_value).all().order_by("-id");
    else:
        users = models.User.objects.filter(status=1).all().order_by("-id");
    data['users'] = users;
    return render(request, 'admin/user/list.html', data);

def checkUser(request):
    if request.method == "GET" :
        username = request.GET['username'];
        try:
            models.User.objects.get(username=username.strip(), status=1);
            return HttpResponse("0", content_type="text/plain");
        except:
            return HttpResponse("1", content_type="text/plain");

def addUser(request, data):
    if request.method == "POST" :
        id = request.POST['id'];
        username = request.POST['username'];
        nick = request.POST['nick'];
        password = request.POST['password'];
        mail = request.POST['mail'];
        if id != "":
            user = models.User.objects.get(id=id);
        else :
            user = models.User();
            user.jointime = datetime.datetime.now();
        user.username = username.strip();
        user.nick = nick.strip();
        if password != "":
            user.password = commons.md5(password.strip());
        user.mail = mail.strip();
        user.save();
        return HttpResponseRedirect( reverse("user.list") );
    elif request.method == "GET" :
        if "id" in request.GET :
            id = request.GET['id'];
            user = models.User.objects.get(id=id);
            data['user'] = user;
            return render(request, 'admin/user/add.html', data);
        else:
            return render(request, 'admin/user/add.html', data);

def delUser(request, data):
    if request.method == "GET" :
        id = request.GET['id'];
        try:
            user = models.User.objects.get(id=id);
            user.status = 0;
            user.save();
            return HttpResponse("1", content_type="text/plain");
        except:
            return HttpResponse("0", content_type="text/plain");

# system function
def systemfunctionList(request, data):
    parents = models.SystemFunction.objects.filter(pid=0).all().order_by("orderdisplay", "id");
    subs = [];
    for p in parents:
        subs.append({"parent": p, "son": models.SystemFunction.objects.filter(pid=p.id).all().order_by("orderdisplay","id")});
    data['subsystemfuns'] = subs;
    return render(request, 'admin/systemfunction/list.html', data);

def addSystemfunction(request,data):
    if request.method == "POST" :
        id = request.POST['id'];
        name = request.POST['name'];
        url = request.POST['url'];
        accessurl = request.POST['accessurl'];
        orderdisplay = request.POST['orderdisplay'];
        pid = request.POST['pid'];
        icon = request.POST['icon'];
        status = request.POST['status'];
        if "ismenu" in request.POST:
            ismenu = request.POST['ismenu'];
        else:
            ismenu = 0;
        if id != "":
            sysfunction = models.SystemFunction.objects.get(id=id);
        else :
            sysfunction = models.SystemFunction();
        sysfunction.name = name.strip();
        sysfunction.url = url.strip();
        sysfunction.accessurl = accessurl.strip();
        sysfunction.orderdisplay = orderdisplay.strip();
        sysfunction.pid = pid.strip();
        sysfunction.ismenu = ismenu;
        sysfunction.icon = icon;
        sysfunction.status = int(status);
        sysfunction.save();
        return HttpResponseRedirect( reverse("systemfunction.list") );
    else:
        if "id" in request.GET :
            id = request.GET['id'];
            systemfunction = models.SystemFunction.objects.get(id=id);
            data['systemfunction'] = systemfunction;
            return render(request, 'admin/systemfunction/add.html', data);
        else:
            return render(request, 'admin/systemfunction/add.html', data);

def delSystemfunction(request, data):
    if request.method == "GET" :
        id = request.GET['id'];
        try:
            sysfun = models.SystemFunction.objects.get(id=id);
            sysfun.delete();
            return HttpResponse("1", content_type="text/plain");
        except:
            return HttpResponse("0", content_type="text/plain");

def bindSystemfunction(request, data):
    if request.method == "GET" :
        id = request.GET['id'];
        parents = models.SystemFunction.objects.filter(pid=0,status=1).all().order_by("orderdisplay", "id");
        subs = [];
        for p in parents:
            subs.append({"parent": p, "son": models.SystemFunction.objects.filter(pid=p.id,status=1).all().order_by("orderdisplay","id")});
        data['subsystemfuns'] = subs;
        data['role'] = models.Role.objects.get(id=id);
        data['checked'] = [ x.systemfunction_id for x in models.SystemFunctionRole.objects.filter(role_id=id).all() ];
        return render(request, 'admin/systemfunction/bind.html', data);
    else:
        values = [k.replace("systemfun_","") for k,v in request.POST.iteritems() if k.find("systemfun_") >= 0];
        sysroles = [];
        models.SystemFunctionRole.objects.filter(role_id=request.POST['role_id']).all().delete();
        for v in values:
            sysrole = models.SystemFunctionRole();
            sysrole.role_id = request.POST['role_id'];
            sysrole.systemfunction_id = v;
            sysroles.append(sysrole);
        models.SystemFunctionRole.objects.bulk_create(sysroles);
        return HttpResponseRedirect( reverse("systemfunction.bindRole") + "?id=" + request.POST['role_id']);


# role view function
def roleList(request, data):
    parents = models.Role.objects.filter(pid=0,status=1).all().order_by("orderdisplay", "id");
    subs = [];
    for p in parents:
        subs.append({"parent": p, "son": models.Role.objects.filter(pid=p.id, status=1).all().order_by("orderdisplay","id")});
    data['roles'] = subs;
    return render(request, 'admin/role/list.html', data);

def addRole(request,data):
    if request.method == "POST" :
        id = request.POST['id'];
        name = request.POST['name'];
        orderdisplay = request.POST['orderdisplay'];
        pid = request.POST['pid'];
        status = request.POST['status'];
        if id != "":
            role = models.Role.objects.get(id=id);
        else :
            role = models.Role();
        role.name = name.strip();
        role.orderdisplay = orderdisplay.strip();
        role.pid = pid.strip();
        role.status = int(status);
        role.save();
        return HttpResponseRedirect( reverse("role.list") );
    else:
        if "id" in request.GET :
            id = request.GET['id'];
            role = models.Role.objects.get(id=id);
            data['role'] = role;
            return render(request, 'admin/role/add.html', data);
        else:
            return render(request, 'admin/role/add.html', data);

def delRole(request, data):
    if request.method == "GET" :
        id = request.GET['id'];
        try:
            role = models.Role.objects.get(id=id);
            role.delete();
            return HttpResponse("1", content_type="text/plain");
        except:
            return HttpResponse("0", content_type="text/plain");

def bindRole(request, data):
    if request.method == "GET" :
        id = request.GET['id'];
        parents = models.Role.objects.filter(pid=0,status=1).all().order_by("orderdisplay", "id");
        subs = [];
        for p in parents:
            subs.append({"parent": p, "son": models.Role.objects.filter(pid=p.id,status=1).all().order_by("orderdisplay","id")});
        data['roles'] = subs;
        data['user'] = models.User.objects.get(id=id);
        data['checked'] = [ x.role_id for x in models.UserRole.objects.filter(user_id=id).all() ];
        return render(request, 'admin/role/bind.html', data);
    else:
        values = [k.replace("role_","") for k,v in request.POST.iteritems() if k.find("role_") >= 0];
        userroles = [];
        models.UserRole.objects.filter(user_id=request.POST['user_id']).all().delete();
        for v in values:
            userrole = models.UserRole();
            userrole.user_id = request.POST['user_id'];
            userrole.role_id = v;
            userroles.append(userrole);
        models.UserRole.objects.bulk_create(userroles);
        return HttpResponseRedirect( reverse("role.bindUser") + "?id=" + request.POST['user_id']);

def test(request, data):
    return render(request, 'admin/index.html', data);