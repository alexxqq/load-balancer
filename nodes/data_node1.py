from flask import request, Flask, make_response
app = Flask(__name__)

messages = []

@app.route('/receive')
def get_message():
    global messages
    temp = messages.pop(0)    #треба переробити щоб воно було або у файлі або на диску
    print(messages)
    return temp
@app.post('/send')
def send_message():
    global messages 
    mes = request.data
    messages.append(mes)
    print(messages)
    return make_response()
@app.route('/stats')
def stats():
    global messages
    print(messages)
    return str(len(messages))

if __name__ == '__main__':

    app.run(debug=True, host='localhost',port=5001)
# python -m flask --app data_node run --port 5002