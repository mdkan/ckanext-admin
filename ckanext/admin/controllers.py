import logging

from pylons import config

import commands

from ckan.lib.base import render, c
from ckan.controllers.admin import AdminController

log = logging.getLogger('ckanext.admin')

class SystemController(AdminController):
    def system(self):
        smem = commands.getoutput("free -m")
        c.mem = smem.split( );
        # Add empty list items for empty cells
        c.mem.extend(['','',''])
        c.mem.insert(0, '')
        c.mem = c.mem[0:18] + ['','',''] + c.mem[-7:]
        
        shd = commands.getoutput("df -h")
        c.hd = shd.split( );
        # Split matches the single phrase "Mounted on", quick fix:
        c.hd[5] = c.hd[5] + ' ' + c.hd[6]
        del c.hd[6]
              
        sut = commands.getoutput("uptime")
        c.ut = sut.split(',');
        del c.ut[1:2]
        c.ut[2] = c.ut[2] + ', ' + c.ut[3] + ', '+ c.ut[4]
        del c.ut[3:]
        
        return render('admin/system.html')
    def report(self):
        return render('admin/report.html')
    