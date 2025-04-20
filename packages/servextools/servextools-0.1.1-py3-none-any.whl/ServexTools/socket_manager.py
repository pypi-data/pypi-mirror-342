import uuid
import ServexTools.Tools as Tools
from flask_socketio import SocketIO
import eventlet

_socketio_instance = None

def get_socketio():
    global _socketio_instance
    return _socketio_instance

def init_socketio(app,isProduccion=False,Proyecto="Servex"):
    global _socketio_instance
    if _socketio_instance is None:
        if not Tools.ExistFile('sctkRedis'):
            Tools.CreateFile(nombre="sctkRedis",datos=uuid.uuid4().hex)
        
        canalredis = Tools.ReadFile("sctkRedis")
        if isProduccion:
            eventlet.monkey_patch()
            _socketio_instance = SocketIO(app, 
                            ping_timeout=25000,
                            ping_interval=10000,
                            cors_allowed_origins="*",
                            async_mode='eventlet',
                            message_queue=f'redis://?db=0',
                            channel=Proyecto + canalredis,
                            logger=False,
                            engineio_logger=False)
        else:
            _socketio_instance = SocketIO(app, 
                        ping_timeout=5000,
                        ping_interval=2000,
                        cors_allowed_origins="*",
                        async_mode='threading')
    return _socketio_instance
