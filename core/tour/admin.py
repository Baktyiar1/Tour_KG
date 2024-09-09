from django.contrib import admin

from .models import (
    Region, Category, Tour, Image, Booking, Payment, RatingStar,
    Rating, Reviews, Wishlist, TourView, Banner, Date_tour, TourAuthorRequest
)

admin.site.register(Region)
admin.site.register(Category)
admin.site.register(Tour)
admin.site.register(Image)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(RatingStar)
admin.site.register(Rating)
admin.site.register(Reviews)
admin.site.register(Wishlist)
admin.site.register(TourView)
admin.site.register(Banner)
admin.site.register(Date_tour)
admin.site.register(TourAuthorRequest)
