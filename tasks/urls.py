from django.urls import path

from tasks.views import TasksListView, CreateTaskView, complete_task, delete_task, TodayListView, TomorrowListView, \
    ExpiredTasksView, chart

app_name = 'task'


urlpatterns = [
    path('', TasksListView.as_view(), name='index'),
    path('category/<slug:category_slug>/', TasksListView.as_view(), name='category'),
    path('results/', TasksListView.as_view(), name='searching'),
    path('add', CreateTaskView.as_view(), name='create_task'),
    path('task/complete/', complete_task, name='complete_task'),
    path('task/delete/', delete_task, name='delete_task'),
    path('today/', TodayListView.as_view(), name='tasks_for_today'),
    path('tomorrow/', TomorrowListView.as_view(), name='tasks_for_tomorrow'),
    path('expired/', ExpiredTasksView.as_view(), name='expired_tasks'),
    path('pie-chart/', chart, name='pie-chart')
]

