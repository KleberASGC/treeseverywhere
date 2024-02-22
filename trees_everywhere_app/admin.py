from django.contrib import admin
from .models import Account, PlantedTree, Tree


class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'display_users', 'created', 'active']

    def display_users(self, obj):
        return ', '.join([user.username for user in obj.users.all()])
    display_users.short_description = 'users'
    actions = ['activate_accounts', 'deactivate_accounts']

    def activate_accounts(self, request, queryset):
        queryset.update(active=True)
    activate_accounts.short_description = "Activate selected accounts"

    def deactivate_accounts(self, request, queryset):
        queryset.update(active=False)
    deactivate_accounts.short_description = "Deactivate selected accounts"

class PlantedTreeInline(admin.TabularInline):
    model = PlantedTree
    fields = ('latitude', 'longitude', 'account_name', 'age')
    readonly_fields = ('latitude', 'longitude', 'account_name', 'age')
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def account_name(self, instance):
        return instance.account.name if instance.account else "-"

@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    inlines = [PlantedTreeInline]

admin.site.register(Account, AccountAdmin)
