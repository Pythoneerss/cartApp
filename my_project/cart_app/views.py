from django.shortcuts import render
from django.forms import ModelChoiceField
from django.core.serializers import serialize

#import first the model added in the model.py
from django.http import JsonResponse
import json
from .models import GridNode
from django.views.decorators.csrf import csrf_exempt
from .models import led_status
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Esp32Command


# this section will be the get all the data from the database
# the data from the data base will be convert to json to make it easy for the js to pars

def grid_editor_view(request):
    nodes_queryset = GridNode.objects.all()
    for node in nodes_queryset:
        print(f"Retrieved node name: {node.name}") 
    form_field = ModelChoiceField(queryset=nodes_queryset, empty_label="Select a Node ID")
    nodes_json = serialize(
        'json', 
        nodes_queryset,     
        fields=('id', 'custom_id', 'name', 'x_coord', 'y_coord', 'owner',
                'north_node', 'south_node', 'east_node', 'west_node')
    )
    context = {
        'node_dropdown_field': form_field,
        'nodes_data_json': nodes_json,
    }
    return render(request, 'index.html', context)

def getdata(request):
    Nodes = GridNode.objects.all()
    return JsonResponse({"Nodes":list(Nodes.values())})

@csrf_exempt
def set_command(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        new_state = data.get("status")

        # store the command
        cmd, created = Esp32Command.objects.get_or_create(name="blink")
        cmd.status = new_state
        cmd.save()

        return JsonResponse({"success": True, "status": new_state})

    return JsonResponse({"success": False, "message": "POST only"}, status=405)

def esp32_command(request):
    try:
        cmd = Esp32Command.objects.get(name="blink")
        return JsonResponse({"blink": cmd.status})
    except Esp32Command.DoesNotExist:
        return JsonResponse({"blink": False})

@csrf_exempt
def update_status(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        device_id = data.get("device_id")
        status = data.get("status")

        print(device_id)
        print(status)

        status_bool = True if status == "On" else False

        print(status_bool)
        led_status.objects.create(device_id=device_id, status=status_bool)

        return JsonResponse({"status": "success", "received": data})
    return JsonResponse({"status": "error", "message": "POST only"}, status=405)


def status_display(request):
    try:
        device_status = led_status.objects.filter(device_id="esp32-001").latest('timestamp')
        
        data = {
            'device_id': device_status.device_id,
            'status': "On" if device_status.status else "Off",
            'last_update': device_status.timestamp.isoformat(),
            'success': True
        }
        return JsonResponse(data, status=200)

    except led_status.DoesNotExist:
        error_data = {
            'status': 'error',
            'message': 'Device not found',
            'success': False
        }
        return JsonResponse(error_data, status=404)

# /blink
# GET -> server return current state (client/esp32)
# POST -> change blink state (client)
    