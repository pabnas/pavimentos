from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
import img2pdf
from PIL import Image
import os

"""https://www.roytuts.com/how-to-send-attachments-with-email-using-python/"""


def Enviar_correo2(subject, to, text):
    subject = subject
    from_email = "pointdato@gmail.com"
    to = to
    text_content = text
    html_content = 'This is an HTML message.'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)


def Enviar_correo(subject,mensaje,to,archivo=""):
    msg = EmailMessage(
        subject=subject,
        body=mensaje,
        from_email='pointdato@gmail.com',
        to=to,
        reply_to=['pointdato@gmail.com'],
        headers={'Message-ID': 'foo'},
    )
    if archivo != "":
        msg.attach_file(archivo)
    msg.send(fail_silently=False)

def img_to_pdf(ruta):
    # storing image path
    img_path = ruta
    # storing pdf path
    pdf_path = "Factura.pdf"
    # opening image
    image = Image.open(img_path)
    # converting into chunks using img2pdf
    pdf_bytes = img2pdf.convert(image.filename)
    # opening or creating pdf file
    file = open(pdf_path, "wb")
    # writing pdf files with chunks
    file.write(pdf_bytes)
    # closing image file
    image.close()
    # closing pdf file
    file.close()
