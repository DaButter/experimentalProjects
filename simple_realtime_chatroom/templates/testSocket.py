# Other program that shows new messages on refresh/or when messages are already sent
from flask import Flask, request, render_template, session
from datetime import datetime
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

messages = []


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        print("Need to get name, redirect to getname.html")
        return render_template('getname.html')

    if request.method == 'POST':
        message = request.form['message']
        username = session['username']
        now = datetime.now().strftime('%H:%M:%S')

        new_data = f"{now} - {username}: {message}"
        print(f"Data to be appended: {new_data }")
        messages.append(f"{new_data }")
        print(f"Messages content full: {messages}")

        # socketio.emit('new_message', {'data': f"{username}: {message}"})  # broadcast=True
        # socketio.emit('new_message', data=new_data, room=None, namespace=None, include_self=True)
        # return render_template('index.html', messages=messages)

    return render_template('index.html', messages=messages)


@app.route('/setname', methods=['POST'])
def setname():
    print("Need to get username in /setname ")
    username = request.form['username']
    print(f"Got username in /setname: {username}")
    print("Redirect to index.html")
    session['username'] = username
    return render_template('index.html', messages=messages)


# @socketio.on('new_message')
# def handle_message(data):
#     print("I was at handle_connect")
#     print(f"Data received for broadcast: {data}")
    # emit('messages', data, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000, debug=True, allow_unsafe_werkzeug=True)
