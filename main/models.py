from django.db import models

class LowLevelDesign(models.Model):
    client = models.CharField(max_length=255)

    def __str__(self):
        return f"LLD for {self.client}"
    
    def generateScript(self):
        result = Script(content="")
        for router in self.routers.all():
            result.content += f"router :  {router.name} \n--------------------------\n"
            for phyInterface in router.physicalInterfaces.all():
                result.content += f"#\ninterface {phyInterface.name} \ndescription To_{phyInterface.radioSite.name}\nundo shutdown\n#\n"
                
                for logInterface2G in phyInterface.logicalInterfaces_2g.all():
                    result.content += f"interface {logInterface2G.name} \nvlan-type dot1q {logInterface2G.vlan}\nundo shutdown\ndescription 2G_{phyInterface.radioSite.name}\nip binding vpn-instance vpn_name(2G)\nip address {logInterface2G.ip_address} 255.255.255.252\n#\n"
                
                for logInterface3G in phyInterface.logicalInterfaces_3g.all():
                    result.content += f"interface {logInterface3G.name} \nvlan-type dot1q {logInterface3G.vlan}\nundo shutdown\ndescription 3G_{phyInterface.radioSite.name}\nip binding vpn-instance vpn_name(3G)\nip address {logInterface3G.ip_address} 255.255.255.252\n#\n"
                
                for logInterfaceManagement in phyInterface.logicalInterfaces_management.all():
                    result.content += f"interface {logInterfaceManagement.name} \nvlan-type dot1q {logInterfaceManagement.vlan}\nundo shutdown\ndescription Management_{phyInterface.radioSite.name}\nip binding vpn-instance vpn_name(Management)\nip address {logInterfaceManagement.ip_address} 255.255.255.252\n#\n"
                
                for logInterface4G in phyInterface.logicalInterfaces_4g.all():
                    result.content += f"interface {logInterface4G.name} \nvlan-type dot1q {logInterface4G.vlan}\nundo shutdown\ndescription 4G_{phyInterface.radioSite.name}\nip binding vpn-instance vpn_name(4G)\nip address {logInterface4G.ip_address} 255.255.255.252\n#\n"
        
        result.save()
        return result


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
    radioSite = models.OneToOneField(RadioSite, on_delete=models.CASCADE, null=True, blank=True)

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
        return f"2G Interface: {self.ip_address}"

class Interface3G(LogicalInterface):
    physicalInterface = models.ForeignKey(PhysicalInterface, on_delete=models.CASCADE, related_name='logicalInterfaces_3g')

    def __str__(self):
        return f"3G Interface: {self.ip_address}"

class Interface4G(LogicalInterface):
    physicalInterface = models.ForeignKey(PhysicalInterface, on_delete=models.CASCADE, related_name='logicalInterfaces_4g')

    def __str__(self):
        return f"4G Interface: {self.ip_address}"

class ManagementInterface(LogicalInterface):
    physicalInterface = models.ForeignKey(PhysicalInterface, on_delete=models.CASCADE, related_name='logicalInterfaces_management')

    def __str__(self):
        return f"Management Interface: {self.ip_address}"


class Script(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content
