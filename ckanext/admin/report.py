# pylint: disable=E1101

'''
Specific reports for authorities via tailored SQL queries.
'''
import logging

import ckan.model as model

log = logging.getLogger(__name__)

DATE_FORMAT = '%Y-%m-%d'

class PackageReport(object):
    '''
    Queries to gain package data
    '''
    @classmethod
    def total_packages(cls):
        '''
        Return total of packages
        Assuming state="active", type="dataset"
        
        :return: count
        '''
        res = model.Session.query(model.Package.id).filter(model.Package.state \
                    == "active").filter(model.Package.type=="dataset").count()
        return res
        
    @classmethod
    def total_packages_by_extra(cls, key, value):
        '''
        Return total of packages, whose key and extra are given.
        Assuming state="active", type="dataset"
        
        :param key: key value from extras
        :value: value from extras
        :return: count
        '''
        res = model.Session.query(model.Package.id).\
                   filter(model.Package.state=="active").\
                   filter(model.Package.type=="dataset").\
                   filter(model.PackageExtra.key==key).\
                   filter(model.PackageExtra.value==value).\
                   filter(model.Package.id==model.PackageExtra.package_id).\
                   count()
        return res
    
class UserReport(object):
    '''
    Queries for user information
    '''
    @classmethod
    def total_users(cls):
        '''
        Return total of users
        
        :return: count
        '''
        res = model.Session.query(model.User.id).count()
        return res

