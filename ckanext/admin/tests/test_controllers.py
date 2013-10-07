#pylint: disable=R0201, R0904

"""Unit tests for controllers"""

from pylons import config
import paste.fixture    # pylint: disable=F0401

from ckan.config.middleware import make_app
from ckan.lib.create_test_data import CreateTestData
from ckan.tests import WsgiAppCase, CommonFixtureMethods, url_for
from ckan.tests.html_check import HtmlCheckMethods


class TestAdminControllers(WsgiAppCase, HtmlCheckMethods, CommonFixtureMethods):
    """
    Tests for admin reporting tool's controllers and routing.
    """
    
    @classmethod
    def setup_class(cls):
        """Set up testing environment."""

        CreateTestData.create()

        wsgiapp = make_app(config['global_conf'], **config['app_conf'])
        cls.app = paste.fixture.TestApp(wsgiapp)

    @classmethod
    def teardown_class(cls):
        """Get away from testing environment."""

        CreateTestData.delete()

        
    def test_admin_reporting_rendered(self):
        '''
        An admin user should see reporting page.
        '''       
        offset = url_for(controller='ckanext.admin.controllers:ReportController', action='report')
        username = u'testsysadmin'.encode('utf8')
        extra_environ = {'REMOTE_USER':username}
        res = self.app.get(offset, extra_environ=extra_environ)
        assert res.status == 200, 'Wrong status code (should be 200), in admin/reporting'
