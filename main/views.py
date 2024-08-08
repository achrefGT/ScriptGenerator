from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import Router, PhysicalInterface, Interface2G, Interface3G, Interface4G, ManagementInterface, Script, LowLevelDesign,RadioSite
from .forms import (
    LowLevelDesignForm,
    RouterForm,
    RadioSiteForm,
    PhysicalInterfaceFormSet,
    Interface2GFormSet,
    Interface3GFormSet,
    Interface4GFormSet,
    ManagementInterfaceFormSet,
)

def index(request):
    return render(request, "main/base.html")



def create_radioSite(request):
    if request.method == "POST" :
        radio_site_form = RadioSiteForm(request.POST)
        if radio_site_form.is_valid():
            # Save the RadioSite instance
            radio_site = radio_site_form.save(commit=False)
            radio_site.save()
        return redirect('index')
    else :
        radio_site_form = RadioSiteForm()
    return render(request, "main/create_radioSite.html", {
        'radio_site_form': radio_site_form
        })

def create_LLD(request):
    if request.method == "POST" :
        low_level_design_form = LowLevelDesignForm(request.POST)
        if low_level_design_form.is_valid():
            low_level_design = low_level_design_form.save(commit=False)
            low_level_design.save()
        return redirect('index')
    else :
        low_level_design_form = LowLevelDesignForm()
    return render(request, "main/create_LLD.html", {
        'low_level_design_form': low_level_design_form
        })


def create_router(request):
    if request.method == 'POST':
        # Instantiate all forms with POST data
        router_form = RouterForm(request.POST)
        physical_interface_formset = PhysicalInterfaceFormSet(request.POST)
        interface2g_formset = Interface2GFormSet(request.POST)
        interface3g_formset = Interface3GFormSet(request.POST)
        interface4g_formset = Interface4GFormSet(request.POST)
        management_interface_formset = ManagementInterfaceFormSet(request.POST)

        # Validate all forms and formsets
        if (router_form.is_valid() and
            physical_interface_formset.is_valid() and
            interface2g_formset.is_valid() and
            interface3g_formset.is_valid() and
            interface4g_formset.is_valid() and
            management_interface_formset.is_valid()):

            # Save the Router instance
            router = router_form.save()

            # Save physical interfaces and associate them with the router
            physical_interfaces = physical_interface_formset.save(commit=False)
            for physical_interface in physical_interfaces:
                physical_interface.router = router
                physical_interface.save()

                # Save logical interfaces associated with the physical interface
                for formset in [interface2g_formset, interface3g_formset, interface4g_formset, management_interface_formset]:
                    logical_interfaces = formset.save(commit=False)
                    for logical_interface in logical_interfaces:
                        logical_interface.physicalInterface = physical_interface
                        logical_interface.save()

            # Generate the script after saving all the data
            lld = router.lld  # Assuming the Router has a ForeignKey to LowLevelDesign
            script = lld.generateScript()

            # Pass the script content to the result template
            return render(request, 'main/result.html', {'script_content': script.content})

    else:
        # Instantiate all forms with empty data
        router_form = RouterForm()
        physical_interface_formset = PhysicalInterfaceFormSet(queryset=PhysicalInterface.objects.none())
        interface2g_formset = Interface2GFormSet(queryset=Interface2G.objects.none())
        interface3g_formset = Interface3GFormSet(queryset=Interface3G.objects.none())
        interface4g_formset = Interface4GFormSet(queryset=Interface4G.objects.none())
        management_interface_formset = ManagementInterfaceFormSet(queryset=ManagementInterface.objects.none())

    return render(request, "main/create_router.html", {
        'router_form': router_form,
        'physical_interface_formset': physical_interface_formset,
        'interface2g_formset': interface2g_formset,
        'interface3g_formset': interface3g_formset,
        'interface4g_formset': interface4g_formset,
        'management_interface_formset': management_interface_formset,
    })