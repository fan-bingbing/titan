from django.contrib import admin

# Register your models here.
from first_app.models import FEP, RES, DEMOD, TXSIG, MADOUT, ACP, ACPOUT
from first_app.models import FEPOUT, CSE, CSEOUT, CSHOUT, RXSIG, BLKOUT, ACSOUT, SROUT
admin.site.register(FEP)
admin.site.register(RES)
admin.site.register(DEMOD)
admin.site.register(TXSIG)
admin.site.register(FEPOUT)
admin.site.register(MADOUT)
admin.site.register(ACP)
admin.site.register(ACPOUT)
admin.site.register(CSE)
admin.site.register(CSEOUT)
admin.site.register(CSHOUT)
admin.site.register(RXSIG)
admin.site.register(ACSOUT)
admin.site.register(BLKOUT)
admin.site.register(SROUT)
