import qrcode
import pandas as pd
from PIL import Image
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import CircleModuleDrawer, SquareModuleDrawer


def lectura_excel():
    df = pd.read_excel(
        "C:\\Users\\omar.martinez\\OneDrive - HNG DESARROLLO, S.A DE C.V., SOFOM, E.N.R\\Personal\\XV Ivonne\\Lista de Invitados Final.xlsx",
        skiprows=1,
    )
    print(df.head())
    for i in range(len(df)):
        created_qr(df["ID_Guest"][i])


def created_qr(id):
    # Llenamos de datos el código QR
    url = f"https://xvivonne.com/invite?id={id}&QR=1"  # URL del Código
    qr = qrcode.QRCode(
        version=10,
        # https://github.com/lincolnloop/python-qrcode/blob/df139670ac44382d4b70820edbe0a9bfda9072aa/qrcode/util.py#L183
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        # border=18,
        mask_pattern=4,  # https://www.thonky.com/qr-code-tutorial/mask-patterns,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Agregamos nuestra imagen al código QR
    QRimg = qr.make_image(
        fill_color="white",
        back_color=None,
        image_factory=StyledPilImage,
        module_drawer=CircleModuleDrawer(resample_method=None),
        eye_drawer=SquareModuleDrawer(),
    )
    # Guardamos la imagen de nuestro código QR en un directorio
    QRimg.save(f"QRs/preview/{id}.jpg")

    # Abrir las imágenes
    imagen_grande = Image.open(f"QRs/preview/{id}.jpg")
    imagen_pq = Image.open("QRs/XV.png")

    # Redimensionar la imagen pequeña al tamaño deseado
    new_size = (250, 250)  # Cambia este tamaño a tus preferencias
    imagen_pq_rz = imagen_pq.resize(new_size)

    # Superponer la imagen pequeña redimensionada sobre la imagen grande
    pos = (200, 200)  # Cambia esta posición a tus preferencias
    imagen_grande.paste(imagen_pq_rz, pos, imagen_pq_rz)

    # Mostrar la imagen resultante
    # imagen_grande.show()
    imagen_grande.save(f"QRs/finals/{id}.jpg")


if __name__ == "__main__":
    lectura_excel()
