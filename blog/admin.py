from django.contrib import admin
from .models import Post, Category, Tag, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'published', 'category')
    list_filter = ('status', 'created', 'category', 'tags')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}  # پر کردن خودکار اسلاگ از عنوان
    raw_id_fields = ('author',)
    date_hierarchy = 'published'
    ordering = ('-published',)
    filter_horizontal = ('tags',)  # برای انتخاب چندتایی تگ‌ها


# admin.p

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')  # در صفحه لیست ادمین این فیلدها نمایش داده میشن
    prepopulated_fields = {'slug': ('name',)}  # هنگام نوشتن عنوان، اسلاگ خودش ساخته میشه


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')  # فیلدهایی که توی لیست نشون داده میشن
    prepopulated_fields = {'slug': ('name',)}  # موقع وارد کردن عنوان، اسلاگ اتوماتیک ساخته میشه
