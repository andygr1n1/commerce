from django.contrib import admin

from .models import *

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'category', 'owner', 'is_active', 'image_url', 'created_at', 'updated_at')
    list_editable = ('title','description', 'is_active', 'image_url', 'category') 
    list_filter = ('owner', 'created_at', 'is_active')  
    search_fields = ('title', 'description') 

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

class BidAdmin(admin.ModelAdmin):
    list_display = ('owner', 'amount', 'listing', 'created_at')
    list_editable = ('amount',)
    list_filter = ('owner', 'created_at')
    search_fields = ('owner__username', 'listing__title')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'listing', 'created_at')
    list_editable = ('content',)
    list_filter = ('user', 'created_at')
    search_fields = ('user__username', 'listing__title')




admin.site.register(User,UserAdmin)

admin.site.register(AuctionListing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Watchlist)
