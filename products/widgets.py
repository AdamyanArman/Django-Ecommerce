from django import forms
from django.utils.safestring import mark_safe
from django.forms.widgets import CheckboxSelectMultiple


class GroupedCheckboxSelectMultiple(forms.SelectMultiple):
    """
    Ցուցադրում է AttributeValue-երը՝ խմբավորված ըստ իրենց Attribute-ի,
    որպես checkbox-ների առանձին բաժիններ։
    """
    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = []
        selected_ids = {str(v) for v in value}

        # Խմբավորում ենք values-երը ըստ attribute-ի
        from .models import AttributeValue
        grouped = {}
        for av in AttributeValue.objects.select_related('attribute').all():
            grouped.setdefault(av.attribute, []).append(av)

        html = ['<div class="grouped-checkbox-widget">']
        for attribute, values in grouped.items():
            html.append(f'<fieldset style="margin-bottom:12px; border:1px solid #ccc; padding:8px;">')
            html.append(f'<legend style="font-weight:bold;">{attribute.name_hy}</legend>')
            for av in values:
                checked = 'checked' if str(av.pk) in selected_ids else ''
                html.append(
                    f'<label style="display:inline-block; margin-right:15px;">'
                    f'<input type="checkbox" name="{name}" value="{av.pk}" {checked}> '
                    f'{av.value_hy}'
                    f'</label>'
                )
            html.append('</fieldset>')
        html.append('</div>')

        return mark_safe(''.join(html))