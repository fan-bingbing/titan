from django.contrib import admin

# Register your models here.
from first_app.models import FEP, RES, DEMOD, TXSIG, MADOUT, ACP, ACPOUT

admin.site.register(FEP)
admin.site.register(RES)
admin.site.register(DEMOD)
admin.site.register(TXSIG)
admin.site.register(MADOUT)
admin.site.register(ACP)
admin.site.register(ACPOUT)
