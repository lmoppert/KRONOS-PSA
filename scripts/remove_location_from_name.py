from psa.models import PSAProduct
import re


def run():
    print "Searching for location strings in names..."
    for item in PSAProduct.objects.all():
        item.name = re.sub("\(Leverkusen\)", '', item.name)
        item.name = re.sub("\(Leverku", '', item.name)
        item.name = re.sub("\(Le", '', item.name)
        item.name = re.sub("\(LEV\)", '', item.name)
        item.name = re.sub("LEV", '', item.name)
        item.name = re.sub("\(Nordenham\)", '', item.name)
        item.name = re.sub("\(Nordenahm\)", '', item.name)
        item.name = re.sub(", Nordenham", '', item.name)
        item.name = re.sub("\(Nordenh", '', item.name)
        item.name = re.sub("\(NHM\)", '', item.name)
        item.save()
