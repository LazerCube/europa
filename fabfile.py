from posixpath import join

from fabric.operations import local as lrun, run
from fabric.api import cd, env, prefix, sudo, reboot, settings
from fabric.contrib.files import append

import os
import random
import string

def localhost():
    env.user = 'django'
    env.run = lrun
    env.hosts = ['localhost']

def remote():
    env.user = 'django'
    env.run = run
    env.hosts = ['10.0.2.2:2500']

PROJECT_NAME = 'myproject'
HOME_DIR = '/home/{0}'.format(env.user)
BASE_DIR = join(HOME_DIR, 'myproject')

NGINX_CONFIG = '/etc/nginx'
SYSTEMD_CONFIG = '/etc/systemd/system'

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
    sudo('psql -c "ALTER ROLE %s SET client_encoding TO \'utf8\';"' % (DATABASE_USER), user='postgres')
    sudo('psql -c "ALTER ROLE %s SET default_transaction_isolation TO \'read committed\';"' % (DATABASE_USER), user='postgres')
    sudo('psql -c "ALTER ROLE %s SET timezone TO \'UTC\';"' % (DATABASE_USER), user='postgres')
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

def deploy_gunicorn(settings=None):
    sudo('rm -rf {0}'.format(join(SYSTEMD_CONFIG, 'gunicorn.service')))
    sudo('rm -rf {0}'.format(join(SYSTEMD_CONFIG, 'gunicorn.socket')))
    sudo('cp -f {0} {1}'.format(join(BASE_DIR, 'bin/gunicorn.service'), join(SYSTEMD_CONFIG, 'gunicorn.service')))
    sudo('cp -f {0} {1}'.format(join(BASE_DIR, 'bin/gunicorn.socket'), join(SYSTEMD_CONFIG, 'gunicorn.socket')))
    if settings:
        append(join(HOME_DIR, '.bash_profile'), 'export DJANGO_SETTINGS_MODULE=\'config.settings.{0}\''.format(settings))
    with prefix('workon myproject'):
        run('python {0} {1}'.format(join(BASE_DIR, 'myproject/manage.py'), 'migrate'))
        run('python {0} {1}'.format(join(BASE_DIR, 'myproject/manage.py'), 'collectstatic'))
        sudo('systemctl start gunicorn')
        sudo('systemctl enable gunicorn')

def deploy_nginx():
    sudo('rm -rf {0}'.format(join(NGINX_CONFIG, 'sites-available/myproject')))
    sudo('rm -rf {0}'.format(join(NGINX_CONFIG, 'sites-enabled/default')))
    sudo('cp -f {0} {1}'.format(join(BASE_DIR, 'config/nginx.conf'), join(NGINX_CONFIG, 'sites-available/myproject')))
    with settings(warn_only=True):
        sudo('ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled')
    sudo('nginx -t')
    sudo('systemctl restart nginx')

def generate_key(secret_key=None):
    if secret_key:
        return secret_key
    secret_key = ("".join([random.SystemRandom().choice(string.digits + string.letters + string.punctuation) for i in range(100)]))
    return secret_key

def create_key(secret_key=None):
    remove_key()
    append("/etc/secret_key.txt", "{0}".format(generate_key(secret_key)), use_sudo=True)

def remove_key():
    sudo('rm -rf /etc/secret_key')

def reboot():
    print('::Rebooting to apply new changes...')
    reboot(300)
    print('::Continuing with install...')

def start():
    sudo("systemctl start gunicorn")
    sudo("systemctl start nginx")

def stop():
    sudo("systemctl stop gunicorn")
    sudo("systemctl stop nginx")

def restart():
    sudo("systemctl restart gunicorn")
    sudo("systemctl restart nginx")

def manage(command=''):
    with prefix('workon myproject'):
        run('python {0} {1}'.format(join(BASE_DIR, 'myproject/manage.py'), command))

def full_install(origin=ORIGIN_DIR, settings=None, secret_key=None):
    upgrade_system()
    install_software()
    create_database()
    install_myproject(origin)
    create_key(secret_key)
    create_virtualenv()
    deploy_requirements()
    deploy_gunicorn(settings)
    deploy_nginx()
    start()

def quick_upgrade(settings=None, secret_key=None):
    upgrade_myproject()
    create_key(secret_key)
    deploy_requirements()
    deploy_gunicorn(settings)
    restart()

def full_upgrade(settings=None, secret_key=None):
    upgrade_system()
    install_software()
    upgrade_myproject()
    create_key(secret_key)
    deploy_requirements()
    deploy_gunicorn(settings)
    deploy_nginx()
    restart()

def full_remove():
    stop()
    remove_virtualenv()
    remove_key()
    remove_myproject()
    remove_software()
