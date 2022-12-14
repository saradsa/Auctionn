from django.contrib import admin
from .models import User, Category, Listing, Bid, Comment
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['username']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'detail',
                    'price', 'isActive', 'category', 'owner']


class BidAdmin(admin.ModelAdmin):
    list_display = ['listing', 'bidder', 'new_bid', 'created_at']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['listing', 'commenter', 'comment', 'created_at']


admin.site.register(User)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
