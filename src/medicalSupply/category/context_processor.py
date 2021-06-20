from .models import Category

def cat_menu(request):
    links = Category.objects.all()
    return dict(links=links)