# from django.contrib.auth.models import User
from filer.models.filemodels import File
from psa.models import PSAItem, PSACategory
from psa.legacy import StoreProducts, StoreCategories


##############################################################################
# Helper methods
##############################################################################
def get_file_handle(s):
    name = s.split('/')[-1]
    try:
        handle = File.objects.get(original_filename=name, folder_id=580)
    except:
        print "File not found: {}".format(name)
        return
    return handle


##############################################################################
# Create methods for the models
##############################################################################
def create_categories():
    count = 0
    objs = StoreCategories.objects.using('legacy_psa').all()
    print "Found {} Categories, processing migrattion...".format(objs.count())
    for obj in objs:
        oid = obj.pid
        count += 1
        PSACategory.objects.create(
            id=oid,
            name=obj.name,
            description=obj.description,
            teaser=obj.teaser,
        )
    print "... building hirarchy...".format(objs.count())
    for obj in objs:
        try:
            parent = PSACategory.objects.get(pk=obj.parent.pid)
            child = PSACategory.objects.get(pk=obj.pid)
            child.parent = parent
            child.save()
        except:
            pass
    print "... {} Categories migrated".format(count)


def create_items():
    count = 0
    objs = StoreProducts.objects.using('legacy_psa').all()
    print "Found {} Items, processing migrattion...".format(objs.count())
    for obj in objs:
        count += 1
        category = PSACategory.objects.get(pk=obj.category.pid)
        PSAItem.objects.create(
            name=obj.name,
            number=obj.number,
            description=obj.description,
            image=get_file_handle(obj.image),
            category=category,
        )
    print "... {} Items migrated".format(count)


##############################################################################
# Main method
##############################################################################
def run():
    create_categories()
    create_items()
    print "All objecst migrated - Thanks for your patience!"
