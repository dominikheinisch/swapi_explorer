from ast import literal_eval
from datetime import datetime

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView

from .models import File
from .logic.etl_controller import ETLController


class IndexView(ListView):
    model = File
    context_object_name = 'file_list'
    queryset = File.objects.order_by('-creation_date')
    template_name = 'explorer_app/index.html'

    def post(self, request: HttpRequest) -> HttpResponse:
        if 'fetch' in request.POST:
            filename = ETLController.create_empty()
            File.objects.create(name=filename, creation_date=datetime.now())
            ETLController.fetch(filename)
        return redirect('explorer_app:index')


class FileView(View):
    template_name = 'explorer_app/file.html'

    def get(self, request: HttpRequest, filename: str) -> HttpResponse:
        return self._handle_request(request, filename, counter=11)

    def post(self, request: HttpRequest, filename: str) -> HttpResponse:
        counter = request.POST.get('load_more')
        if counter is not None:
            return self._handle_request(request, filename, counter=int(counter) + 10)

    def _handle_request(self, request: HttpRequest, filename: str, counter: int) -> HttpResponse:
        people_table = ETLController.load(filename)
        context = {
            'counter': counter,
            'filename': filename,
            'table_head': people_table[0],
            'table_body': people_table[1:counter],
        }
        return render(request, self.template_name, context=context)


class CountView(View):
    template_name = 'explorer_app/count.html'

    def get(self, request: HttpRequest, filename: str) -> HttpResponse:
        people_table = ETLController.load(filename)
        context = {
            'filename': filename,
            'buttons': {name: False for name in people_table[0]}
        }
        return render(request, self.template_name, context=context)

    def post(self, request: HttpRequest, filename: str) -> HttpResponse:
        buttons = literal_eval(request.POST['buttons'])
        buttons[request.POST['selected_button']] = not buttons[request.POST['selected_button']]
        context = {
            'filename': filename,
            'buttons': buttons,
        }
        count_by = tuple(name for name, is_highlighted in buttons.items() if is_highlighted)
        if count_by:
            count_table = ETLController.count(
                source=filename,
                by=count_by if not len(count_by) == 1 else count_by[0]
            )
            context = {
                **context,
                'table_head': count_table[0],
                'table_body': count_table[1:],
            }
        return render(request, self.template_name, context=context)
