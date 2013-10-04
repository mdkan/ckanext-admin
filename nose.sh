case "$1" in
	unit )
		echo "Running unit tests";
		nosetests --ckan --with-pylons=ckanext-admin/test-core.ini ckanext-admin/ckanext/admin/tests --logging-filter=admin;
		;;
	* )
		echo "Accepted parameters are 'selenium' and 'unit' to run only Selenium or unit tests.";
		echo "Running all tests";

		nosetests --ckan --with-pylons=ckanext-admin/test-core.ini ckanext-admin/ckanext/admin/tests --logging-filter=admin;
		
		# xvfb-run nosetests --ckan --with-pylons=ckanext-admin/test-core.ini ckanext-admin/ckanext/admin/ --logging-filter=admin;
		;;
esac
