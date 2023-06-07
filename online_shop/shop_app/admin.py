from django.contrib import admin
from .models import *
from django.db.models.query import QuerySet
from abc import abstractmethod

    
admin.site.site_header = "Админ-панель сайта 'Шестерочка'"

class CategoryListFilter(admin.SimpleListFilter):

    title = 'Категория'
    parameter_name = 'category'
    supercategories = Categories.objects.filter(supercategory=None) 

    def lookups(self, *_):
        return [(cat.id, cat.name) for cat in self.supercategories]

    @abstractmethod
    def queryset(self, _, queryset) -> QuerySet:
        pass
    
class ProductCategoryListFilter(CategoryListFilter):
    def queryset(self, _, queryset) -> QuerySet:
        if self.value():
            return queryset.filter(category__id=self.value())
        return queryset.all()

class CatCategoryListFilter(CategoryListFilter):
    def queryset(self, _, queryset) -> QuerySet:
        if self.value():
            return queryset.filter(id=self.value())
        return queryset.all()
    



class OrderProductInline(admin.StackedInline):
    model = OrdersToProducts
    extra = 1
    verbose_name_plural = 'Продукты'

class UserToAddressInline(admin.StackedInline):
    model = UserToAddress
    extra = 1
    verbose_name_plural = 'Продукты'


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ("first_name", "last_name", "surname", "email", "date_joined")
    list_display = ('first_name', 'surname', 'last_name', 'display_addresses', 'is_superuser')
    search_fields = ('last_name',)
    exclude = ['password', 'username', 'last_login']
    empty_value_display = ''

    def has_add_permission(self, _):
        return False

@admin.action(description="Mark selected products as removed")
def make_removed(modeladmin, request, queryset):
    queryset.update(status="removed")

@admin.action(description="Mark selected products as for fale")
def make_for_sale(modeladmin, request, queryset):
    queryset.update(status="for fale")

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('name', 'category__name') 
    list_display = ('name', 'category', 'weight', 'number', 'price', 'status', 'image')
    list_filter = ('status', ProductCategoryListFilter)
    actions = [make_removed, make_for_sale]


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment', 'product']
    list_filter = ['product']
    readonly_fields = ['user']

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_add_permission(self, request):
        return request.user.is_superuser

    def save_model(self, request, obj, form, change):
        obj.user = Users.objects.get(id=request.user.id)
        obj.save()
    

@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]
    readonly_fields = ['status','user']
    search_fields = ('date',)
    list_display = ('user', 'date', 'status')

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, _, obj=None):
        return False 
    
    def has_change_permission(self, _, obj=None):
        if obj:
            return obj.status == 'created' or obj.status == 'in_basket'
        return True


@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'supercategory')
    list_filter = (CatCategoryListFilter,)

    def save_model(self, request, obj, form, change) -> None:
        raise ValidationError('lflf')

@admin.register(Discounts)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('date_of_creation', 'finished', 'product', 'percentage')


@admin.register(UserAddresses)
class AddressAdmin(admin.ModelAdmin):
    inlines = [UserToAddressInline]

