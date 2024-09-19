from django.contrib import admin

from .models import *

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'image_url', 'created_at', 'updated_at', 'owner', 'is_active')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    
    def listings_count(self, obj):
        return obj.listings.count()
    listings_count.short_description = 'Listings Count'
    
    list_display = ('name', 'description', 'listings_count')

class UserAdmin(admin.ModelAdmin):
    
    def watchlist_count(self, obj):
        return obj.watchlist.count()
    watchlist_count.short_description = 'Watchlist Count'

    list_display = ('username', 'email', 'first_name', 'last_name', 'watchlist_count')




admin.site.register(User,UserAdmin)

admin.site.register(AuctionListing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Watchlist)
