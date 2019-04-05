from collections import Counter
from django.shortcuts import render_to_response

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    landing_name = request.GET.get('from-landing')
    counter_click[landing_name] += 1

    return render_to_response('index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    landing_name = request.GET.get('from-landing')
    counter_show[landing_name] += 1
    if landing_name == 'original':
        return render_to_response('landing.html')

    return render_to_response('landing_alternate.html')


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать значения test и original
    # Для вывода результат передайте в следующем формате:
    if not counter_show['test']:
        test_message = round(counter_click['test'] / counter_show['test'], 2)
    else:
        test_message = 0

    if counter_show['original']:
        original_message = round(counter_click['original'] / counter_show['original'], 2)
    else:
        original_message = 0

    return render_to_response('stats.html', context={
        'test_conversion': test_message,
        'original_conversion': original_message,
    })
