# DJANGO
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.urls import reverse
from apps.core.views import robots
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# handler404 = 'apps.core.views.handler404'
# handler500 = 'apps.core.views.handler500'


urlpatterns = [
    path('admin',     admin.site.urls),
 	path('',          include('apps.shop.urls',     namespace='shop')),
    path('',          include('apps.core.urls',     namespace='core')),
    path('',          include('apps.user.urls',     namespace='user')),
    path('cart/',     include('apps.cart.urls',     namespace='cart')),
    path('order/',    include('apps.order.urls',    namespace='order')),
    path('search/',   include('apps.search.urls',   namespace='search')),
    path('commetns/', include('apps.comments.urls', namespace='comments')),
   
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain'), name='robots'),
    path('sitemap.xml', TemplateView.as_view(template_name="sitemap.xml", content_type='application/xml'), name='sitemap'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += staticfiles_urlpatterns()