import logging

from pylons import config
from paste.deploy.converters import asbool

import commands

from ckan.lib.base import render, c
from ckan.controllers.admin import AdminController
import ckan.model as model
from ckan.model import Package, PackageExtra, User


log = logging.getLogger('ckanext.admin')

class ReportController(AdminController):
    def report(self):
        '''
        Generates a simple report page to admin site
        '''
        # package info
        # Todo: make this a real quality page
        c.numpackages = c.openpackages = 0
        c.numpackages = model.Session.query(Package.id).count()
        key = 'access'
        value = 'free'
        c.openpackages = model.Session.query(Package.id).\
                   filter(PackageExtra.key==key).\
                   filter(PackageExtra.value==value).\
                   filter(Package.id==PackageExtra.package_id).\
                   count()
        # format to: d.dd %
        if c.numpackages > 0:
            c.popen = float(c.openpackages) / float(c.numpackages) * 100           
        else:
            c.popen = 0
        c.popen = "{0:.2f}".format(c.popen) + ' %'
        
        
        # Todo: remove?
        # user info
        c.numusers = 0
        c.numusers = model.Session.query(User.id).count()
        
        return render('admin/report.html')
    