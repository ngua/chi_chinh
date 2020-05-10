from django.db.models.functions import Greatest
from django.views.generic import ListView
from django.contrib.postgres.search import TrigramSimilarity
from django.views.decorators.http import require_safe
from django.utils.decorators import method_decorator
from recipes.models import Recipe


@method_decorator(require_safe, name='dispatch')
class RecipeSearchListView(ListView):
    model = Recipe
    template_name = 'search/results.html'
    paginate_by = 10

    def get_queryset(self):
        """
        Searches for trigrams matching query in Recipe instance's
        name, description, and categories. Low similarity required
        for fuzzy searches of Vietnamese characters without diacritics,
        e.g. 'Việt' --> 'viet'

        TODO Improve search efficiency and speed - dedicated search vector
        model field and/or gin index
       """
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
            ).filter(similarity__gte=0.1).order_by('-similarity').distinct()
            self.total = len(qs)
            self.q = q
        return qs

    def get_context_data(self, **kwargs):
        """
        Overrides parent method to insert additional context for use in
        template - q (original search query) and total number of results
        """
        context = super().get_context_data(**kwargs)
        context['query'] = self.q
        context['total'] = self.total
        return context
