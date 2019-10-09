from django.contrib import admin

# Register your models here.
from first_app.models import FEP, RES, DEMOD, TXSIG, MADOUT, ACP, ACPOUT, CSE, CSEOUT, CSHOUT

admin.site.register(FEP)
admin.site.register(RES)
admin.site.register(DEMOD)
admin.site.register(TXSIG)
admin.site.register(MADOUT)
admin.site.register(ACP)
admin.site.register(ACPOUT)
admin.site.register(CSE)
admin.site.register(CSEOUT)
admin.site.register(CSHOUT)
