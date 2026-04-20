from django.contrib import admin
from django.utils.html import format_html
from .models import Quote, EmailSettings


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'project_type', 'source', 'is_read', 'created_at')
    list_filter = ('project_type', 'source', 'is_read', 'created_at')
    search_fields = ('name', 'phone', 'email', 'message')
    readonly_fields = ('created_at',)
    list_editable = ('is_read',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    fieldsets = (
        ('Customer Info', {
            'fields': ('name', 'phone', 'email')
        }),
        ('Inquiry Details', {
            'fields': ('project_type', 'source', 'message', 'is_read')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs

    actions = ['mark_as_read', 'mark_as_unread']

    @admin.action(description="Mark selected as Read")
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description="Mark selected as Unread")
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)


@admin.register(EmailSettings)
class EmailSettingsAdmin(admin.ModelAdmin):
    """
    Singleton settings panel for the owner's email notification preferences.
    Accessible at Admin → Email Settings.
    """

    def has_add_permission(self, request):
        # Only allow one instance
        return not EmailSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    fieldsets = (
        ('Notification Destination', {
            'description': 'Set the email address where new inquiries will be sent.',
            'fields': ('owner_email', 'send_email_on_inquiry'),
        }),
        ('Email Customization', {
            'fields': ('email_subject_prefix',),
        }),
    )