from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

from .resource import ConversationResource, MessageResource
from .models import Conversation, Message, Setting


@admin.register(Conversation)
class ConversationAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'topic', 'created_at')
    resource_class = ConversationResource


@admin.register(Message)
class MessageAdmin(ImportExportModelAdmin):
    list_display = ('id', 'get_conversation_topic', 'message', 'is_bot', 'is_hidden_from_user', 'tokens', 'created_at')
    resource_class = MessageResource

    def get_conversation_topic(self, obj):
        return obj.conversation.topic

    get_conversation_topic.short_description = 'Conversation Topic'


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')