# vim: set fileencoding=utf-8 :
from psa.models import PSAProduct
import re


def run():
    for item in PSAProduct.objects.all():
        text = item.description
        text = re.sub(u'(Absperrband:)', '**\\1**', text)
        text = re.sub(u'(Beschreibung:)', '**\\1**', text)
        text = re.sub(u'(Bevorzugte Bereiche:)', '**\\1**', text)
        text = re.sub(u'(Durchmesser:)', '**\\1**', text)
        text = re.sub(u'(Geschmack:)', '**\\1**', text)
        text = re.sub(u'(Farbe:)', '**\\1**', text)
        text = re.sub(u'(Größe:)', '**\\1**', text)
        text = re.sub(u'(Klebeband:)', '**\\1**', text)
        text = re.sub(u'(Länge:)', '**\\1**', text)
        text = re.sub(u'(Maßeinheit:)', '**\\1**', text)
        text = re.sub(u'(Stulpenlänge:)', '**\\1**', text)
        item.description = text
        item.save()
