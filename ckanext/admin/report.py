# pylint: disable=E1101

'''
Specific reports for authorities via tailored SQL queries.
'''
import logging

import sqlalchemy as sa

import ckan.model as model

log = logging.getLogger(__name__)

DATE_FORMAT = '%Y-%m-%d'

def table(name):
    return sa.Table(name, model.meta.metadata, autoload=True)

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
    
    @classmethod
    def total_packages_by_column(cls, column, value):
        '''
        Return total of packages, whose specific column and value
        are given. Assuming state="active", type="dataset"
        
        :param
        :return: count
        '''
        res = model.Session.query(model.Package.id).\
                   filter(model.Package.state=="active").\
                   filter(model.Package.type=="dataset").\
                   filter(model.Package.column==value).\
                   count()
        return res
    
    @classmethod
    def total_packages_by_license(cls, license):
        '''
        Return count of directly downloadable packages with
        license as cc0
        
        :param license: license id
        :return: count
        '''
        res = model.Session.query(model.Package.id).\
                   filter(model.Package.state=="active").\
                   filter(model.Package.type=="dataset").\
                   filter(model.Package.license_id==license).\
                   filter(model.PackageExtra.key=="availability").\
                   filter(model.PackageExtra.value=="direct_download").\
                   filter(model.Package.id==model.PackageExtra.package_id).\
                   count()
        return res
    
    @classmethod
    def packages_by_license(cls, license):
        '''
        Return count of directly downloadable packages with
        license as zz0
        
        :param license: license id
        :return: list of ids as tuple
        '''
        res = model.Session.query(model.Package.id).\
                   filter(model.Package.state=="active").\
                   filter(model.Package.type=="dataset").\
                   filter(model.Package.license_id==license).\
                   filter(model.PackageExtra.key=="availability").\
                   filter(model.PackageExtra.value=="direct_download").\
                   filter(model.Package.id==model.PackageExtra.package_id).\
                   all()
        return res
    
    @classmethod
    def total_nonfree_packages(cls):
        '''
        Return count of packages which are not freely downloadable
        License must not be not specified
        
        :return: count
        '''
        res = model.Session.query(model.Package.id).\
                   filter(model.Package.state=="active").\
                   filter(model.Package.type=="dataset").\
                   filter(model.Package.license_id!="notspecified").\
                   filter(model.PackageExtra.key=="availability").\
                   filter(model.PackageExtra.value!="direct_download").\
                   filter(model.Package.id==model.PackageExtra.package_id).\
                   count()
        return res
    
    @classmethod
    def nonfree_packages(cls):
        '''
        Return count of packages which are not freely downloadable
        License must not be not specified
        
        :return: list of ids as tuple
        '''
        res = model.Session.query(model.Package.id).\
                   filter(model.Package.state=="active").\
                   filter(model.Package.type=="dataset").\
                   filter(model.Package.license_id!="notspecified").\
                   filter(model.PackageExtra.key=="availability").\
                   filter(model.PackageExtra.value!="direct_download").\
                   filter(model.Package.id==model.PackageExtra.package_id).\
                   all()
        return res
    
    @classmethod
    def new_packages(cls):
        package_revision = table('package_revision')
        revision = table('revision')
        
        sel = """
        select prid, min, extract(year from min) as y, extract(month from min) as m 
from (select package_revision.id as prid, min(revision.timestamp) as min 
from package_revision 
join revision on revision.id = package_revision.revision_id 
group by package_revision.id 
order by min(revision.timestamp)) as tbl;
        """
                
        res = model.Session.execute(sel).fetchall()
        
        nonfree = cls.nonfree_packages()
        freecond = cls.packages_by_license('cc-by') + cls.packages_by_license('cc-by-4.0')
        free = cls.packages_by_license('cc-zero')
        
        ret = {}
        retfr = {}
        retfrc = {}
        retnfr = {}
        
        # TODO: find a better solution in sql, this looping is not good
        # I really doubt this scales well with a mass of datasets, but for now
        # we don't have that many
        for prid, min, y, m in res:
            key = unicode(int(y)) + "/" + unicode(int(m))
            
            if not key in ret:
                ret[key] = int()
            if not key in retfr:
                retfr[key] = int()
            if not key in retfrc:
                retfrc[key] = int()
            if not key in retnfr:
                retnfr[key] = int()
                
            ret[key] += 1
            
            tprid = (prid,)
            if tprid in free:
                retfr[key] += 1
            if tprid in freecond:
                retfrc[key] += 1
            if tprid in nonfree:
                retnfr[key] += 1
        
        return {'total': ret, 'free': retfr, 'freecond': retfrc, 'nonfree': retnfr}
        
    
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
    
    @classmethod
    def users_by_month(cls):
        '''
        New users by month
        
        :return: count
        '''
        user = table('user')
        q = sa.select([sa.func.count('id'), sa.extract('year', user.c.created), \
                        sa.extract('month', user.c.created)],\
                        from_obj=[user]).\
                        group_by('anon_1', 'anon_2').\
                        order_by('anon_1', 'anon_2')
        res = model.Session.execute(q).fetchall()
        ret = {}
        for count, anon_1, anon_2 in res:
            key = unicode(int(anon_1)) + "/" + unicode(int(anon_2))
            ret[key] = count

        return ret
        

