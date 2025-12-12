from django.contrib import admin
from .models import GridNode

# Register your models here.
class GridNodeAdmin(admin.ModelAdmin):
    list_display = (
        'custom_id', 
        'name', 
        'owner', 
        'x_coord', 
    )
    search_fields = ('custom_id', 'name', 'owner__username') # Now search by name too
    list_filter = ('owner',) 

admin.site.register(GridNode)

