from django.contrib import admin
from .models import Course, CoursePart

def some_admin_action(modeladmin, request, queryset):
    print(queryset)

class CoursePartInline(admin.TabularInline):
    model = CoursePart
    extra =  1


class CourseAdmin(admin.ModelAdmin):
    inlines = (CoursePartInline, )
    actions = [some_admin_action, ]
    #fields = ('title', 'description', 'deleted_at')

    list_display = ('id', 'title', 'description', 'part_count')
#
#    def part_count(self, obj):
#        return obj.parts.count()

    #part_count.short_description = 'Amount of Course Parts'

    list_filter = ('title', 'created_at')

    search_fields = ('title', 'description')

    list_editable = ('title', )

    fieldsets = (
        ('Major fields', {'fields': ('description', 'title')}),
        ('Minor fields', {'fields': ('deleted_at', 'created_by')})
    )




admin.site.register(Course, CourseAdmin)
