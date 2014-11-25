from setuptools import setup, find_packages

version = '0.1'

setup(
	name='ckanext-admin',
	version=version,
	description="Reporting tools for admins",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='Pinja Koskinen',
	author_email='pinja.koskinen@csc.fi',
	url='http://github.com/kata-csc/ckanext-admin',
	license='AGPL',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.admin'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
	entry_points=\
	"""
    [ckan.plugins]
	# Add plugins here, eg
	# myplugin=ckanext.admin:PluginClass
	admin_reporting=ckanext.admin.plugin:Reporting
	""",
)
