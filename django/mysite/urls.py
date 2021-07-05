from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include("apps.login.urls")),
    path('', include("apps.home.urls")),
    path('', include("apps.clientes.urls")),
    path('', include("apps.articulos.urls")),
    path('', include("apps.proveedores.urls")),
    path('', include("apps.empresas.urls")),
    path('', include("apps.ventas.urls")),
    path('', include("apps.facturas.urls")),
    path('', include("apps.inventario.urls")),
    path('', include("apps.compras.urls")),
    path('', include("apps.informes.urls")),

    path('', include("apps.requision.urls")),
    path('', include("apps.orden_de_compra.urls")),
    path('', include("apps.registro_material.urls")),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()

#https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)