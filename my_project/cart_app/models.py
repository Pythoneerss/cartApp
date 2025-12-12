from django.db import models
from django.contrib.auth.models import User 


# Nodes in grid model
# each nodes have different coordinates and connections with respect to their position in cartitial plane
class GridNode(models.Model):
    name = models.CharField(max_length=100, help_text="A human-readable name for the location.")
    custom_id = models.CharField(max_length=20, unique=True)
    x_coord = models.IntegerField()
    y_coord = models.IntegerField()

    north_node = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='south_neighbors'
    )
    south_node = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='north_neighbors'
    )
    east_node = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='west_neighbors'
    )
    west_node = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='east_neighbors'
    )

    def __str__(self):
        return f"{self.name} ({self.custom_id})"
    
class led_status(models.Model):
    device_id = models.CharField(max_length=50)
    status = models.BooleanField(max_length=10)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.device_id is {self.status}}"
    
class Esp32Command(models.Model):
    name = models.CharField(max_length=50)    
    status = models.BooleanField(default=False)  
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}: {self.status}"
