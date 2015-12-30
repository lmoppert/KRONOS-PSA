# vim: set fileencoding=utf-8 :
from psa.models import PSAProduct
import re


def run():
    for item in PSAProduct.objects.all():
        item.description = re.sub('\\\\  -', '  -', item.description)
        item.save()
