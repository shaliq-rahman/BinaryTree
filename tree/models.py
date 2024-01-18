from django.db import models

# Create your models here.
class ParentNode(models.Model):
    name = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    

NODE_POSITION = (
    (1, 'left'),
    (2, 'right')
)
# class SubNode(models.Model):
#     name = models.CharField(max_length=250)
#     parent = models.ForeignKey(ParentNode, on_delete=models.CASCADE, null=True, blank=True)
#     sub_parent = models.ForeignKey("self", on_delete=models.CASCADE)
#     has_childs = models.BooleanField(default=False)
#     position = models.PositiveIntegerField(choices=NODE_POSITION, null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True, blank=True)
    
class Node(models.Model):
    name = models.CharField(max_length=250)
    parent = models.ForeignKey(ParentNode, on_delete=models.CASCADE, null=True, blank=True)
    sub_parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    has_childs = models.BooleanField(default=False)
    is_root = models.BooleanField(default=False)
    position = models.PositiveIntegerField(choices=NODE_POSITION, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    
    
    
    
