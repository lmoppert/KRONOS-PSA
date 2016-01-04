# from django.contrib.auth.models import User
from psa.models import PSACategory


def run():
    objs = PSACategory.objects.filter(active=True).filter(level=0)
    for num, obj in enumerate(objs.order_by('name')):
        index = (num + 1) * 20
        print "Processing category {}".format(index)
        obj.order = index
        obj.save()
        subs = PSACategory.objects.filter(parent__id=obj.id).order_by('name')
        for snum, sub in enumerate(subs):
            sub.order = index + snum
            sub.save()

    print "Tree has been sorted - Thanks for your patience!"
