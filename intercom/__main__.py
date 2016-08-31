import cherrypy
import click
from intercom.roots import IntercomRoot
from cherrypy.process.plugins import Daemonizer, PIDFile


def run_server(
        global_config_filename,
        app_config_filename,
        daemon_pid_filename=None):
    if daemon_pid_filename is not None:
        Daemonizer(cherrypy.engine).subscribe()
        PIDFile(cherrypy.engine, daemon_pid_filename).subscribe()

    cherrypy.config.update(global_config_filename)
    cherrypy.quickstart(root=IntercomRoot(), config=app_config_filename)


@click.command()
@click.argument('global-config', type=click.Path(exists=True, dir_okay=False))
@click.argument('app-config', type=click.Path(exists=True, dir_okay=False))
@click.option('--daemon-pid-file', type=click.Path(dir_okay=False))
def main(global_config, app_config, daemon_pid_file):
    run_server(global_config, app_config, daemon_pid_file)


if __name__ == '__main__':
    main()
