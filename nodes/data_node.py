from flask import request, Flask, make_response,jsonify
app = Flask(__name__)

import threading #
lock = threading.Lock() #
messages = []

# @app.route('/receive')
# def get_message():
#     global messages


#     temp = messages.pop(0)    #треба переробити щоб воно було або у файлі або на диску
#     return temp

@app.route('/receive')
def get_message():
    global messages


    if messages:
        temp = messages.pop(0)
        return temp
    else:
        # Return a custom JSON response when there are no messages
            response_data = 'No data!'
            return jsonify(response_data), 200

@app.post('/send')
def send_message():
    global messages 
    mes = request.data
    messages.append(mes)

    return make_response()
@app.route('/stats')
def stats():
    global messages

    return str(len(messages))


if __name__ == '__main__':

    app.run(debug=True, host='localhost',port=5001)
# python -m flask --app data_node run --port 5001