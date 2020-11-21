from django.urls import include, path, re_path
from django.views.generic import TemplateView
from apps.shop import views


app_name = 'shop'

pages = [
    path('about',        TemplateView.as_view(template_name='shop/shop__about.html'),         name='about'),
    path('delivery',     TemplateView.as_view(template_name='shop/shop__delivery.html'),      name='delivery'),
    path('contacts',     TemplateView.as_view(template_name='shop/shop__contacts.html'),      name='contacts'),
    path('guarantee',    TemplateView.as_view(template_name='shop/shop__guarantee.html'),     name='guarantee'),
    path('public_offer', TemplateView.as_view(template_name='shop/shop__publicofer.html'),    name="public_offer"),
    path('politics',     TemplateView.as_view(template_name="shop/product_lp/politics.html"), name="politics"),
]


urlpatterns = [
    path('', views.home, name='home'),
    re_path(
        r'''^catalogue/(?P<category>[-\w/]*)/'''
        r'''product-(?P<slug>[\w-]+)-id-(?P<product_id>[0-9]+)'''
        r'''(?:-(?P<variant_id>[0-9]+))?/'''
        r'''?(?:\/(?P<page>characteristics|comments|questions|review|photo|))?/?$''',
        views.ProductPage.as_view({'get':'page'}), 
        name="product"
    ),
    # re_path(
    #     r'''^product
    #     r'''(?P<slug>[\w-]+)-id-(?P<product_id>[0-9]+)'''
    #     r'''(?:-(?P<variant_id>[0-9]+))?/'''
    #     r'''?(?:\/(?P<page>characteristics|comments|questions|review|photo|))?/?$''',
    #     views.ProductPage.as_view({'get':'page'}), 
    #     name="product"
    # ),
    re_path(
        r'''^catalogue/(?P<category>[-\w/]*)/'''
        r'''product-(?P<slug>[\w-]+)-id-(?P<product_id>[0-9]+)/'''
        r'''(?:-(?P<variant_id>[0-9]+))?/'''
        r'''comments/form/$''',
        views.ProductPage.as_view({'get':'comment_form', 'post':'comment_form'}), 
        name="comment_form"
    ),
    re_path(
        r'''^catalogue/(?P<category>[-\w/]*)/'''
        r'''product-(?P<slug>[\w-]+)-id-(?P<product_id>[0-9]+)/'''
        r'''(?:-(?P<variant_id>[0-9]+))?/'''
        r'''question/form/$''',
        views.ProductPage.as_view({'get':'question_form', 'post':'question_form'}), 
        name="question_form"
    ),

    

    re_path('catalogue/(?P<category>[-\w/]*)/$', views.catalogue, name="catalogue"),
    re_path('catalogue/', views.catalogue, name="catalogue"),
    path('watchlist', views.watchlist, name="watchlist"),
    path('set_watchlist/<int:product_id>/<int:variant_id>/', views.set_watchlist, name="set_watchlist"),
    path('set_watchlist/<int:product_id>/', views.set_watchlist, name="set_watchlist"),
    path('facebook_feed', views.facebook_feed, name="facebook_feed"),
    path('', include(pages)),
]
