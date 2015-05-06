from django.http import HttpResponse;
from django.core.urlresolvers import resolve;
from django.core.urlresolvers import reverse;
import hashlib;
import models;

_PASSWORD_PREFIX = "WWW_AHERN88_CN_VBN12M45S648A6ED";
_PASSWORD_ENDFIX = "74FDG54A3DF4GASD4GA4SD5";

class AdminFilter(object):

    def process_request(self, request):
        if request.path in ['/admin', '/admin/', '/admin/login', '/admin/login/', '/admin/auth', '/admin/auth/','/admin/logout', '/admin/logout/']:
            return;
        if "user" not in request.session:
            return HttpResponse(changePage("/admin/login"), content_type="text/html");
        url_name = resolve(request.path).url_name;
        if "own_url" not in request.session:
            userid = request.session['user_id'];
            sysfunroles = [];
            for m in models.UserRole.objects.filter(user_id=userid).all():
                sysfunroles.extend([models.SystemFunction.objects.get(id=x.systemfunction_id) for x in models.SystemFunctionRole.objects.filter(role_id=m.role_id)]);
            urls = [sysfun.accessurl for sysfun in sysfunroles];
            own_url = ",".join(urls).split(",");
            request.session['own_url'] = own_url;
        else:
            own_url = request.session['own_url'];
        if url_name not in own_url:
            return HttpResponse(changePage("/admin/login"), content_type="text/html");


    def process_view(self ,request, fnc , arg ,kwarg):
        if request.path.find("/admin/") >= 0:
            if "user_id" not in request.session:
                return fnc(request, kwarg);
            userid = request.session['user_id'];
            sysids = [];
            for m in models.UserRole.objects.filter(user_id=userid).all():
                sysids.extend([x.systemfunction_id for x in models.SystemFunctionRole.objects.filter(role_id=m.role_id)]);
            navs = [];
            sysids = set(sysids);
            for p in models.SystemFunction.objects.filter(status=1, ismenu=1, pid=0).all().order_by("orderdisplay", "id"):
                if p.id not in sysids:
                    continue;
                sons = [];
                for s in models.SystemFunction.objects.filter(pid=p.id, status=1, ismenu=1).all().order_by("orderdisplay","id"):
                    if s.id not in sysids:
                        continue;
                    try:
                        urls =[reverse(x) for x in s.accessurl.split(",") if s.accessurl ];
                        s.accessurl = ",".join(urls);
                        sons.append(s);
                    except:
                        print "error: systemfunction where name is %s" % s.name;

                navs.append({"parent": p, "sons": sons});
            try:
                url_name = resolve(request.path).url_name;
                subNav = models.SystemFunction.objects.get(accessurl__contains=url_name);
                bigNav =  models.SystemFunction.objects.get(id=subNav.pid);
                kwarg['nav'] = {"subNav": subNav, "bigNav": bigNav};
            except:
                pass;
            kwarg['navs'] = navs;
            return fnc(request, kwarg);

def md5(password):
    content = _PASSWORD_PREFIX + password + _PASSWORD_ENDFIX;
    return hashlib.md5(content.encode("utf-8")).hexdigest();

def changePage(page):
    return "<script type='text/javascript'>window.location.href='%s';</script>" % page ;