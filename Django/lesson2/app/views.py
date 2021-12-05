from django.shortcuts import render, reverse

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'sandwich': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
}


def home_view(request):
        pages = {
            'Омлет': 'recipe/omlet',
            'Сэндвич': 'recipe/sandwich',
            'Паста': 'recipe/pasta',
        }
        context = {
            'pages': pages
        }
        return render(request, 'home.html', context)


def show_recipe(request, dish):
    recipe = DATA.get(dish).items()
    recipe_list = []
    servings = request.GET.get('servings', 1)
    for item in recipe:
        recipe_list.append(f'{item[0]}: {item[1]*int(servings)}')
    context = {
        'recipe' : recipe_list,
    }
    return render(request, 'recipe.html', context)

# def time_view(request):
#     # обратите внимание – здесь HTML шаблона нет,
#     # возвращается просто текст
#     current_time = datetime.datetime.now()
#     msg = f'Текущее время: {current_time}'
#     return HttpResponse(msg)
