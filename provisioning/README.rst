extensions.libreoffice.org operations documentation
===================================================

Architecture
------------

This is the operations documentation for the deployment of the extensions and
templates site `extensions.libreoffice.org`. It's a Plone site deployed using a
ZEO server (DB backend) and two Zope clients. We are using an Nginx frontend
server and a Varnish HTTP accelerator. To balance the load between the two Zope
clients we use a HAProxy balancer.

All of them are controlled via a supervisord instance.

The deployment is centralized in one directory:

  /srv/extensions.libreoffice.org

Buildout
--------

The buildout used for the deployment is:

  $ cd /srv/extensions.libreoffice.org
  $ ./bin/buildout -c live.cfg

That will trigger the installation of all the software stack.

Nginx
-----

We are using the packaged version of the Nginx server, not the one available in
the buildout. So all the configuration related to the frontend Nginx server is
done outside the build.

Start/Stop
----------

The server stack can be started by starting supervisord:

  $ cd /srv/extensions.libreoffice.org
  $ ./bin/supervisord

And controlled using the supervisord cli:

  $ ./bin/supervisorctl

haproxy                          RUNNING   pid 1094, uptime 7 days, 11:54:06
instance1                        RUNNING   pid 1102, uptime 7 days, 11:54:06
instance2                        RUNNING   pid 1103, uptime 7 days, 11:54:06
varnish                          RUNNING   pid 1100, uptime 7 days, 11:54:06
zeo                              RUNNING   pid 1101, uptime 7 days, 11:54:06
supervisor>

or use the command line:

  $ ./bin/supervisorctl restart instance1

For automatic start when the server starts, we are using this script:

  /etc/init.d/supervisor

set for starting for the required rc.d entrypoints.

Access to the ZMI
-----------------

It is recommended to access the ZMI via an ssh tunnel. You can do so, by
configuring locally your ssh config to use your private key to access the
remote server and issuing the command:

  $ ssh -L 8085:localhost:8085 -N <server_name> -v

Once issued the command you can open a browser for accessing the instance to
the port 8085 (or the port of the any of the externally facing Zope instances,
8081 or 8082, see below).

  http://localhost:8085/manage

It's advisable not to bother the externally facing instances (if possible) and
start a debug instance for maintenance operations:

  $ ./bin/instance-debug fg

This instance run in the 8085 port.

The name of the Plone instance is `Plone`.

Backup
------

A daily backup is performed in the `backups` directory. A cron job is
configured to do it.

Ansible playbook
----------------

For simple maintenance and update tasks you can use the supplied Ansible
playbook. You need to have installed Ansible > 2.0 in your system or an
equivalent virtualenv (you can use requirements.txt to install it):

  $ ansible-playbook -i hosts playbook.yml -K

NOTE: You should parametrize the `playbook.yml` and the `host` files and
replace the `<remote_user>` and `<server_name>` placeholders with the remote user
and the server name.
