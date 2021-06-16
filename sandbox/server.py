'''
Socket.IO server for testing
CLI:
  python -m watchgod server.main 1
'''

import socketio
from sanic import Sanic
from aiohttp import web
import tornado.ioloop
import tornado.web

# TODO:
# * asgi/Uvicorn
# * asgi/Daphne

ASYNC_MODE = 'tornado'
PORT = 63047

sio = socketio.AsyncServer(async_mode=ASYNC_MODE)
count = 0

if ASYNC_MODE == 'aiohttp':
    app = web.Application()
if ASYNC_MODE == 'sanic':
    app = Sanic(name='Just a simple service')
if ASYNC_MODE == 'tornado':
    app = tornado.web.Application([
        (r"/socket.io/", socketio.get_tornado_handler(sio))
    ])

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

def main():
    print('=========================')
    print('  async_mode = %s' % ASYNC_MODE)
    print('=========================')
    if ASYNC_MODE == 'aiohttp':
        sio.attach(app)
        web.run_app(app, port=PORT)
    if ASYNC_MODE == 'tornado':
        app.listen(PORT)
        tornado.ioloop.IOLoop.current().start()
    if ASYNC_MODE == 'sanic':
        sio.attach(app)
        app.run(port=PORT)

if __name__ == '__main__':
    main()