import cherrypy
import click
from intercom.roots import IntercomRoot

CLICK_FILE_TYPE = click.Path(exists=True, dir_okay=False)


def run_server(global_config_filename, app_config_filename):
    cherrypy.config.update(global_config_filename)
    cherrypy.quickstart(root=IntercomRoot(), config=app_config_filename)


@click.command()
@click.argument('global_config', type=CLICK_FILE_TYPE)
@click.argument('app_config', type=CLICK_FILE_TYPE)
def main(global_config, app_config):
    run_server(global_config, app_config)


if __name__ == '__main__':
    main()
