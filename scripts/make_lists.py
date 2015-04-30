# vim: set fileencoding=utf-8 :
from psa.models import PSAItem
import re


def run():
    for item in PSAItem.objects.all():
        item.description = re.sub('\\\\  -', '  -', item.description)
        item.save()
