from django.db import models
from .account import Account

# Create your models here.
class UserTable(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='user')
    qa = models.TextField(null=True) # PLACEHOLDER TYPE

    def __str__(self):
        return self.account.username
    

class InterviewerTable(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='interviewer')
    schedule = models.TextField(null=True) # PLACEHOLDER TYPE
    blocked = models.TextField(null=True) # PLACEHOLDER TYPE

    def __str__(self):
        return self.account.username


class BookingTable(models.Model):
    """
    One account in UserTable can be related to many BookingTable rows, same for InterviewerTable
    """
    user = models.ForeignKey(UserTable, on_delete=models.CASCADE, related_name='time_slots')
    interviewer = models.ForeignKey(InterviewerTable, on_delete=models.CASCADE, related_name='time_slots')
    date_booked_utc = models.TextField(null=True) # PLACEHOLDER TYPE

    def __str__(self):
        return self.user.account.username
    
