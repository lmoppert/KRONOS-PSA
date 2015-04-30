import re
from base64 import b64encode
from django import template
from django.utils.safestring import mark_safe
from reportlab.lib.units import mm
from reportlab.graphics import renderPM
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics.shapes import Drawing


register = template.Library()


@register.filter
def markup(text):
    "Show  text with corresponding markup"
    text = re.sub('\n', '\n<br>', text)
    text = re.sub('\*{2}(.+)\*{2}', '<strong>\\1</strong>', text)
    text = re.sub('  - (.+)', '<span style="padding-left: 10px">- \\1</span>',
                  text)
    return mark_safe(u'{}'.format(text))


@register.filter
def barcode(value):
    "generate a barcode for the provided value"
    barcode = createBarcodeDrawing("Code128", value=value, barHeight=8*mm,
                                   humanReadable=True, )
    drawing = Drawing(barcode.width, barcode.height)
    drawing.add(barcode, name='barcode')
    data = b64encode(renderPM.drawToString(drawing, fmt='PNG'))
    return mark_safe('<img src="data:image/png;base64,{}">'.format(data))
