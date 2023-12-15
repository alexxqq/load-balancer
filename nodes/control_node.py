from data_node import *    
from flask import request, Flask, make_response,jsonify
import requests

app = Flask(__name__)

page = '''
<head>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
</head>
<body>
    <input type="text"> 
    <button>Add</button>
    <script>
        $("button").click(function(){
            var a = $("input").val();
            var url = "add/" + a;
            $.get(url, function(data, status){
                console.log(status);
            });
        });
    </script>
</body>
'''

data_node_list = []
stats = {}
counter = 0
update_stats_counter = 5

@app.route("/page")
def make_page():
    return page

# @app.route("/add/<addr>")
# def add_node(addr):
#     if addr in data_node_list:
#         pass
#     else:
#         data_node_list.append(addr)    #перевірка чи ще такого немає
#     return make_response()
@app.route("/add/<addr>")
def add_node(addr):
    if addr in data_node_list:
        pass
    else:
        data_node_list.append(addr)
        with open("D:\\django\\anaboliy\\server\\app\\info.txt", "r") as file:
            file.seek(0)
            text = file.readlines()
            if f"ID: {addr}\n" not in text:
                text.append(f"ID: {addr}\n")
                text.append("Access: Allowed\n")
            elif f"ID: {addr}\n" in text:
                text[text.index(f"ID: {addr}\n") + 1] = "Access: Allowed\n"
        with open("D:\\django\\anaboliy\\server\\app\\info.txt", "w") as file:
            for i in text:
                file.write(i)
        return make_response()
# @app.route("/remove/<addr>")
# def remove_node(addr):
#     data_node_list.remove(addr)
#     return make_response()
@app.route("/remove/<addr>")
def remove_node(addr):
    if addr in data_node_list:
        data_node_list.remove(addr)
        with open("D:\\django\\anaboliy\\server\\app\\info.txt", "r") as file:
            file.seek(0)
            text = file.readlines()
            lines_to_transfer = []
            i = 0
            while i != len(text):
                if text[i] == f"ID: {addr}\n":
                    text[i + 1] = "Access: Disallowed\n"
                    break
                else:
                    i += 1
            if "Allowed" in file.read():
                if "ID" not in text[i + 2]:
                    i += 2
                    while "ID" in text[i]:
                        if "active" in text[i]:
                            lines_to_transfer.append(text[i])
                            text[i] = ", ".join(list(text[i].split(",")[0], "non-active"))
                        i += 1
                    k = 0
                    while k != len(text):
                        if "Access: Allowed" in text[k]:
                            k -= 1
                            break
                        else:
                            k += 1
                    text = text[0 : k + 2] + lines_to_transfer + text[k + 2 :]
                    accessed_id = text[k].strip().split(": ")[1]
                    for message in lines_to_transfer:
                        requests.post(f"http://{accessed_id}/send", data=message)
                else:
                    pass
            else:
                pass
        with open("D:\\django\\anaboliy\\server\\app\\info.txt", "w") as file:
            for i in text:
                file.write(i)
        return make_response()
    else:
        pass




@app.route("/list")
def get_nodes():
    return data_node_list   

def get_stats():
    global counter
    global stats
    updated_stats = {}  # Створюємо новий словник для оновлених значень
    for addr in data_node_list:
        result = requests.get(f"http://{addr}/stats")
        if result.status_code == 200:
            node_stats = int(result.text)
            updated_stats[addr] = node_stats
        else:
            print(result.raw)

    # Оновлюємо старий словник новими значеннями
    stats = updated_stats


@app.route("/stats")
def get_data_node_stats():
    global stats
    get_stats()
    return stats
# python -m flask --app control_node run  
