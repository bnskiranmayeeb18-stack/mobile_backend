# rides/admin.py
from django.contrib import admin
from .models import Ride

# vere models em unnayo chuddam, dynamic ga register cheddam
from django.apps import apps

# Only Ride register chesi chudu
admin.site.register(Ride)

# Migilavi unte auto ga kanukko
try:
    from .models import DriverProfile
    admin.site.register(DriverProfile)
except:
    pass

try:
    from .models import Booking
    admin.site.register(Booking)
except:
    pass