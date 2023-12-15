from django.shortcuts import render,redirect
from django.http import HttpResponse
import requests
from django.http import JsonResponse
from .forms import *
import json
# Create your views here.
control_node = '127.0.0.1:5000'
addresses = [f'127.0.0.1:500{i}' for i in range(1,10)]
class Client():
    def __init__(self, addr, step = 10):
        self.addr = addr
        self.stats = {}
        self.counter = 0
        self.step = step  

    def get_stats(self):
        s = requests.get(f"http://{control_node}/stats")
        #s = requests.get(f"http://{self.addr}/stats")

        self.stats = s.json()

    
    def update_stats(self):
        self.counter = (self.counter + 1) % self.step
        if self.counter == 0:
            self.get_stats()

    def send(self, message):

        self.update_stats()
        self.get_stats()
        
        dn_addr = min(self.stats.items(), key = lambda pair : int(pair[1]))[0]
        with open("D:\\django\\anaboliy\\server\\app\\info.txt", "r") as file:
            file.seek(0)
            text = file.readlines()
            for i in range(len(text)):
                if f"{dn_addr}" in text[i]:
                    text.insert(i + 2, f"{message}, active\n")
                    break
        with open("D:\\django\\anaboliy\\server\\app\\info.txt", "w") as file:
            for i in text:
                file.write(i)
        requests.post(f"http://{dn_addr}/send", data = message)     
        #requests.post(f"http://{self.addr}/send", data = message)     

    def receive(self):
        self.update_stats()
        self.get_stats()



        if self.stats.items():
            dn_addr = max(self.stats.items(), key = lambda p : int(p[1]))[0]
            with open("D:\\django\\anaboliy\\server\\app\\info.txt", "r") as file:
                file.seek(0)
                text = file.readlines()
                i = 0
                while i != len(text):
                    if text[i] == f"ID: {dn_addr}\n":
                        i += 2
                        break
                    else:
                        i += 1
                if i < len(text):
                    while "ID:" in text[i]:
                        if "non-active" in text[i]:
                            i += 1
                        elif ", active" in text[i]:
                            text[i] = text[i][0: text[i].index("active")] + "non-active"
            with open("D:\\django\\anaboliy\\server\\app\\info.txt", "w") as file:
                for i in text:
                    file.write(i)
            to_return=requests.get(f"http://{dn_addr}/receive")
            if to_return.status_code == 200:
                return to_return.text 
        #     else:
        #         return "No data to receive!"
        # else:
        #     raise Exception('no node')
        # return requests.get(f"http://{self.addr}/receive").text   



def base(request):
    control_node_url = f'http://{control_node}/list'

    response = requests.get(control_node_url)

    if response.status_code == 200:

        nodes_list = response.json()

    context ={'list' : nodes_list}


    return render(request, 'app/base.html',context)



def send_data_to_node(request):
    if request.method == 'POST':
        
        input_field_data = request.POST.get('input_field', None)
        client = Client(addr=f'{control_node}')  

        try:

            message = input_field_data

            client.send(message)
            return render(request,'app/successorfail.html',{'result': f'Data "{message}" sent successfully.'})

        except Exception as e:
            return render(request,'app/successorfail.html',{'result': f'Failed to send data. No nodes available.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def add_node(request):

    if request.method == 'POST':
        
        input_field_data = request.POST.get('input_field', None)

        control_node_url = f'http://{control_node}/list'


        # response = requests.get(control_node_url)

        # if response.status_code == 200:

        #     nodes_list = response.json()
    

        if input_field_data not in addresses:
             return render(request,'app/successorfail.html',{'result': f"Node '{input_field_data}' not in available nodes."})
        control_node_url = f'http://{control_node}/add'
        new_data_node_address = input_field_data

        response = requests.get(f"{control_node_url}/{new_data_node_address}")

        if response.status_code == 200:
            return render(request,'app/successorfail.html',{'result': f"Node '{new_data_node_address}' added successfully."})
        else:
            return render(request,'app/successorfail.html',{'result': f"Failed to add node. Status code: {response.status_code}"})

    else:
        return redirect('base')

def get_nodes(request):

    control_node_url = f'http://{control_node}/list'


    response = requests.get(control_node_url)

    if response.status_code == 200:

        nodes_list = response.json()

        context ={'list' : nodes_list}
        return render(request,'app/base.html',context)
    else:
        return JsonResponse({'error': f"Failed to get nodes. Status code: {response.status_code}"}, status=500)
    
def remove_node(request):

    
    if request.method == 'POST':

        input_field_data = request.POST.get('input_field', None)
        addr = input_field_data
        control_node_url = f'http://{control_node}/remove/{addr}'
        response = requests.get(control_node_url)
        if response.status_code == 200:
            return render(request,'app/successorfail.html',{'result': f"Node '{addr}' removed successfully."})

        else:
            return render(request,'app/successorfail.html',{'result': f"Failed to remove node '{addr}'. Status code: {response.status_code}"})

    else:
        return redirect('base')

    

    

def receive_data_from_node(request):
    if request.method == 'GET':
        client = Client(addr=f'{control_node}') 


        try:
            received_data = client.receive()
            print(received_data)
        except:
            return render(request,'app/successorfail.html',{'result': 'No data available!'})
        if received_data is not None:
            return render(request,'app/successorfail.html',{'result': received_data})

        else:
            return render(request,'app/successorfail.html',{'result': 'No nodes available'})

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    

def get_data_node_stats(request):
    if request.method == 'GET':
        client = Client(addr=f'{control_node}')  # Replace with the actual address of your control node

        try:
            # Call the get_stats method to retrieve statistics from data nodes
            client.get_stats()

            # Return the statistics as a JSON response
            return render(request,'app/result.html',{'stats': client.stats})
        except Exception as e:
            return JsonResponse({'error': f'Failed to retrieve stats. {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)