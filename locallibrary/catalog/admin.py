from django.contrib import admin

from catalog.models import Genre, Author, Book, BookInstance, Language

# Register your models here.


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

class AuthorAdmin(admin.ModelAdmin):
	list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
	fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

	inlines = [BooksInstanceInline]
	


class BookAdmin(admin.ModelAdmin):
	list_display=('title', 'author', 'display_genre')
	inlines = [BooksInstanceInline]


class BookInstanceAdmin(admin.ModelAdmin):
	list_display =('book', 'status', 'due_back' , 'id')

	list_filter = ('status', 'due_back')

	fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )


admin.site.register(Genre)
# commented due to ModelAdmin
# admin.site.register(Author)

admin.site.register(Author, AuthorAdmin)
# admin.site.register(Book)
admin.site.register(Book, BookAdmin)
# admin.site.register(BookInstance)

admin.site.register(BookInstance, BookInstanceAdmin)


admin.site.register(Language)


# @admin.register(BookInstance)

