from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Product, Category

class ProductListView(generic.ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    paginate_by = 3

product_list = ProductListView.as_view()

class CategoryListView(generic.ListView):
    template_name = 'catalog/category.html'
    context_object_name = 'products'

    #Modifica a queryset padrão para gerar a lista
    def get_queryset(self):
        #kwargs são os parametros nomeados da request
        return Product.objects.filter(category__slug=self.kwargs['slug'])

    # Para colocar dados adicionais no context
    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['current_category'] = get_object_or_404(Category, slug=self.kwargs['slug'])
        return context

category = CategoryListView.as_view()

def product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        'product': product
    }
    return render(request, 'catalog/product.html', context)
