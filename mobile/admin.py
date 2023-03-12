from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext

from .models import (
    Category,     Promo,
    Mentor,
    User,
    Course,
    Material,
    Project,
    Order,
)


class UserAdmin(admin.ModelAdmin):
    list_display = ('custom_photoUrl', 'username', 'email', 'name')
    search_fields = ('custom_photoUrl', 'username',)

    def custom_photoUrl(self, obj):
        if obj.photoUrl:
            return mark_safe('<img src="{url}" width={width} />'.format(
                url=obj.photoUrl,
                width='90'
            )
            )

    custom_photoUrl.short_description = gettext('photoUrl')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)


class PromoAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'discount', 'available')
    search_fields = ('id',)
    list_editable = ('available',)


class MentorAdmin(admin.ModelAdmin):
    list_display = ('custom_photoUrl', 'name', )
    list_display_links = ('custom_photoUrl', 'name',)
    search_fields = ('name',)

    def custom_photoUrl(self, obj):
        if obj.photoUrl:
            return mark_safe('<img src="{url}" width={width} />'.format(
                url=obj.photoUrl,
                width='90'
            )
            )

    custom_photoUrl.short_description = gettext('photoUrl')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('custom_photoUrl', 'name',
                    'price', 'available', 'updated_at')
    list_display_links = ('custom_photoUrl', 'name')
    list_editable = ('price', 'available')
    list_filter = ('price', 'available', 'updated_at')
    search_fields = ('name',)

    def custom_photoUrl(self, obj):
        if obj.photoUrl:
            return mark_safe('<img src="{url}" width={width} />'.format(
                url=obj.photoUrl,
                width='90'
            )
            )

    custom_photoUrl.short_description = gettext('photoUrl')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'status',
                    'total', 'updated_at')
    list_display_links = ('user', 'course')
    list_filter = ('user', 'course', 'status')
    search_fields = ('user', 'course',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'title')
    search_fields = ('title',)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'url', 'score')
    search_fields = ('id',)
    list_filter = ('user', 'course', 'updated_at',)


class CertificateAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'created_at')
    search_fields = ('id',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Promo, PromoAdmin)
admin.site.register(Mentor, MentorAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Order, OrderAdmin)
