from django.db import models

class Booking(models.Model):
    Name = models.CharField(max_length=255)
    No_of_guests = models.IntegerField()
    BookingDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.Name} - {self.BookingDate}"
    
class Menu(models.Model):
    Title = models.CharField(max_length=255)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Inventory = models.IntegerField()

    def get_item(self):
        return f'{self.Title} : (str{self.Price})'
    

