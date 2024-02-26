from rest_framework import serializers
from .models import PlantedTree, Tree

class TreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tree
        fields = ['id', 'name', 'scientific_name']

class PlantedTreeSerializer(serializers.ModelSerializer):
    tree = TreeSerializer() 

    class Meta:
        model = PlantedTree
        fields = ['id', 'tree', 'planted_at', 'latitude', 'longitude']
