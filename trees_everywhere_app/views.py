from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .forms import LoginForm, PlantedTreeForm
from .models import PlantedTree
from .serializers import PlantedTreeSerializer

class UserPlantedTreesAPIView(generics.ListAPIView):
    serializer_class = PlantedTreeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return PlantedTree.objects.filter(user=user)

def user_planted_trees_view(request):
    user_accounts = request.user.accounts.all()
    planted_trees = PlantedTree.objects.filter(account__in=user_accounts)
    return render(request, 'user_planted_trees.html', {'planted_trees': planted_trees})

def add_planted_tree_view(request):
    if request.method == 'POST':
        form = PlantedTreeForm(request.POST)
        if form.is_valid():
            planted_tree = form.save(commit=False)
            tree = form.cleaned_data['tree']
            account = form.cleaned_data['account']
            planted_tree.user = request.user
            planted_tree.tree = tree
            planted_tree.account = account
            planted_tree.save()
            return redirect('planted_trees')
    else:
        form = PlantedTreeForm()
    return render(request, 'add_planted_tree.html', {'form': form})

def planted_trees_view(request):
    user = request.user
    user_first_account = user.accounts.first()
    planted_trees = PlantedTree.objects.filter(account = user_first_account)
    form = PlantedTreeForm()
    return render(request, 'planted_trees.html', {'planted_trees': planted_trees, 'form': form})

def tree_details_view(request, tree_id):
    tree = get_object_or_404(PlantedTree, pk=tree_id)
    return render(request, 'tree_details.html', {'tree': tree})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('planted_trees')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
