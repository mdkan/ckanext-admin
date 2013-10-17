'''
Plugin to provide reporting in admin page
'''

import logging
import os

from pylons import config

from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IRoutes, IMapper, IConfigurer

log = logging.getLogger(__name__)

class Reporting(SingletonPlugin):
    '''
    Plugin for displaying report
    '''
    
    def update_config(self, config):
        '''
        IConfigurer inplementation to tell CKAN to search for templates in
        this extension's templates folder
        '''
        here = os.path.dirname(__file__)
        rootdir = os.path.dirname(os.path.dirname(here))
        template_dir = os.path.join(rootdir, 'ckanext', 'admin', 'theme', 'templates')
        config['extra_template_paths'] = ','.join([
            template_dir, config.get('extra_template_paths', '')])
    implements(IRoutes, inherit=True)
    implements(IConfigurer, inherit=True)
    
    def before_map(self, map):
        
        map.connect('ckanadmin_report',
                    '/ckan-admin/report',
                    controller='ckanext.admin.controllers:ReportController',
                    action='report')
        return map
        