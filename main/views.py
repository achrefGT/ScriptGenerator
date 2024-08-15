from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import Router, PhysicalInterface, Interface2G, Interface3G, Interface4G, ManagementInterface, Script, LowLevelDesign, LowLevelDesign_Co_trans,RadioSite
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
import pandas as pd

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


def upload_file(request):
    if request.method == 'POST':
        form = LowLevelDesignForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('file_upload_success')
    else:
        form = LowLevelDesignForm()
    return render(request, 'main/uploadLLD.html', {'form': form})


def success_view(request):
    return render(request, 'main/success.html')


@require_POST
def download_script(request):
    script_content = request.POST.get('script_content', '')  
    
    response = HttpResponse(script_content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="script.txt"'

    return response


def get_column_value(row, column_name, column_index, sheet_name):
    """
    Try to get the value by column name; if it fails, use the column index.
    If both fail, raise an error with details about the column and sheet.
    """
    try:
        return row[column_name]
    except KeyError:
        result = row[column_index]
        if not pd.isna(result):  
            return result
    
        raise ValueError(f"Failed to find the column '{column_name}' in sheet '{sheet_name}'.")



IP_PLAN_COLUMNS = {
    'Router': 0,
    'radio_site_name': 1,
    'Interface': 8,
}

INTERFACE_2G_COLUMNS = {
    'NE40': 0,
    'Site Name': 1,
    'NE40 Interface': 2,
    'Radio_Site address': 3,
    'NE40 GW': 4,
    'VLAN': 5,
    
}

INTERFACE_3G_COLUMNS = {
    'NE40 Interface': 2,
    'NE40': 0,
    '3G UP&CP GW IP': 5,
    'UP&CP VLAN': 7,
    '3G UP&CP IP': 4,
    'Management IP': 10,
    'Management VLAN': 12,
    'OMCH IP': 8,
}

INTERFACE_4G_COLUMNS = {
    'NE40 Interface': 2,
    'NE40': 0,
    '4G UP&CP GW IP': 4,
    'VLAN': 5,
    '4G UP&CP IP': 3,
}

LLD_CO_TRANS_COLUMNS = {
    'NE40/NE8000': 0,
    'site ': 1,
    'Config O&M': 2,
    'Config TDD': 3,
}

def upload_lld(request):
    if request.method == 'POST':
        form = LowLevelDesignForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                excel_file = request.FILES['file']
                xls = pd.ExcelFile(excel_file)

                # Try to read sheets by name, fall back to sheet numbers if needed
                try:
                    ip_plan_df = pd.read_excel(xls, 'IP PLAN')
                except ValueError:
                    ip_plan_df = pd.read_excel(xls, sheet_name=0)  # Fallback to the first sheet

                try:
                    interface_2g_df = pd.read_excel(xls, '2G')
                except ValueError:
                    interface_2g_df = pd.read_excel(xls, sheet_name=1)  # Fallback to the second sheet

                try:
                    interface_3g_df = pd.read_excel(xls, '3G')
                except ValueError:
                    interface_3g_df = pd.read_excel(xls, sheet_name=2)  # Fallback to the third sheet

                try:
                    interface_4g_df = pd.read_excel(xls, '4G')
                except ValueError:
                    interface_4g_df = pd.read_excel(xls, sheet_name=3)  # Fallback to the fourth sheet

                # Create LowLevelDesign instance (assuming one LLD per file)
                lld = LowLevelDesign.objects.create(file=excel_file)  

                # Process IP Plan sheet
                for _, row in ip_plan_df.iloc[1:].iterrows():
                    router_name = get_column_value(row, 'Router', IP_PLAN_COLUMNS['Router'], 'IP PLAN')
                    radio_site_name = get_column_value(row, 'radio_site_name', IP_PLAN_COLUMNS['radio_site_name'], 'IP PLAN')
                    
                    if router_name and radio_site_name:
                        router, created = Router.objects.get_or_create(name=router_name, lld=lld)
                        radio_site, created = RadioSite.objects.get_or_create(name=radio_site_name, lld=lld)

                        PhysicalInterface.objects.create(
                            name=get_column_value(row, 'Interface', IP_PLAN_COLUMNS['Interface'], 'IP PLAN'), 
                            router=router, 
                            radioSite=radio_site
                        )

                # Process 2G interfaces
                for _, row in interface_2g_df.iterrows():
                    physical_iface_name = get_column_value(row, 'NE40 Interface', INTERFACE_2G_COLUMNS['NE40 Interface'], '2G')
                    router_name = get_column_value(row, 'NE40', INTERFACE_2G_COLUMNS['NE40'], '2G')
                    router = Router.objects.get(name=router_name, lld=lld)
                    phy_iface = PhysicalInterface.objects.get(name=physical_iface_name, router=router)

                    Interface2G.objects.create(
                        ip_address=get_column_value(row, 'NE40 GW', INTERFACE_2G_COLUMNS['NE40 GW'], '2G'), 
                        vlan=get_column_value(row, 'VLAN', INTERFACE_2G_COLUMNS['VLAN'], '2G'), 
                        connectedTo=get_column_value(row, 'Radio_Site address', INTERFACE_2G_COLUMNS['Radio_Site address'], '2G'), 
                        physicalInterface=phy_iface,
                    )

                # Process 3G interfaces
                for _, row in interface_3g_df.iterrows():
                    physical_iface_name = get_column_value(row, 'NE40 Interface', INTERFACE_3G_COLUMNS['NE40 Interface'], '3G')
                    router_name = get_column_value(row, 'NE40', INTERFACE_3G_COLUMNS['NE40'], '3G')
                    router = Router.objects.get(name=router_name, lld=lld)
                    phy_iface = PhysicalInterface.objects.get(name=physical_iface_name, router=router)

                    Interface3G.objects.create(
                        ip_address=get_column_value(row, '3G UP&CP GW IP', INTERFACE_3G_COLUMNS['3G UP&CP GW IP'], '3G'), 
                        vlan=get_column_value(row, 'UP&CP VLAN', INTERFACE_3G_COLUMNS['UP&CP VLAN'], '3G'), 
                        connectedTo=get_column_value(row, '3G UP&CP IP', INTERFACE_3G_COLUMNS['3G UP&CP IP'], '3G'), 
                        physicalInterface=phy_iface,
                    )

                    ManagementInterface.objects.create(
                        ip_address=get_column_value(row, 'Management IP', INTERFACE_3G_COLUMNS['Management IP'], '3G'), 
                        vlan=get_column_value(row, 'Management VLAN', INTERFACE_3G_COLUMNS['Management VLAN'], '3G'), 
                        connectedTo=get_column_value(row, 'OMCH IP', INTERFACE_3G_COLUMNS['OMCH IP'], '3G'), 
                        physicalInterface=phy_iface,
                    )

                # Process 4G interfaces
                for _, row in interface_4g_df.iterrows():
                    physical_iface_name = get_column_value(row, 'NE40 Interface', INTERFACE_4G_COLUMNS['NE40 Interface'], '4G')
                    router_name = get_column_value(row, 'NE40', INTERFACE_4G_COLUMNS['NE40'], '4G')
                    router = Router.objects.get(name=router_name, lld=lld)
                    phy_iface = PhysicalInterface.objects.get(name=physical_iface_name, router=router)

                    Interface4G.objects.create(
                        ip_address=get_column_value(row, '4G UP&CP GW IP', INTERFACE_4G_COLUMNS['4G UP&CP GW IP'], '4G'), 
                        vlan=get_column_value(row, 'VLAN', INTERFACE_4G_COLUMNS['VLAN'], '4G'), 
                        connectedTo=get_column_value(row, '4G UP&CP IP', INTERFACE_4G_COLUMNS['4G UP&CP IP'], '4G'), 
                        physicalInterface=phy_iface,
                    )
                
                # Generate the script
                script = lld.generateScript()
                return render(request, 'main/result.html', {'script_content': script.content})

            except Exception as e:
                # Handle any errors that occur
                error_message = f"An error occurred while processing the file: {str(e)}"
                return render(request, 'main/uploadLLD.html', {'form': form, 'error': error_message})


    else:
        form = LowLevelDesignForm()

    return render(request, 'main/uploadLLD.html', {'form': form})



def upload_lld_Co_Trans(request):
    if request.method == 'POST':
        form = LowLevelDesignForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                excel_file = request.FILES['file']
                lld_data_df = pd.read_excel(excel_file, sheet_name=0)  
                print(lld_data_df)
                # Create LowLevelDesign instance
                lld = LowLevelDesign_Co_trans.objects.create(file=excel_file)  


                # Process the first row of the DataFrame (assuming it contains the data)
                for _, row in lld_data_df[1:].iterrows():
                    router_name = row[0]
                    site_name = row[1]
                    o_and_m_ip = row[2]  
                    tdd_ip = row[3] 

                    print(f" ******************************** {router_name} / {site_name} :{o_and_m_ip} + {tdd_ip}")


                    if router_name and site_name:
                        router, created = Router.objects.get_or_create(name=router_name, lld=lld)
                        radio_site, created = RadioSite.objects.get_or_create(name=site_name, lld=lld)
                        lld.o_and_m = o_and_m_ip
                        lld.TDD = tdd_ip
                        lld.save()

                # Generate the script
                script = lld.generateScript(site_name)
                return render(request, 'main/result.html', {'script_content': script.content})

            except Exception as e:
                error_message = f"An error occurred while processing the file: {str(e)}"
                return render(request, 'main/uploadLLD.html', {'form': form, 'error': error_message})

    else:
        form = LowLevelDesignForm()

    return render(request, 'main/uploadLLD.html', {'form': form})
