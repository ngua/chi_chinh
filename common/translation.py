from django.contrib.flatpages.models import FlatPage
from modeltranslation.translator import translator, TranslationOptions


class FlatPageTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


translator.register(FlatPage, FlatPageTranslationOptions)
