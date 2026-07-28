from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .constants import MAX_SCORE, MIN_SCORE

def validate_year(value):
    """Проверяет, что год не превышает текущий."""
    current_year = datetime.now().year
    if value > current_year:
        raise ValidationError(
            _('Год не может быть больше текущего (%(current_year)s)'),
            params={'current_year': current_year},
        )
        
def validate_score(value):
    """Проверяет, что оценка в диапазоне от 1 до 10."""
    if not (MIN_SCORE <= value <= MAX_SCORE):
        raise ValidationError(
            _(f'Оценка должна быть от {MIN_SCORE} до {MAX_SCORE}')
        )
    return value