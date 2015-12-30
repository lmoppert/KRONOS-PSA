from psa.models import PSAProduct, PSACategory
from HTMLParser import HTMLParser
from html2text import html2text


def unescape(code):
    "We need to unescape twice for the umlaute"

    HTML = HTMLParser()
    return HTML.unescape(HTML.unescape(code))


def decode_teaser():
    print "Decoding category teaser text..."
    for category in PSACategory.objects.all():
        category.teaser = html2text(unescape(category.teaser))
        category.save()
    print "...Done"


def decode_description():
    print "Decoding item description text..."
    for item in PSAProduct.objects.all():
        item.description = html2text(item.description)
        item.save()
    print "...Done"


def run():
    decode_teaser()
    decode_description()
    print "All objecst decoded - Thanks for your patience!"
