from django.contrib import admin
from .models import Post, PostStatistic


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'description', 'created_at')
    list_filter = ('author',)
    search_fields = ('title', 'description')
    ordering = ('-created_at',)


class PostStatisticAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'like', 'dislike','created_at')
    list_filter = ('post',)
    search_fields = ('post', )
    ordering = ('-created_at',)


admin.site.register(Post, PostAdmin)
admin.site.register(PostStatistic, PostStatisticAdmin)