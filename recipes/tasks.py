import dramatiq


@dramatiq.actor
def unmark_new_task(recipe_id):
    from .models import Recipe
    try:
        recipe = Recipe.objects.get(id=recipe_id)
        recipe.new = False
        recipe.save()
        unmark_new_task.logger.info(
            f'{str(recipe)} is no longer marked as new'
        )
    except Recipe.DoesNotExist:
        unmark_new_task.logger.error(
            f'Recipe with ID {recipe_id} does not exist, '
            'task failed'
        )
