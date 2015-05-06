from django.db import models

# Tag Model
class Tag(models.Model):
    name = models.CharField(max_length=32);
    counts = models.IntegerField(default=0);
    status = models.BooleanField(default=True);

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=32);
    url = models.CharField(max_length=256, null=True);
    pid = models.IntegerField(default=0);
    orderdisplay = models.IntegerField(default=0);
    newpage = models.BooleanField(default=False);
    isurl = models.BooleanField(default=False);
    status = models.BooleanField(default=True);

# Article Model
class Article(models.Model):
    title = models.CharField(max_length=256);
    author = models.CharField(max_length=32);
    addtime = models.DateTimeField();
    urlname = models.CharField(max_length=256, null=True);
    content = models.TextField();
    markdown = models.TextField(null=True);
    hits = models.IntegerField(default=0);
    comments = models.IntegerField(default=0);
    category = models.ForeignKey(Category);
    istop = models.BooleanField(default=False);
    edittime = models.DateTimeField(null=True);
    status = models.BooleanField(default=True);

# Article and Tag Model
class ArticleTag(models.Model):
    article = models.ForeignKey(Article);
    tag = models.ForeignKey(Tag);

# Comments Model
class Comment(models.Model):
    name = models.CharField(max_length=32);
    url = models.CharField(max_length=256, null=True);
    pic = models.CharField(max_length=256, null=True);
    markdown = models.TextField(null=True);
    content = models.TextField();
    article = models.ForeignKey(Article);
    commentid = models.IntegerField(default=0);
    addtime = models.DateTimeField();
    status = models.BooleanField(default=False);
