from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Account, Tree, PlantedTree

class TestScenario(TestCase):
    def setUp(self):
        # Create two accounts
        self.account1 = Account.objects.create(name='Account 1')
        self.account2 = Account.objects.create(name='Account 2')

        # Create three users
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.user3 = User.objects.create_user(username='user3', password='password3')

        # Associate users with accounts
        self.account1.users.add(self.user1, self.user2)
        self.account2.users.add(self.user3)

        # Create some trees
        self.tree1 = Tree.objects.create(name='Tree 1', scientific_name='Scientific Name Tree 1')
        self.tree2 = Tree.objects.create(name='Tree 2', scientific_name='Scientific Name Tree 2')

        # Create some planted trees for each user
        self.planted_tree1_user1 = self.user1.plant_tree(tree=self.tree1, latitude=0.1, longitude=0.2)
        self.planted_tree2_user1 = self.user1.plant_tree(tree=self.tree2, latitude=0.2, longitude=0.3)
        self.planted_tree1_user2 = self.user2.plant_tree(tree=self.tree1, latitude=0.3, longitude=0.4)
        self.planted_tree1_user3 = self.user3.plant_tree(tree=self.tree1, latitude=0.4, longitude=0.3)

    def test_scenario(self):
        # Check if the accounts were created correctly
        self.assertEqual(Account.objects.count(), 2)
        # Check if the users were associated with the accounts correctly
        self.assertEqual(self.account1.users.count(), 2)
        self.assertEqual(self.account2.users.count(), 1)
        # Check if the trees were planted correctly by each user
        self.assertEqual(PlantedTree.objects.filter(account=self.account1).count(), 3)
        self.assertEqual(PlantedTree.objects.filter(account=self.account2).count(), 1)
    
    def test_planted_trees_template(self):
        # Login as a user
        self.client = Client()
        self.client.login(username='user1', password='password1')

        # Get the response when accessing the user's planted trees page
        response = self.client.get(reverse('planted_trees'))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the correct template is being used
        self.assertTemplateUsed(response, 'planted_trees.html')

        # Check if the page content contains information about the trees planted by the user
        self.assertContains(response, 'Tree 1')
        self.assertContains(response, 'Tree 2')

    def test_user_account_planted_trees_template(self):
        # Log in as user1 (member of account1)
        self.client.login(username='user1', password='password1')

        # Access the page that lists trees planted by users of the accounts the logged-in user belongs to
        response = self.client.get(reverse('user_planted_trees'))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if information about trees planted by users of the accounts the logged-in user belongs to is present in the template
        self.assertContains(response, 'Tree 1')
        self.assertContains(response, 'Tree 2')

    def test_plant_tree_method(self):
        # Check if the plant_tree method creates a PlantedTree associated with the user
        planted_tree = self.user1.plant_tree(tree=self.tree1, latitude=0.5, longitude=0.6)
        
        self.assertEqual(planted_tree.user, self.user1)  # Check if the user is correct
        self.assertEqual(planted_tree.tree, self.tree1)  # Check if the tree is correct
        self.assertEqual(planted_tree.latitude, 0.5)  # Check if the latitude is correct
        self.assertEqual(planted_tree.longitude, 0.6)  # Check if the longitude is correct

    def test_plant_trees_method(self):
        # Create a list of tuples (tree, latitude, longitude)
        trees = [(self.tree1, (0.1, 0.2)), (self.tree2, (0.2, 0.3))]

        # Check if the plant_trees method creates PlantedTrees associated with the user
        planted_trees = self.user1.plant_trees(trees)

        self.assertEqual(len(planted_trees), 2)  # Check if two PlantedTrees were created
        
        for i, (tree, location) in enumerate(trees):
            self.assertEqual(planted_trees[i].user, self.user1)  # Check if the user is correct
            self.assertEqual(planted_trees[i].tree, tree)  # Check if the tree is correct
            self.assertEqual(planted_trees[i].latitude, location[0])  # Check if the latitude is correct
            self.assertEqual(planted_trees[i].longitude, location[1])  # Check if the longitude is correct


