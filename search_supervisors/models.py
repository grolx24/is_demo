from django.db import models


class EmployeeDepartmentSelection(models.Model):
    employee = models.CharField(max_length=255, null=False, blank=False)
    department = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f'Employee: {self.employee}, Department: {self.department}'
