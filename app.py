from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-me')
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

devices = {}   # device_id -> info
logs    = []   # event log

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/mobile')
def mobile():
    return render_template('mobile.html')

# ── WebSocket: موبايل يتصل ──────────────────────────────────────────────────
@socketio.on('device_hello')
def on_hello(data):
    did = data.get('id', request.sid)
    join_room(did)
    devices[did] = {
        'id':       did,
        'sid':      request.sid,
        'name':     data.get('name', 'Mobile'),
        'battery':  data.get('battery', '?'),
        'network':  data.get('network', '?'),
        'platform': data.get('platform', '?'),
        'screen':   data.get('screen', '?'),
        'ip':       request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr),
        'time':     datetime.now().strftime('%H:%M:%S'),
        'status':   'online',
    }
    _log(did, f"[CONNECTED] {devices[did]['name']}", 'info')
    socketio.emit('update', {'devices': list(devices.values()), 'logs': logs[-30:]})

@socketio.on('device_update')
def on_update(data):
    did = data.get('id', request.sid)
    if did in devices:
        devices[did].update({k: data[k] for k in ['battery','network'] if k in data})
        devices[did]['time'] = datetime.now().strftime('%H:%M:%S')
        socketio.emit('update', {'devices': list(devices.values()), 'logs': logs[-30:]})

@socketio.on('device_reply')
def on_reply(data):
    did = data.get('id', request.sid)
    _log(did, f"[REPLY] {data.get('msg','')}", 'reply')
    socketio.emit('update', {'devices': list(devices.values()), 'logs': logs[-30:]})

@socketio.on('send_command')
def on_command(data):
    did  = data.get('device_id')
    cmd  = data.get('cmd', '')
    _log(did, f"[CMD] {cmd}", 'cmd')
    socketio.emit('command', {'cmd': cmd}, room=did)
    socketio.emit('update', {'devices': list(devices.values()), 'logs': logs[-30:]})

@socketio.on('disconnect')
def on_disconnect():
    to_del = next((d for d, v in devices.items() if v['sid'] == request.sid), None)
    if to_del:
        name = devices[to_del]['name']
        devices[to_del]['status'] = 'offline'
        _log(to_del, f"[DISCONNECTED] {name}", 'warn')
        del devices[to_del]
        socketio.emit('update', {'devices': list(devices.values()), 'logs': logs[-30:]})

def _log(did, msg, kind='info'):
    entry = {'time': datetime.now().strftime('%H:%M:%S'), 'did': str(did)[:8], 'msg': msg, 'kind': kind}
    logs.append(entry)
    if len(logs) > 200: logs.pop(0)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
