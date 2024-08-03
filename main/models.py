from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class LowLevelDesign(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f"LLD {self.lld_id} for {self.client}"

class Router(models.Model):
    name = models.CharField(max_length=255)
    lld = models.ForeignKey(LowLevelDesign, on_delete=models.CASCADE, related_name='routers')

    def __str__(self):
        return self.name

class RadioSite(models.Model):
    name = models.CharField(max_length=255)
    lld = models.ForeignKey(LowLevelDesign, on_delete=models.CASCADE, related_name='radio_sites')

    def __str__(self):
        return self.name

class PhysicalInterface(models.Model):
    rate = models.CharField(max_length=100) 
    name = models.CharField(max_length=255)
    router = models.ForeignKey(Router, on_delete=models.CASCADE, related_name='physicalInterfaces')

    def __str__(self):
        return self.name

class LogicalInterface(models.Model):
    ip_address = models.GenericIPAddressField()
    vlan = models.IntegerField()
    connectedTo = models.GenericIPAddressField(null=True, blank=True)
    name = models.CharField(max_length=255)
    physicalInterface = models.ForeignKey(PhysicalInterface, on_delete=models.CASCADE)

    class Meta:
        abstract = True  

class Interface2G(LogicalInterface):
    physicalInterface = models.ForeignKey(PhysicalInterface, on_delete=models.CASCADE, related_name='logicalInterfaces_2g')

    def __str__(self):
        return f"2G Interface: {self.logicalInterface_id}"

class Interface3G(LogicalInterface):
    physicalInterface = models.ForeignKey(PhysicalInterface, on_delete=models.CASCADE, related_name='logicalInterfaces_3g')

    def __str__(self):
        return f"3G Interface: {self.logicalInterface_id}"

class Interface4G(LogicalInterface):
    physicalInterface = models.ForeignKey(PhysicalInterface, on_delete=models.CASCADE, related_name='logicalInterfaces_4g')

    def __str__(self):
        return f"4G Interface: {self.logicalInterface_id}"

class ManagementInterface(LogicalInterface):
    physicalInterface = models.ForeignKey(PhysicalInterface, on_delete=models.CASCADE, related_name='logicalInterfaces_management')

    def __str__(self):
        return f"Management Interface: {self.logicalInterface_id}"

class Script(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content
