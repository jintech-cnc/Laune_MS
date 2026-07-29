from django.contrib import admin
from .models import ChatSession, ChatMessage


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ['sender', 'content', 'sent_at', 'is_read']
    can_delete = False


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['visitor_name', 'visitor_email', 'started_at', 'last_activity', 'is_closed', 'message_count']
    list_filter = ['is_closed', 'started_at']
    search_fields = ['visitor_name', 'visitor_email']
    readonly_fields = ['session_id', 'started_at', 'last_activity']
    inlines = [ChatMessageInline]

    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'sender', 'content_preview', 'sent_at', 'is_read']
    list_filter = ['sender', 'is_read', 'sent_at']
    readonly_fields = ['session', 'sender', 'content', 'sent_at']
    search_fields = ['content', 'session__visitor_name']

    def content_preview(self, obj):
        return obj.content[:60] + '...' if len(obj.content) > 60 else obj.content
    content_preview.short_description = 'Message'
