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

@app.route("/add/<addr>")
def add_node(addr):
    if addr in data_node_list:
        pass
    else:
        data_node_list.append(addr)    #перевірка чи ще такого немає
    return make_response()

@app.route("/remove/<addr>")
def remove_node(addr):
    data_node_list.remove(addr)
    return make_response()

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

#попробувати в зв'язі і запускати на різниї портах