#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives using do_clean
"""

from fabric.api import local, run, lcd, env

env.hosts = ['52.86.196.120', '100.24.235.246']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_clean(number=0):
    """Deletes out-of-date archives"""
    number = int(number)
    if number < 0:
        return

    try:
        number_to_keep = number + 1

        with lcd("versions"):
            local("ls -1t | tail -n +{} | xargs -I {{}} rm {{}}"
                  .format(number_to_keep))

        with cd("/data/web_static/releases"):
            run("ls -1t | tail -n +{} | xargs -I {{}} rm -rf {{}}"
                .format(number_to_keep))
    except Exception as e:
        print("Error:", e)


        if number_to_keep <= 1:
            return
