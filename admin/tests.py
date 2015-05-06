"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):
    def test_init_datas(self):
        import models;
        user = models.User(username="ahern88", password="f109af48c9fa8ffd277846b99694ab82", nick="艾恒", mail="66429174@qq.com", joindatetime="2014-05-10 06:34:40");
        user.save();
        role = models.Role(name="管理员");
        role.save();
        userrole = models.UserRole(user_id=user.id, role_id= role.id);
        userrole.save();
        system1 = models.SystemFunction(name="系统管理", orderdisplay=1, ismenu=1);
        system1.save();
        system2 = models.SystemFunction(name="用户列表", orderdisplay=0, ismenu=1, icon="icon-user", pid=system1.id, url="user.list", accessurl="user.list,user.add,user.delete");
        system2.save();
        system3 = models.SystemFunction(name="角色列表", orderdisplay=0, ismenu=1, icon="icon-list", pid=system1.id, url="role.list", accessurl="role.list,role.add,role.delete,role.bindUser");
        system3.save();
        system4 = models.SystemFunction(name="资源列表", orderdisplay=0, ismenu=1, icon="icon-list-alt", pid=system1.id, url="systemfunction.list", accessurl="systemfunction.list,systemfunction.add,systemfunction.delete,systemfunction.bindRole");
        system4.save();
        system5 = models.SystemFunction(name="公共资源", orderdisplay=0, ismenu=0, icon="icon-list", pid=system1.id, url="admin.index", accessurl="user.add,admin.index");
        system5.save();
        models.SystemFunctionRole(role_id=role.id, system1.id).save();
        models.SystemFunctionRole(role_id=role.id, system2.id).save();
        models.SystemFunctionRole(role_id=role.id, system3.id).save();
        models.SystemFunctionRole(role_id=role.id, system4.id).save();
        models.SystemFunctionRole(role_id=role.id, system5.id).save();

