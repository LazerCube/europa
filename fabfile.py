from posixpath import join

from fabric.operations import local as lrun, run
from fabric.api import cd, env, prefix, sudo
from fabric.contrib.files import append

import os

env.user = 'ubuntu'

def localhost():
    env.run = lrun
    env.hosts = ['localhost']

def remote():
    env.run = run
    env.hosts = ['some.remote.host']

PROJECT_NAME = 'myproject'
HOME_DIR = '/home/ubuntu'
BASE_DIR = join(HOME_DIR, 'myproject')
SUPERVISOR_CONFIG = '/etc/supervisor'
NGINX_CONFIG = '/etc/nginx'

DATABASE_USER = 'myprojectuser'
DATABASE_PASSWORD = 'randomtemppassword'

ORIGIN_DIR = os.path.dirname(os.path.realpath(__file__))

def upgrade_system():
    sudo('apt-get update -y')
    sudo('apt-get upgrade -y')

def install_software():
    sudo('apt-get install -y git nginx python-dev python-pip libpq-dev postgresql postgresql-contrib')
    sudo('pip install -U virtualenvwrapper')
    append(join(HOME_DIR, '.bash_profile'), ('export WORKON_HOME={0}/.virtualenvs'.format(HOME_DIR), 'source /usr/local/bin/virtualenvwrapper.sh'))

def remove_software():
    run('rm -rf {0}'.format(join(HOME_DIR, '.bash_profile')))
    sudo('pip uninstall virtualenvwrapper')
    sudo('apt-get purge -y nginx python-dev python-pip libpq-dev postgresql postgresql-contrib')
    sudo('apt-get autoremove')

def create_database():
    sudo('psql -c "CREATE DATABASE %s;"' % (PROJECT_NAME), user='postgres')
    sudo('psql -c "CREATE USER %s WITH PASSWORD \'%s\';"' % (DATABASE_USER, DATABASE_PASSWORD), user='postgres')
    sudo('psql -c "GRANT ALL PRIVILEGES ON DATABASE %s TO %s;"' % (PROJECT_NAME, DATABASE_USER), user='postgres')

def install_myproject(origin=ORIGIN_DIR):
    run('git clone -b master {0} {1}'.format(origin, BASE_DIR))
    run('mkdir {0}'.format(join(BASE_DIR, 'logs')))

def upgrade_myproject():
    with cd(BASE_DIR):
        run('git pull origin master')

def remove_myproject():
    run('rm -rf {0}'.format(BASE_DIR))

def create_virtualenv():
    run('mkvirtualenv myproject')

def remove_virtualenv():
    run('rmvirtualenv myproject')

def deploy_requirements():
    with prefix('workon myproject'):
        run('pip install -r {0}'.format(join(BASE_DIR,'requirements/production.txt'))) #should pick based on env

def deploy_gunicorn(settings=None, secret_key=None):
    sudo('chmod u+x {0}'.format(join(BASE_DIR, 'bin/gunicorn_start')))
    if settings:
        append(join(HOME_DIR, '.bash_profile'), 'export DJANGO_SETTINGS_MODULE=\'myproject.config.settings.{0}\''.format(settings))
    if secret_key:
        append(join(HOME_DIR, '.bash_profile'), 'export SECRET_KEY=\'{0}\''.format(secret_key))
    with prefix('workon myproject'):
        run('python {0} {1}'.format(join(BASE_DIR, 'myproject/manage.py'), 'migrate'))
        run('python {0} {1}'.format(join(BASE_DIR, 'myproject/manage.py'), 'collectstatic'))

def deploy_supervisor():
    sudo('rm -rf {0}'.format(join(SUPERVISOR_CONFIG, 'conf.d/myproject.conf')))
    sudo('cp -f {0} {1}'.format(join(BASE_DIR, 'config/supervisord.conf'), join(SUPERVISOR_CONFIG, 'conf.d/myproject.conf')))
    sudo('supervisorctl update')

def deploy_nginx():
    sudo('rm -rf {0}'.format(join(NGINX_CONFIG, 'conf.d/myproject.conf')))
    sudo('rm -rf {0}'.format(join(NGINX_CONFIG, 'sites-enabled/default')))
    sudo('cp -f {0} {1}'.format(join(BASE_DIR, 'config/nginx.conf'), join(NGINX_CONFIG, 'conf.d/myproject.conf')))
    sudo('nginx -s reload')

def start():
    sudo("supervisorctl start myproject")
    sudo("service nginx start")

def stop():
    sudo("supervisorctl stop myproject")
    sudo("service nginx stop")

def restart():
    sudo("supervisorctl restart myproject")
    sudo("service nginx restart")

def manage(command=''):
    with prefix('workon myproject'):
        run('python {0} {1}'.format(join(BASE_DIR, 'myproject/manage.py'), command))

def full_install(origin=ORIGIN_DIR, settings=None, secret_key=None):
    upgrade_system()
    install_software()
    create_database()
    install_myproject(origin)
    create_virtualenv()
    deploy_requirements()
    deploy_gunicorn(settings, secret_key)
    #deploy_supervisor()
    deploy_nginx()
    start()

def quick_upgrade(settings=None, secret_key=None):
    upgrade_myproject()
    deploy_requirements()
    deploy_gunicorn(settings, secret_key)
    restart()

def full_upgrade(settings=None, secret_key=None):
    upgrade_system()
    install_software()
    upgrade_myproject()
    deploy_requirements()
    deploy_gunicorn(settings, secret_key)
    #deploy_supervisor()
    deploy_nginx()
    restart()

def full_remove():
    stop()
    remove_virtualenv()
    remove_myproject()
    remove_software()
