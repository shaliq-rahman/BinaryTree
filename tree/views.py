from django.shortcuts import render
from django.views import View
from .forms import NodeCreationForm
from django.db import transaction
from django.contrib import messages
import pdb
from .models import *

class HomePage(View):
    template_name = "home.html"
    def get(self, request, *args, **kwargs):
        datas = {}
        return render(request, self.template_name, datas)
    

class CreateParentNode(View):
    template_name = "node_form.html"
    
    def get(self, request, *args, **kwargs):
        form = NodeCreationForm()
        nodes = Node.objects.filter(is_active= True)
        parent_node = Node.objects.filter(is_active=True, is_root=True)
        datas = {'form':form, 'nodes':nodes, 'parent_node':parent_node}
        return render(request, self.template_name, datas)
    
    def post(self, request, *args, **kwargs):
        nodes = Node.objects.filter(is_active= True)
        parent_node = Node.objects.filter(is_active=True, is_root=True)
        datas = {'nodes':nodes, 'parent_node':parent_node}
        create_conditions = {}
        try:
            name = request.POST.get('node_name', None)
            parent_node = request.POST.get('parent_node', None)
            position = request.POST.get('position', None)
            if parent_node:
                parent =  Node.objects.filter(id=parent_node)
                if parent:
                    if parent[0].has_childs:
                        childs = Node.objects.filter(sub_parent=parent[0])
                        if childs:
                            for child in childs:
                                if child.position == int(position):
                                    messages.error(request, "No more insertion Possible")
                                    return render(request, self.template_name, datas)     
                Node.objects.filter(id=parent_node).update(has_childs=True)
            if name:
                create_conditions['name'] = name
            if parent_node:
                create_conditions['sub_parent_id'] = parent_node
            if position:
                create_conditions['position'] = position
            
            if Node.objects.filter(name=name).exists():
                messages.error(request, "Data already Exists")
                return render(request, self.template_name, datas)
            
            if not Node.objects.filter(is_active=True).exists():
                create_conditions['is_root'] = True
            Node.objects.create(**create_conditions)
            messages.success(request, "Data inserted successfully")
        except Exception as error:
            messages.warning(request, "Data was not inserted")
            print(error)
            return render(request, self.template_name, datas)
        return render(request, self.template_name, datas)
    

class SearchNode(View):
    template_name = "node_search_form.html"
    
    def get(self, request, *args, **kwargs):
        nodes = Node.objects.filter(is_active= True)
        parent_node = Node.objects.filter(is_active=True, is_root=True)
        datas = {'nodes':nodes, 'parent_node':parent_node}
        return render(request, self.template_name, datas)
    
    def post(self, request, *args, **kwargs):
        parent_node = request.POST.get('parent_node', None)
        position = request.POST.get('position', None)
        nodes = Node.objects.filter(is_active=True)
        datas = {}
        datas['position'] = position
        
        try:
            parent_node = Node.objects.get(id=parent_node)
            primary_node = parent_node
            while 1:
                if parent_node.has_childs:
                    item_exist =  Node.objects.filter(sub_parent=parent_node, position=position)
                    if item_exist:
                        parent_node = Node.objects.get(sub_parent=parent_node, position=position)
                    else:
                        searched_node = parent_node
                        datas['searched_node'] = searched_node
                        
                        if primary_node == searched_node:
                            datas['search_found'] = False
                        else:
                            datas['search_found'] = True
                        break
                else:
                    searched_node = parent_node
                    datas['searched_node'] = searched_node
                    if primary_node == searched_node:
                        datas['search_found'] = False
                    else:
                        datas['search_found'] = True
                    break
        except Exception as dberror:
            print(dberror)
        datas['nodes'] = nodes
        return render(request, self.template_name, datas)
    
    
    

# def post(self, request, *args, **kwargs):
#         parent_node = request.POST.get('parent_node', None)
#         position = request.POST.get('position', None)
#         nodes = Node.objects.filter(is_active=True)
#         datas = {}
#         try:
#             parent_node = Node.objects.get(id=parent_node)
#             primary_node = parent_node
#             while 1:
#                 if parent_node.has_childs:
#                     parent_node = Node.objects.get(sub_parent=parent_node, position=position)
#                 else:
#                     searched_node = parent_node
#                     datas['searched_node'] = searched_node
#                     if primary_node == searched_node:
#                         datas['search_found'] = False
#                     else:
#                         datas['search_found'] = True
#                     break
#         except Exception as dberror:
#             print(dberror)
#         datas['nodes'] = nodes
#         return render(request, self.template_name, datas)
        
        

        