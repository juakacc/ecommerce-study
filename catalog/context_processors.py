from .models import Category

def categories(context):
    return {
        'categories': Category.objects.all()
    }
