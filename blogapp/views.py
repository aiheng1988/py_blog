from django.http import HttpResponseRedirect;
from django.http import HttpResponse;
from django.shortcuts import render;
from django.core.urlresolvers import reverse;
import models;
import os,time;
from datetime import datetime;

_PAGE_SIZE = 15;
def uploadJson(request, data):
    if request.method == "POST":
        try:
            filename = handle_uploaded_file(request.FILES['imgFile'], request.GET['dir']);
            json_data = '{"error": 0, "url": "/static/upload/image/%s"}' % filename;
        except:
            json_data = '{"error": 1, "message": "upload error"}';
        print json_data;
    return HttpResponse(json_data, content_type="text/html");

def handle_uploaded_file(f, dir):
    current_dir = os.path.join(os.path.dirname(__file__), "../static", "upload" ,dir );
    prefix = f.name.split(".")[-1:][0];
    file_name = time.strftime('%Y%m%d%H%M%S') + "." + prefix;
    with open(current_dir + os.path.sep + file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk);
    return file_name;


# Tag
def tagList(request, data):
    data['tags'] = models.Tag.objects.order_by("name").all();
    return render(request, "admin/blog/tag/list.html", data);

def viewTag(request, data):
    if request.method == "GET" and "id" in request.GET:
        id = request.GET['id'];
        try:
            tagObj = models.Tag.objects.get(id=id);
            data['tag'] = tagObj;
        except:
            pass;
        return render(request, "admin/blog/tag/add.html", data);

def addTag(request, data):
    if request.method == "POST" and "tag" in request.POST:
        name = request.POST['tag'].strip();
        if name != "":
            if "id" in request.POST:
                tagObj = models.Tag.objects.get(id=request.POST['id']);
                tagObj.name = name;
                status = request.POST['status'];
                tagObj.status = int(status);
                tagObj.save();
            else:
                try:
                    models.Tag.objects.get(name=name);
                except:
                    models.Tag(name=name).save();
        return HttpResponseRedirect( reverse("tag.list") );

def deleteTag(request, data):
    if "id" in request.GET:
        id = request.GET['id'];
        try:
            # first delete article
            for at in models.ArticleTag.objects.filter(tag_id= id).all():
                at.delete();
                #models.Article.objects.get(id=at.article.id).delete();
            models.Tag.objects.get(id = id).delete();
            return HttpResponse("1", content_type="text/plain");
        except:
            return HttpResponse("0", content_type="text/plain");

# category
def categoryList(request, data):
    data['categorys'] = models.Category.objects.order_by("orderdisplay","-id").all();
    return render(request, "admin/blog/category/list.html", data);

def addCategory(request, data):
    if request.method == "POST":
        category = models.Category();
        for k,v in request.POST.iteritems():
            if hasattr(category, k) and v != "":
                if k in ["status", "newpage", "isurl"]:
                    setattr(category, k, int(v));
                else:
                    setattr(category, k, v);
        category.save();
        return HttpResponseRedirect( reverse("category.list") );
    else:
        if request.GET.has_key("id"):
            data['category'] = models.Category.objects.get(id= request.GET['id']);
        return render(request, "admin/blog/category/add.html", data);

def deleteCategory(request, data):
    if "id" in request.GET:
        id = request.GET['id'];
        try:
            # first delete article
            for art in models.Article.objects.filter(category_id= id).all():
                art.delete();
            models.Category.objects.get(id = id).delete();
            return HttpResponse("1", content_type="text/plain");
        except:
            return HttpResponse("0", content_type="text/plain");

# Article
def articleList(request, data):
    if request.method == "GET":
        page = 1;
        data['status'] = "-1";
        data['category_id'] = "0";
        data['articles'] = models.Article.objects.order_by("id").all()[0:_PAGE_SIZE];
        data['totalcounts'] = models.Article.objects.count();
    if request.method == "POST":
        page = request.POST['curr_page'];
        title = request.POST['title'];
        status = request.POST['status'];
        category_id = request.POST['category_id'];
        data['title'] = title;
        data['status'] = status;
        if category_id != "":
            data['category_id'] = int(category_id);
        else:
            category_id = "0";
        page = int(page);
        if status != "-1" and category_id != "0":
            data['articles'] = models.Article.objects.filter(status=status,category_id=category_id, title__contains=title).order_by("id").all()[(page-1)*_PAGE_SIZE: page*_PAGE_SIZE];
            data['totalcounts'] = models.Article.objects.filter(status=status,category_id=category_id, title__contains=title).count();
        elif category_id != "0" and status == "-1":
            data['articles'] = models.Article.objects.filter(category_id=category_id, title__contains=title).order_by("id").all()[(page-1)*_PAGE_SIZE: page*_PAGE_SIZE];
            data['totalcounts'] = models.Article.objects.filter(category_id=category_id, title__contains=title).count();
        elif category_id == "0" and status != "-1":
            data['articles'] = models.Article.objects.filter(status=status, title__contains=title).order_by("id").all()[(page-1)*_PAGE_SIZE: page*_PAGE_SIZE];
            data['totalcounts'] = models.Article.objects.filter(status=status, title__contains=title).count();
        else:
            data['articles'] = models.Article.objects.filter(title__contains=title).order_by("id").all()[(page-1)*_PAGE_SIZE: page*_PAGE_SIZE];
            data['totalcounts'] = models.Article.objects.filter(title__contains=title).count();
    data['page'] = page;
    data['categorys'] = models.Category.objects.order_by("orderdisplay","-id").all();
    return render(request, "admin/blog/article/list.html", data);

def addArticle(request, data):
    if request.method == "GET":
        if "id" in request.GET:
            id = request.GET['id'];
            checkedtags = [t.tag_id for t in models.ArticleTag.objects.filter(article_id=id).all()];
            data['checkedtags'] = checkedtags;
            data['article'] = models.Article.objects.get(id=id);
        data['categorys'] = models.Category.objects.order_by("orderdisplay","-id").all();
        data['now'] = datetime.now();
        data['tags'] = models.Tag.objects.filter(status=1).order_by("name").all();
        return render(request, "admin/blog/article/add.html", data);
    elif request.method == "POST":
        title = request.POST['title'].strip();
        author = request.POST['author'].strip();
        urlname = request.POST['urlname'].strip();
        content = request.POST['content'];
        markdown = request.POST['markdown'];
        addtime = request.POST['addtime'];
        tags = request.POST.getlist("tag");
        if "istop" in request.POST:
            istop = 1;
        else:
            istop = 0;
        if "status" in request.POST:
            status = 1;
        else:
            status = 0;
        categoryid = request.POST['categoryid'];
        article = models.Article();
        article.title = title;
        article.author = author;
        article.urlname = urlname;
        article.content = content;
        article.markdown = markdown;
        article.addtime = addtime;
        article.istop = istop;
        article.category_id = categoryid;
        article.status = status;
        if request.POST['id'] != "":
            article.id = request.POST['id'];
            article.edittime = datetime.now();
            models.ArticleTag.objects.filter(article_id=request.POST['id']).delete();
        article.save();
        for tag in tags:
            at = models.ArticleTag();
            at.article_id = article.id;
            at.tag_id = tag;
            at.save();
        return HttpResponseRedirect( reverse("article.list") );

def deleteArticle(request, data):
    if "id" in request.GET:
        id = request.GET['id'];
        try:
            # first delete article
            models.ArticleTag.objects.filter(article_id= id).delete();
            models.Article.objects.get(id= id).delete();
            return HttpResponse("1", content_type="text/plain");
        except:
            return HttpResponse("0", content_type="text/plain");
