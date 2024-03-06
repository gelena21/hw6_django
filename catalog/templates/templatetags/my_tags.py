from django import template

register = template.Library()


@register.filter()
def show_img(img_url):
    if img_url:
        return f'/media/{img_url}'
    return ("https://otvet.imgsmail.ru/download/209827595_062753955e431ed09b9ea0bb74716df2_800.jpg")
