import logging

from pylons import config

from ckan.lib.base import render, c
from ckan.controllers.admin import AdminController
import ckan.model as model
import ckanext.admin.report as report


log = logging.getLogger(__name__)

class ReportController(AdminController):
    def report(self):
        '''
        Generates a simple report page to admin site.
        Note, that the stats extension provides some nice reporting
        '''
        # package info
        # Total packages
        pkg_stats = report.PackageReport()
        c.numpackages = pkg_stats.total_packages()
        # Total of packages, where extra key=access and value=free
        key = 'access'
        value = 'free'
        c.openpackages = pkg_stats.total_packages_by_extra(key, value)
        # format to: d.dd %
        try:
            c.popen = "{0:.2f}".format(float(c.openpackages) / float(c.numpackages) * 100) + ' %'          
        except ZeroDivisionError:
            c.popen = "No packages"
        
        # user info
        usr_stats = report.UserReport()
        c.numusers = usr_stats.total_users()
        
        return render('admin/report.html')
    