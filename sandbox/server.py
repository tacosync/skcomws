'''
Socket.IO server for testing

CLI:
  python -m watchgod server.main [aiohttp|sanic|tornado|asgi]

Test results:
           | connect | disconnect | event | background_task | Ctrl+C
  ---------+---------+------------+-------+-----------------|--------
   aiohttp |    O    |     O      |   O   |        X        |   O
   sanic   |    O    |     O      |   O   |        X        |   O
   tornado |    O    |     O      |   O   |        O        |   O
   asgi    |    O    |     O      |   O   |        !        |   O
'''

import sys

from servers.aiohttp_server import main as aiohttp_main
from servers.asgi_server import main as asgi_main
from servers.sanic_server import main as sanic_main
from servers.tornado_server import main as tornado_main

def main():
    if len(sys.argv) > 1:
        framework = sys.argv[1]
    else:
        framework = 'tornado'

    boot_options = {
        'aiohttp': aiohttp_main,
        'asgi': asgi_main,
        'sanic': sanic_main,
        'tornado': tornado_main
    }

    if framework in boot_options:
        bootstrap = boot_options[framework]
        bootstrap()
    else:
        print('Unknown framework "%s".' % framework)

if __name__ == '__main__':
    main()

