import datetime
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, FormView

from .models import Category, Task


class TasksListView(ListView):
    paginate_by = 10
    template_name = 'index.html'
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.get_user_categories(self.request)
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        qs = super().get_queryset().filter(owner=self.request.user).filter(status='NW')
        if query:
            qs = qs.filter(Q(title__icontains=query) | Q(content__icontains=query))
        return qs

    def get(self, request, *args, category_slug=None):
        category = None
        self.object_list = self.get_queryset()
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            self.object_list = self.get_queryset().filter(category=category)
        context = self.get_context_data()
        context['category'] = category
        return self.render_to_response(context)


class TodayListView(TasksListView):
    def get_queryset(self):
        qs = super().get_queryset().filter(day_to_perform=datetime.date.today())
        return qs


class TomorrowListView(TasksListView):
    def get_queryset(self):
        qs = super().get_queryset().filter(day_to_perform=datetime.date.today() + datetime.timedelta(days=1))
        return qs


class ExpiredTasksView(TasksListView):
    def get_queryset(self):
        qs = Task.objects.filter(owner=self.request.user).filter(status='EXP')
        return qs


class CreateTaskView(CreateView):
    model = Task
    fields = ['title', 'content', 'priority', 'day_to_perform', 'category']
    template_name = 'add_task.html'
    success_url = reverse_lazy('task:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        return super(CreateTaskView, self).form_valid(form)


@csrf_exempt
def complete_task(request):
    if request.is_ajax():
        task_id = request.GET.get('task_id')
        Task.change_status(task_id, 'OK')
        return JsonResponse({'status': 'Ok'})


@csrf_exempt
def delete_task(request):
    if request.is_ajax():
        task_id = request.GET.get('task_id')
        Task.change_status(task_id, 'DL')
        return JsonResponse({'status': 'Ok'})


def chart(request):
    pie_chart = Task.get_completed_tasks_per_day(request)
    bar_chart = Task.get_number_of_tasks_by_status(request)
    return render(request, 'pie_chart.html', {
        'labels': pie_chart[0],
        'data': pie_chart[1],
        'labels1': bar_chart[0],
        'data1': bar_chart[1]
    })
