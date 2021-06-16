'''
Socket.IO server for testing
CLI:
  python -m watchgod server.main
'''

import socketio
from sanic import Sanic

count = 0

app = Sanic(name='Just a simple service')
sio = socketio.AsyncServer(async_mode='sanic')
sio.attach(app)

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
    app.run(port=63047)

if __name__ == '__main__':
    main()
