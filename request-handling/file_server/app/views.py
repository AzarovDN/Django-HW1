import datetime, time

from django.shortcuts import render
from django.views.generic import TemplateView
from os import listdir, stat


class FileList(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, date=None):

        file_list = listdir('./files')
        result_list = []

        if date:
            year, month, day, *_ = time.strptime(date, "%Y-%m-%d")
            date = datetime.date(year, month, day)

        for file in file_list:
            stat_info = stat(f'./files/{file}')
            file_dict = {'name': file,
                         'mtime': datetime.datetime.fromtimestamp(stat_info.st_ctime),
                         'ctime': datetime.datetime.fromtimestamp(stat_info.st_mtime)
                         }
            if date:
                if date == file_dict['mtime'].date() or date == file_dict['ctime'].date():
                    result_list.append(file_dict)
            else:
                result_list.append(file_dict)

        return {
            'files': result_list,
            'date': date
        }


def file_content(request, name):
    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    file_list = listdir('./files')
    if name in file_list:
        with open(f'./files/{name}') as f:
            file = f.read()

            return render(
                request,
                'file_content.html',
                context={'file_name': name, 'file_content': file}
            )
    return render(
        request,
        'file_content.html',
        context={'file_name': f'Файл {name} не найден', 'file_content': ''}
    )