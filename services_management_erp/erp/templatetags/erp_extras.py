from django import template
register=template.Library()
@register.filter
def get_attr(obj, name):
    try: return getattr(obj, name)
    except (AttributeError, TypeError): return ''
