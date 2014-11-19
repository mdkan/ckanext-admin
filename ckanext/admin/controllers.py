'''
Controller(s) for reporting in admin page
'''

import logging
import sys

import datetime

from pylons import config

from ckan.lib.base import render, c
from ckan.controllers.admin import AdminController
import ckanext.admin.report as report


log = logging.getLogger(__name__)

def datetime2date(datetime_):
    return datetime.date(datetime_.year, datetime_.month, datetime_.day)

def lastmonth(year, month):
    if month == 1 or month == 01:
        return (year-1, 12)
    else:
        return (year, month-1)

class ReportController(AdminController):
    def report(self):
        '''
        Generates a simple report page to admin site.
        Note, that the stats extension provides some nice reporting
        '''
        # package info
        # Total packages
        try:
            pkg_stats = report.PackageReport()
            c.numpackages = pkg_stats.total_packages()
            # Total of packages, where extra key=availability and value=direct_download and license=cc0
            ccz = pkg_stats.total_packages_by_license('CC0-1.0')
            odc = pkg_stats.total_packages_by_license('ODC-PDDL-1.0')
            c.cc0 = ccz + odc
            # Total of packages, where extra key=availability and value=direct_download and license=cc-by
            ccbysa = pkg_stats.total_packages_by_license("CC-BY-SA-4.0")
            cc4by = pkg_stats.total_packages_by_license("CC-BY-4.0")
            odbl = pkg_stats.total_packages_by_license("ODbL-1.0")
            oddby = pkg_stats.total_packages_by_license("ODC-BY-1.0")
            c.ccby = ccbysa + cc4by + odbl + oddby
            # Total of packages, where extra key=availability and value is not direct_download and 
            # license is not notspecified
            c.notfree = pkg_stats.total_nonfree_packages()
        
            c.pkg_per_month = pkg_stats.new_packages()
            
            # user info
            usr_stats = report.UserReport()
            
            c.numusers = usr_stats.total_users()
        
            #date_ = datetime2date(datetime.date.today())
            #c.date__0 = (date_.year, date_.month)
            #c.usrmonth__0 = usr_stats.users_by_month(date_.year, date_.month)
            #c.date__1 = lastmonth(date_.year, date_.month)
            #c.usrmonth__1 = usr_stats.users_by_month(c.date__1[0], c.date__1[1])
            #c.date__2 = lastmonth(c.date__1[0], c.date__1[1])
            #c.usrmonth__2 = usr_stats.users_by_month(c.date__2[0], c.date__2[1])
            c.users_per_month = usr_stats.users_by_month()
        except TypeError:
            log.debug(sys.exc_info()[0])
        
        return render('admin/report.html')
    