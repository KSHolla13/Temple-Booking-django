from django.contrib import admin
from .models import *


admin.site.register(user_table)
admin.site.register(sevas_table)
admin.site.register(booking_table)
admin.site.register(transaction_table)
admin.site.register(god_table)
admin.site.register(festival_table)