if [ -d $WORKSPACE/../virtualenv ]; then
	rm -rf $WORKSPACE/../virtualenv
fi
if [ -d $WORKSPACE/../static ]; then
	rm -rf $WORKSPACE/../static
fi
if [ -d $WORKSPACE/../database ]; then
	rm -rf $WORKSPACE/../database
fi
mkdir ../virtualenv
mkdir ../database
mkdir ../static
virtualenv -p /usr/local/bin/python2.7 $WORKSPACE/../virtualenv
$WORKSPACE/../virtualenv/bin/pip install -r ./dependencies.txt
#source $WORKSPACE/../virtualenv/bin/activate
$WORKSPACE/../virtualenv/bin/python $WORKSPACE/group1/manage.py makemigrations
$WORKSPACE/../virtualenv/bin/python $WORKSPACE/group1/manage.py migrate
nohup $WORKSPACE/../virtualenv/bin/python group1/manage.py runserver 0.0.0.0:8090 &
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'aalva@bu.edu', 'pass')" | $WORKSPACE/../virtualenv/bin/python $WORKSPACE/group1/manage.py shell
#$WORKSPACE/../virtualenv/bin/python group1/manage.py test
$WORKSPACE/../virtualenv/bin/python group1/manage.py jenkins --enable-coverage requirements.tests.unit
$WORKSPACE/../virtualenv/bin/pylint --rcfile=.pylintrc group1/requirements > group1/pylint.log || exit 0
#$WORKSPACE/../virtualenv/bin/python group1/manage.py test requirements.tests.ui
fuser -k 8090/tcp
