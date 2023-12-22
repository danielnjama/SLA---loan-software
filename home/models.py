from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib import messages



class Userinfo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    phone = PhoneNumberField()
    profile_pic = models.ImageField(upload_to='photos',blank=True)
    id_number = models.IntegerField(verbose_name="ID Number")

    def __str__(self):
        return self.user.username


class Contribution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    date_contributed = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"


loan_status = (
    ('Active','Active'),
    ('Cleared','Cleared')
)
class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    remaining_amount = models.FloatField()
    date_taken = models.DateField(auto_now_add=True)
    interest_rate = models.FloatField(default=0.1)
    loan_status = models.CharField(choices=loan_status,max_length=20, default="Active")
    
    def __str__(self):
        return f"{self.user.username} - {self.amount}"
    
    def save(self,*args, **kwargs):
        self.remaining_amount = (self.amount * self.interest_rate) + self.amount
        super(Loan, self).save(*args, **kwargs)
        


class RepaymentRecord(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount_paid = models.FloatField()
    date_paid = models.DateField(auto_now_add=True)
    loan_balance = models.FloatField()

    
    def save(self, *args, **kwargs):
        total_amount_paid = RepaymentRecord.objects.filter(loan=self.loan).aggregate(models.Sum('amount_paid'))['amount_paid__sum'] or 0
        self.loan_balance = self.loan.remaining_amount - total_amount_paid - self.amount_paid
        # Update the remaining amount in the loan when a payment is made
        self.loan.remaining_amount -= self.amount_paid
        if self.loan.loan_status == "Cleared":
            return
        if self.loan_balance <= 0:
            self.loan.loan_status = "Cleared"
            self.loan.save()

        
        super(RepaymentRecord, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.loan.user.username} - {self.amount_paid}"
