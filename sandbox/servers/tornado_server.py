import asyncio
import socketio
import tornado.ioloop
import tornado.web

PORT = 63047
count = 0
sio = socketio.AsyncServer(async_mode='tornado')
app = tornado.web.Application([
    (r"/socket.io/", socketio.get_tornado_handler(sio))
])
tick_queue = asyncio.Queue()
tock_queue = asyncio.Queue()

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
        print('tick_dequeue() qsize=%d' % tick_queue.qsize(), True)

async def tick_enqueue():
    print('tick_enqueue() start', True)
    while True:
        await asyncio.sleep(1)
        await tick_queue.put({
            'security_code': '2330.TW',
            'close': 601.15
        })
        print('tick_enqueue()', True)

async def init_task():
    print('init_task()', flush=True)
    for i in range(100):
        await tock_queue.put({ 'foo': 'bar%d' % i })

async def loop_task():
    while True:
        print('loop_task()', flush=True)
        tock = await tock_queue.get()
        await sio.emit('tock', tock)
        await sio.sleep(1)

# 非同步背景工作放在 main() 或是 global 都正常
# sio.start_background_task(init_task)
# sio.start_background_task(loop_task)

def main():
    print('==============================')
    print('    async_mode = tornado')
    print('==============================')
    # 非同步背景工作放在 main() 或是 global 都正常
    sio.start_background_task(init_task)
    sio.start_background_task(loop_task)
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
