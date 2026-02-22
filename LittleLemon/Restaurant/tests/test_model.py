from decimal import Decimal
from django.test import TestCase
from Restaurant.models import Menu, Booking

class BookingTestCase(TestCase):
    def setUp(self):
        self.item = Booking.objects.create(Name="John Doe", No_of_guests=4)

    def test_booking_creation(self):
        booking = Booking.objects.get(Name="John Doe")
        self.assertEqual(booking.Name, "John Doe")
        self.assertEqual(booking.No_of_guests, 4)

    def test_booking_update(self):
        self.item.No_of_guests = 5
        self.item.save()
        booking = Booking.objects.get(Name="John Doe")
        self.assertEqual(booking.No_of_guests, 5)

    def test_booking_deletion(self):
        self.item.delete()
        exists = Booking.objects.filter(Name="John Doe").exists()
        self.assertFalse(exists)

class MenuTestCase(TestCase):
    def setUp(self):
        self.item = Menu.objects.create(Title="Pasta", Price=Decimal("12.99"), Inventory=10)

    def test_menu_creation(self):
        menu_item = Menu.objects.get(Title="Pasta")
        self.assertEqual(menu_item.Title, "Pasta")
        self.assertEqual(menu_item.Price, Decimal("12.99"))
        self.assertEqual(menu_item.Inventory, 10)

    def test_menu_update(self):
        self.item.Price = Decimal("14.99")
        self.item.save()
        menu_item = Menu.objects.get(Title="Pasta")
        self.assertEqual(menu_item.Price, Decimal("14.99"))

    def test_menu_deletion(self):
        self.item.delete()
        exists = Menu.objects.filter(Title="Pasta").exists()
        self.assertFalse(exists)
