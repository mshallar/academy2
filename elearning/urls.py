from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from app.views import create_checkout_session, webhook

urlpatterns = [
    #path('', include('app.urls')),
    path('admin/', admin.site.urls),
    path('create-checkout-session/', create_checkout_session, name='checkout'),
    path('webhooks/stripe/', webhook,name="webhook"),
]

urlpatterns += i18n_patterns(
    path('', include('app.urls')),
    path('accounts/', include('accounts.urls')),
)

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)