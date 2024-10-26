from django.http import JsonResponse
from django.views import generic
from django.urls import reverse_lazy
from .models import Courses
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

@method_decorator(csrf_exempt, name='dispatch')
class CourseListView(generic.ListView):
    model = Courses
    # Não precisamos de um template se retornarmos JSON
    def get(self, request, *args, **kwargs):
        courses = list(self.get_queryset().values())  # Obtém todos os cursos como dicionários
        return JsonResponse(courses, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CourseDetailView(generic.DetailView):
    model = Courses
    def get(self, request, *args, **kwargs):
        course = self.get_object()
        return JsonResponse({
            'id': course.id,
            'name': course.name,
            'description': course.description
        })

@method_decorator(csrf_exempt, name='dispatch')
class CourseCreateView(generic.CreateView):
    model = Courses
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        name = data['name']
        description = data['description']
        course = Courses.objects.create(name=name, description=description)
        return JsonResponse({
            'id': course.id,
            'name': course.name,
            'description': course.description
        }, status=201)

@method_decorator(csrf_exempt, name='dispatch')
class CourseUpdateView(generic.UpdateView):
    model = Courses
    def post(self, request, *args, **kwargs):
        course = self.get_object()
        course.name = request.POST.get('name', course.name)
        course.description = request.POST.get('description', course.description)
        course.save()
        return JsonResponse({
            'id': course.id,
            'name': course.name,
            'description': course.description
        })
    
@method_decorator(csrf_exempt, name='dispatch')
class CourseDeleteView(generic.DeleteView):
    model = Courses
    def post(self, request, *args, **kwargs):
        course = self.get_object()
        course.delete()
        return JsonResponse({'message': 'Curso deletado com sucesso!'}, status=204)