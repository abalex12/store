from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def active_link(context, url_name):
    if context['request'].resolver_match.url_name == url_name:
        return 'active'
    return ''