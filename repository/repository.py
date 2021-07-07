from category.models import Category


def category_context():
    context = {
        'category': Category.objects.active()
    }
    return context
