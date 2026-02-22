from decimal import Decimal
from urllib import response
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User, Permission
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.contrib.auth import get_user_model
from Restaurant.models import Menu

class BookingURLTests(APITestCase):
    def setUp(self):
        # Use an existing superuser to authenticate API requests
        self.user = User.objects.create_superuser( username="admin", email="", password="12345") 
        self.client = APIClient() 
        self.client.login(username="admin", password="12345")

        # Create an initial booking to test against
        url = reverse('tables-list')
        data = {"Name": "Initial Booking", "No_of_guests": 2}
        response = self.client.post(url, data, format='json')
        self.booking_id = response.data.get("id")

    def test_booking_tables_create(self):
        url = reverse('tables-list')
        data = {"Name": "Test Booking", "No_of_guests": 4}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["Name"], "Test Booking")
        self.assertEqual(response.data["No_of_guests"], 4)

    def test_booking_tables_list(self):
        url = reverse('tables-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_booking_tables_detail(self):
        url = reverse('tables-detail', args=[self.booking_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["Name"], "Initial Booking")

    def test_booking_tables_update(self):
        url = reverse('tables-detail', args=[self.booking_id])
        data = {"Name": "Updated Booking", "No_of_guests": 6}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["No_of_guests"], 6)

    def test_booking_tables_partial_update(self):
        url = reverse('tables-detail', args=[self.booking_id])
        data = {"No_of_guests": 8}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["No_of_guests"], 8)

    def test_booking_tables_delete(self):
        url = reverse('tables-detail', args=[self.booking_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


User = get_user_model()

class UserPermissionTests(APITestCase):

    def setUp(self):
        # User to be modified/deleted
        self.target_user = User.objects.create_user(
            username="target",
            password="testpass"
        )
        # User WITHOUT permissions
        self.user_no_perm = User.objects.create_user(
            username="noperm",
            password="testpass"
        )
        # User WITH permissions
        self.user_with_perm = User.objects.create_user(
            username="withperm",
            password="testpass"
        )

        content_type = ContentType.objects.get_for_model(User)

        # Get permissions
        self.add_perm = Permission.objects.get(
            codename="add_user",
            content_type=content_type
        )
        self.view_perm = Permission.objects.get(
            codename="view_user",
            content_type=content_type
        )
        self.change_perm = Permission.objects.get(
            codename="change_user",
            content_type=content_type
        )
        self.delete_perm = Permission.objects.get(
            codename="delete_user",
            content_type=content_type
        )

        # Assign permissions
        self.user_with_perm.user_permissions.add(
            self.add_perm,
            self.view_perm,
            self.change_perm,
            self.delete_perm
        )

        self.list_url = reverse("user-list")
        self.detail_url = reverse("user-detail", args=[self.target_user.id])

        #add users
        def test_user_with_permission_can_add_user(self):
            self.client.force_authenticate(user=self.user_with_perm)
            response = self.client.post(
                self.list_url,
                {
                    "username": "newuser",
                    "password": "testpass123"
                },
                format='json'
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        def test_user_without_permission_cannot_add_user(self):
            self.client.force_authenticate(user=self.user_no_perm)
            response = self.client.post(
            self.list_url,
            {
                "username": "newuser",
                "password": "testpass123"
            },
            format='json'
            )
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #view users
        def test_user_with_permission_can_view_users(self):
            self.client.force_authenticate(user=self.user_with_perm)
            response = self.client.get(self.list_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        def test_user_without_permission_cannot_view_users(self):
            self.client.force_authenticate(user=self.user_no_perm)
            response = self.client.get(self.list_url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        #change users
        def test_user_with_permission_can_change_user(self):
            self.client.force_authenticate(user=self.user_with_perm)
            response = self.client.patch(
                self.detail_url,
                {"username": "updated"},
                format='json'
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        def test_user_without_permission_cannot_change_user(self):
            self.client.force_authenticate(user=self.user_no_perm)
            response = self.client.patch(
                self.detail_url,
                {"username": "updated"},
                format='json'
            )
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #delete users
        def test_user_with_permission_can_delete_user(self):
            self.client.force_authenticate(user=self.user_with_perm)
            response = self.client.delete(self.detail_url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        def test_user_without_permission_cannot_delete_user(self):
            self.client.force_authenticate(user=self.user_no_perm)
            response = self.client.delete(self.detail_url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MenuViewTest(APITestCase):
    def setUp(self):
        self.item = Menu.objects.create(Title="Greek Salad", Price=Decimal("12.00"), Inventory=5)
        self.admin_user = User.objects.create_superuser(username='admin', password='password123')
        #self.client = APIClient()
        #self.client.force_authenticate(user=self.admin_user)

    def test_get_all_items(self):
        """Test that any user can view the menu (GET /menu/)"""
        response = self.client.get(reverse('menu-items'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the data returned is a list and contains our item
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['Title'], "Greek Salad")

    def test_get_single_item(self):
        """Test retrieving a specific dish (GET /menu/id/)"""
        self.client.login(username='admin', password='password123')
        url = reverse('single-menu-item', kwargs={'pk': self.item.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Price'], "12.00")

    def test_create_menu_item_restricted(self):
        """Test that anonymous users CANNOT add items (POST /menu/)"""
        url = reverse('menu-items')
        data = {"Title": "Pizza", "Price": Decimal("15.00"), "Inventory": 10}
        response = self.client.post(url, data)
        # Should be 401 or 403 because they aren't logged in/admin
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_admin_can_create_item(self):
        """Test that an authorized admin can add items"""
        url = reverse('menu-items')
        self.client.force_authenticate(user=self.admin_user)
        data = {"Title": "Pasta", "Price": Decimal("14.00"), "Inventory": 20}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)