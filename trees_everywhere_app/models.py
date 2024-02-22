from django.db import models
from django.contrib.auth.models import User as BaseUser

class Account(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    users = models.ManyToManyField(BaseUser, related_name='accounts')

class Profile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    about = models.TextField()
    joined = models.DateTimeField(auto_now_add=True)

class Tree(models.Model):
    name = models.CharField(max_length=255)
    scientific_name = models.CharField(max_length=255)


class PlantedTree(models.Model):
    age = models.IntegerField(default=0)
    planted_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='planted_trees')
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    @property
    def location(self):
        return (self.latitude, self.longitude)

    @location.setter
    def location(self, value):
        self.latitude, self.longitude = value

    def __str__(self):
        return f"Tree planted by ({self.user})"

class User(BaseUser):
    def plant_tree(self, tree, latitude, longitude):
        planted_tree = PlantedTree.objects.create(
            user=self,
            tree=tree,
            account=self.accounts.first(),
            latitude=latitude,
            longitude=longitude
        )
        return planted_tree

    def plant_trees(self, trees):
        planted_trees = []
        for tree, (latitude, longitude) in trees:
            planted_tree = PlantedTree.objects.create(
                user=self,
                tree=tree,
                account=self.accounts.first(),  # Assume que o usuário está associado a uma conta
                latitude=latitude,
                longitude=longitude
            )
            planted_trees.append(planted_tree)
        return planted_trees
