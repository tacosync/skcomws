'''
Socket.IO client for testing
'''

import asyncio
import socketio

COUNT_LIMIT = 3

count = 0
sio = socketio.AsyncClient()

@sio.event
async def connect():
    print('[server]: connected')
    await sio.emit('client_said', { 'message': 'Hello' })

@sio.event
async def server_said(data):
    global count
    print('[server]: %s' % data['message'])
    if count < COUNT_LIMIT:
        message = 'This is client message #%d.' % count
        print('    [me]: %s' % message)
        count += 1
        await sio.sleep(1)
        await sio.emit('client_said', { 'message': message })
    else:
        await sio.disconnect()

@sio.event
async def disconnect():
    print('[server]: disconnected')

async def main():
    await sio.connect('ws://localhost:63047', transports=['websocket'])
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(main())
