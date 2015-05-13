from base64 import b64encode
from django import template
from django.utils.safestring import mark_safe
from reportlab.graphics import renderPM
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics.shapes import Drawing


register = template.Library()


@register.filter
def barcode(value):
    "generate a barcode for the provided value"
    barcode = createBarcodeDrawing("Code128", value=str(value))
    scale = 30 / barcode.height
    drawing = Drawing(barcode.width * scale, 30)
    drawing.scale(scale, scale)
    drawing.add(barcode, name='barcode')
    data = b64encode(renderPM.drawToString(drawing, fmt='PNG'))
    return mark_safe('<img src="data:image/png;base64,{}">'.format(data))
