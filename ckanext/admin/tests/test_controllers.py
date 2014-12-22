#pylint: disable=R0201, R0904

"""Unit tests for controllers"""

from ckan.tests import WsgiAppCase, CommonFixtureMethods, url_for
from ckan.tests.html_check import HtmlCheckMethods
import ckan.model as model
from ckanext.harvest import model as harvest_model
import ckanext.kata.model as kata_model


class TestAdminControllers(WsgiAppCase, HtmlCheckMethods, CommonFixtureMethods):
    """
    Tests for admin reporting tool's controllers and routing.
    """

    @classmethod
    def setup_class(cls):
        kata_model.setup()
        harvest_model.setup()

        model.User(name="testsysadmin", sysadmin=True).save()

    @classmethod
    def teardown_class(cls):
        model.repo.rebuild_db()

        
    def test_admin_reporting_rendered(self):
        '''
        An admin user should see reporting page.
        '''       
        offset = url_for(controller='ckanext.admin.controllers:ReportController', action='report')
        username = u'testsysadmin'.encode('utf8')
        extra_environ = {'REMOTE_USER':username}
        res = self.app.get(offset, extra_environ=extra_environ)
        assert res.status == 200, 'Wrong status code (should be 200), in admin/reporting'
