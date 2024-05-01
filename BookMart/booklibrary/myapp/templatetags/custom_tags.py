from django import template

register=template.Library()

@register.simple_tag()
def half_contet(desc):
    return desc[:int(len(desc)/3)]