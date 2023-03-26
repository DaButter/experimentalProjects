from flask import Flask, request, render_template, session
from datetime import datetime
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

messages = []
print("This is a TEST")


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        print("Need to get name: ")
        return render_template('getname.html')

    if request.method == 'POST':
        message = request.form['message']
        username = session['username']
        now = datetime.now().strftime('%H:%M:%S')
        messages.append(f"{now} - {username}: {message}")
        socketio.emit('new_message', {'message': f"{username}: {message}"})  # boradcast=True
        return render_template('index.html', messages=messages)

    return render_template('index.html', messages=messages)


@app.route('/setname', methods=['POST'])
def setname():
    print("Need to get name: ")
    username = request.form['username']
    session['username'] = username
    return render_template('index.html', messages=messages)


@socketio.on('new_message')
def handle_connect(message):
    print(f"Data received for broadcast: {message}")
    emit('messages', message, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000, debug=True, allow_unsafe_werkzeug=True)
