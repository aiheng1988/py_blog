from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('admin.views',
    # Examples:
    # url(r'^$', 'blog.views.home', name='home'),
    # url(r'^blog/', include('blog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'login'),
    url(r'^login/', 'login', name="login"),
    url(r'^auth/', 'auth', name='auth'),
    url(r'^logout/', 'logout', name='logout'),

    # user
    url(r'^user/list', 'userList', name='user.list'),
    url(r'^user/check', 'checkUser', name='user.check'),
    url(r'^user/add', 'addUser', name='user.add'),
    url(r'^user/delete', 'delUser', name='user.delete'),

    # system function
    url(r'^systemfunction/list', 'systemfunctionList', name='systemfunction.list'),
    url(r'^systemfunction/add', 'addSystemfunction', name='systemfunction.add'),
    url(r'^systemfunction/delete', 'delSystemfunction', name='systemfunction.delete'),
    url(r'^systemfunction/bind', 'bindSystemfunction', name='systemfunction.bindRole'),

    # role url
    url(r'^role/list', 'roleList', name='role.list'),
    url(r'^role/add', 'addRole', name='role.add'),
    url(r'^role/delete', 'delRole', name='role.delete'),
    url(r'^role/bind', 'bindRole', name='role.bindUser'),

    url(r'^index/', 'index', name='admin.index'),

)