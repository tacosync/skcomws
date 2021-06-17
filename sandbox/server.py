'''
Socket.IO server for testing

CLI:
  python -m watchgod server.main [aiohttp|sanic|tornado|asgi]

Test results:
           | connect | disconnect | event | background_task | Ctrl+C
  ---------+---------+------------+-------+-----------------|--------
   aiohttp |    O    |     O      |   O   |        O        |   O
   sanic   |    O    |     X      |   O   |        X        |   O
   torando |    O    |     O      |   O   |        O        |   X
   asgi    |    X    |     ?      |   ?   |        X        |   O
'''

import asyncio
import sys

import socketio
import tornado.ioloop
import tornado.web
import uvicorn

from aiohttp import web
from sanic import Sanic

PORT = 63047
count = 0

if len(sys.argv) >= 2 and sys.argv[1] in ['aiohttp', 'sanic', 'tornado', 'asgi']:
    ASYNC_MODE = sys.argv[1]
else:
    ASYNC_MODE = 'aiohttp'

if ASYNC_MODE == 'sanic':
    sio = socketio.AsyncServer(async_mode=ASYNC_MODE, cors_allowed_origins=[])
else:
    sio = socketio.AsyncServer(async_mode=ASYNC_MODE)

if ASYNC_MODE == 'aiohttp':
    app = web.Application()
if ASYNC_MODE == 'sanic':
    app = Sanic(name='Just a simple service')
    app.config['CORS_SUPPORTS_CREDENTIALS'] = True
if ASYNC_MODE == 'tornado':
    app = tornado.web.Application([
        (r"/socket.io/", socketio.get_tornado_handler(sio))
    ])
if ASYNC_MODE == 'asgi':
    app = socketio.ASGIApp(sio)

tick_queue = asyncio.Queue()

@sio.event
async def connect(sid, environ, auth):
    print('[%s]: connected' % sid)

@sio.event
async def disconnect(sid):
    print('[%s]: disconnected' % sid)

@sio.event
async def client_said(sid, data):
    global count
    message = 'This is server response #%d.' % count
    count += 1
    print('[%s]: %s' % (sid, data['message']))
    await sio.emit('server_said', { 'message': message })

async def tick_dequeue():
    while True:
        await asyncio.sleep(3)
        tick = await tick_queue.get()
        await sio.emit('tick', tick)
        print('tick_dequeue() qsize=%d' % tick_queue.qsize())

async def tick_enqueue():
    while True:
        await asyncio.sleep(1)
        await tick_queue.put({
            'security_code': '2330.TW',
            'close': 601.15
        })
        print('tick_enqueue()')

def get_asgi_app():
    global app
    return app

def main():
    print('==============================')
    print('  async_mode = %s' % ASYNC_MODE)
    print('==============================')

    sio.start_background_task(tick_dequeue)
    sio.start_background_task(tick_enqueue)

    if ASYNC_MODE == 'aiohttp':
        sio.attach(app)
        web.run_app(app, port=PORT)
    if ASYNC_MODE == 'tornado':
        app.listen(PORT)
        tornado.ioloop.IOLoop.current().start()
    if ASYNC_MODE == 'sanic':
        sio.attach(app)
        app.run(port=PORT)
    if ASYNC_MODE == 'asgi':
        uvicorn.run('server:app', host="127.0.0.1", port=PORT, log_level="info")

if __name__ == '__main__':
    main()
