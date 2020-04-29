from django.db.models.functions import Greatest
from django.views.generic import ListView
from django.contrib.postgres.search import TrigramSimilarity
from recipes.models import Recipe


class RecipeSearchListView(ListView):
    model = Recipe
    template_name = 'search/results.html'
    paginate_by = 10

    def get_queryset(self):
        qs = Recipe.objects.all()
        q = self.request.GET.get('q')
        if q:
            qs = qs.annotate(
                similarity=Greatest(
                    TrigramSimilarity('name_en', q),
                    TrigramSimilarity('name_vi', q),
                    TrigramSimilarity('description_en', q),
                    TrigramSimilarity('description_vi', q),
                    TrigramSimilarity('categories__name_en', q),
                    TrigramSimilarity('categories__name_vi', q),
                )
            ).filter(similarity__gte=0.2).order_by('-similarity').distinct()
            self.total = len(qs)
            self.q = q
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.q
        context['total'] = self.total
        return context
