from django.contrib import admin
from .models import Product, Review, Slider, Category, ProductImage, FAQ
from django.utils.html import mark_safe


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px;">')
        return "—"
    preview.short_description = "Превʼю"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    fields = ('category', 'name', 'slug', 'short_description', 'price',
              'full_description', 'image', 'video', 'created_at')
    readonly_fields = ('created_at',)



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'rating')
    search_fields = ('name', 'message')
    list_filter = ('rating',)


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'order')
    list_editable = ('active', 'order')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question',)
    search_fields = ('question', 'answer')
    