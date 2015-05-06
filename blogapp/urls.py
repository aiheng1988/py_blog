from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('blogapp.views',
           # Examples:
           # url(r'^$', 'blog.views.home', name='home'),
           # url(r'^blog/', include('blog.foo.urls')),

           # Uncomment the admin/doc line below to enable admin documentation:
           # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

           # Uncomment the next line to enable the admin:
           # url(r'^admin/', include(admin.site.urls)),

           # file upload
           url(r'^upload_json', 'uploadJson', name='upload.json'),

           # tag
           url(r'^tag/list', 'tagList', name='tag.list'),
           url(r'^tag/add', 'addTag', name='tag.add'),
           url(r'^tag/view', 'viewTag', name='tag.view'),
           url(r'^tag/delete', 'deleteTag', name='tag.delete'),

           # category
           url(r'^category/list', 'categoryList', name='category.list'),
           url(r'^category/add', 'addCategory', name='category.add'),
           url(r'^category/delete', 'deleteCategory', name='category.delete'),

           # article
           url(r'^article/list', 'articleList', name='article.list'),
           url(r'^article/add', 'addArticle', name='article.add'),
           url(r'^article/delete', 'deleteArticle', name='article.delete'),
)