from django.shortcuts import render,redirect
from django.http import HttpResponse
import requests
from django.http import JsonResponse
import json
# Create your views here.

class Client():
    def __init__(self, addr, step = 10):
        self.addr = addr
        self.stats = {}
        self.counter = 0
        self.step = step  

    def get_stats(self):
        s = requests.get(f"http://127.0.0.1:5000/stats")
        #s = requests.get(f"http://{self.addr}/stats")

        self.stats = s.json()

    
    def update_stats(self):
        self.counter = (self.counter + 1) % self.step
        if self.counter == 0:
            self.get_stats()

    def send(self, message):
        print(f'hello {self.stats}')
        self.update_stats()
        self.get_stats()
        dn_addr = min(self.stats.items(), key = lambda pair : int(pair[1]))[0]

        requests.post(f"http://{dn_addr}/send", data = message)     
        #requests.post(f"http://{self.addr}/send", data = message)     

    def receive(self):
        self.update_stats()
        self.get_stats()
        dn_addr = max(self.stats.items(), key = lambda p : int(p[1]))[0]
        return requests.get(f"http://{dn_addr}/receive").text 
        #return requests.get(f"http://{self.addr}/receive").text   



def base(request):
    control_node_url = 'http://127.0.0.1:5000/list'

    # Make a request to the control node to get the list of nodes
    response = requests.get(control_node_url)

    if response.status_code == 200:
        # Parse the response as JSON and return it
        nodes_list = response.json()

    context ={'list' : nodes_list}


    return render(request, 'app/base.html',context)



def send_data_to_node(request):
    if request.method == 'POST':
        # Assuming the data is sent as JSON in the request body
        input_field_data = request.POST.get('input_field', None)
        client = Client(addr='127.0.0.1:5001')  # Replace with the actual address of your control node

        try:

            message = input_field_data

            client.send(message)

            return JsonResponse({'message': 'Data sent successfully.'})
        except Exception as e:
            return JsonResponse({'error': f'Failed to send data. {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)










def add_node(request):

    if request.method == 'POST':
        # Access the input field data from the form submission
        input_field_data = request.POST.get('input_field', None)
        control_node_url = 'http://127.0.0.1:5000/add'
        new_data_node_address = input_field_data

        response = requests.get(f"{control_node_url}/{new_data_node_address}")

        if response.status_code == 200:
            return HttpResponse(f"Node '{new_data_node_address}' added successfully.")
        else:
            return HttpResponse(f"Failed to add node. Status code: {response.status_code}")
        return render(request,'app/base.html')
    else:
        return redirect('base')
    

def get_nodes(request):
    # Replace 'http://control_node_address:port' with the actual address and port of your control node
    control_node_url = 'http://127.0.0.1:5000/list'

    # Make a request to the control node to get the list of nodes
    response = requests.get(control_node_url)

    if response.status_code == 200:
        # Parse the response as JSON and return it
        nodes_list = response.json()

        context ={'list' : nodes_list}
        return render(request,'app/base.html',context)
    else:
        return JsonResponse({'error': f"Failed to get nodes. Status code: {response.status_code}"}, status=500)
    
def remove_node(request):
    # Replace 'http://control_node_address:port' with the actual address and port of your control node
    
    if request.method == 'POST':
        # Access the input field data from the form submission
        input_field_data = request.POST.get('input_field', None)
        addr = input_field_data
        control_node_url = f'http://127.0.0.1:5000/remove/{addr}'
        response = requests.get(control_node_url)
        if response.status_code == 200:
            return JsonResponse({'message': f"Node '{addr}' removed successfully."})
        else:
            return JsonResponse({'error': f"Failed to remove node '{addr}'. Status code: {response.status_code}"}, status=500)
            return render(request,'app/base.html')
    else:
        return redirect('base')

    

    

def receive_data_from_node(request):
    if request.method == 'GET':
        client = Client(addr='127.0.0.1:5001')  # Replace with the actual address of your control node

        # Call the receive method to get data from the data node with the maximum load
        received_data = client.receive()

        if received_data is not None:
            return JsonResponse({'data': received_data})
        else:
            return JsonResponse({'error': 'Failed to receive data. No data nodes available.'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    

def get_data_node_stats(request):
    if request.method == 'GET':
        client = Client(addr='127.0.0.1:5001')  # Replace with the actual address of your control node

        try:
            # Call the get_stats method to retrieve statistics from data nodes
            client.get_stats()

            # Return the statistics as a JSON response
            return JsonResponse({'stats': client.stats})
        except Exception as e:
            return JsonResponse({'error': f'Failed to retrieve stats. {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)