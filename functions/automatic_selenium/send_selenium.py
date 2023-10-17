import time
import pyshorteners as ps
from selenium import webdriver
from selenium.webdriver.common.by import By
from functions.config import *


def inicio_program():
    url = "https://web.whatsapp.com"
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument("--disk-cache-dir=/path/to/cache")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    print("Scan QR Code, And then Enter")
    input()
    print("Logged In")
    # envio_mensajes("5579221449","Hola",driver)
    lista_invitados(driver)


def lista_invitados(driver):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_guest,phone,name,url,id_postday FROM guests WHERE status='test'"
        )
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            if row[1] is not None:
                mensaje = obtener_mensaje(0, row[2], row[0])
                status_envio = envio_mensajes(row[1], mensaje, driver, "text")
                link = short_url(f"https://xvivonne.com/invite?id={row[0]}&WA=1")
                status_envio_link = envio_mensajes(row[1], link, driver, "link")
                if status_envio and status_envio_link:
                    actualizar_estatus(row[0], "sent")
                else:
                    actualizar_estatus(row[0], "error")

    except Exception as e:
        print(e)


def actualizar_estatus(id, status):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE guests SET status ='{status}' WHERE id_guest = '{id}'")
        conn.commit()
        conn.close()

    except Exception as e:
        print(e)


def obtener_mensaje(id, nombre, id_guest):
    # Indicador de mensajes
    # 0- Solo invitación
    # 1- Invitación y desayuno
    mensaje = ""
    if id == 0:
        mensaje = (
            f"_Hola {nombre}_%0A"
            "🎉_¡Celebra con nosotros en una noche llena de magia y alegría en los XV años de *Ivonne*! Este "
            "evento tan especial marcará un nuevo capítulo en su vida, y nos encantaría contar con tu presencia "
            "para hacerlo aún más memorable._%0A%0A"
            "_Prepárate para disfrutar de una velada llena de música, baile y diversión, rodeados de amigos y "
            "familiares. Tu compañía será el regalo más valioso que podríamos recibir._🎁%0A%0A"
            "_Por favor, es *importante* confirmar tu asistencia antes del *14 de octubre* ‼️ para poder "
            "organizar todos los detalles de manera adecuada._%0A%0A"
            "_¡Esperamos verte y compartir juntos esta celebración inolvidable!_%0A%0A"
            "Atentamente,%0A"
            "👨‍👩‍👧‍👧Fam. Martínez Lemus%0A"
        )  # f"https://xvivonne.com/invitacion/index.php?id={id_guest}&WA=1"
    elif id == 1:
        mensaje = (
            f"_Hola {nombre}_%0A"
            "🎉_¡Celebra con nosotros en una noche llena de magia y alegría en los XV años de *Ivonne*! Este "
            "evento tan especial marcará un nuevo capítulo en su vida, y nos encantaría contar con tu presencia "
            "para hacerlo aún más memorable._%0A%0A"
            "_Prepárate para disfrutar de una velada llena de música, baile y diversión, rodeados de amigos y "
            "familiares. Tu compañía será el regalo más valioso que podríamos recibir._🎁%0A%0A"
            "_Además te consideramos un invitado especial y queremos compartir contigo un delicioso desayuno🌮, "
            "organizado por el banquete, "
            "al día siguiente a las 11:00 am⏰ para prolongar la alegría de la celebración y seguir "
            "compartiendo momentos y recuerdos._%0A%0A"
            "_Para contribuir a los gastos de este desayuno especial, se ha establecido un costo de *$250* pesos "
            "por persona. Sabemos que cada uno de ustedes es parte importante de esta celebración, "
            "y agradecemos su consideración en este aspecto._%0A%0A"
            "_Por favor, es *importante* confirmar tu asistencia antes del *14 de octubre* ‼️ para poder "
            "organizar todos los detalles de manera adecuada y también pedimos de tu apoyo para que en la "
            "sección de comentarios, al momento de confirmar, nos compartas si podemos contar contigo para el "
            "desayuno._%0A%0A"
            "_¡Esperamos verte y compartir juntos esta celebración inolvidable!_%0A%0A"
            "Atentamente,%0A"
            "👨‍👩‍👧‍👧Fam. Martínez Lemus%0A"
        )  # f"https://xvivonne.com/invitacion/index.php?id={id_guest}&WA=1"
    return mensaje


def envio_mensajes(telefono, mensaje, driver, type):
    try:
        new_url = (
            "https://web.whatsapp.com/send/?phone=" + telefono + "&text=" + mensaje
        )
        driver.execute_script("window.open('');")
        # driver.switch_to.window(driver.window_handles[1])
        driver.get(new_url)
        current_window_handle = driver.current_window_handle
        window_handles = driver.window_handles
        for window_handle in window_handles:
            if window_handle != current_window_handle:
                driver.switch_to.window(window_handle)
                driver.close()
        driver.switch_to.window(current_window_handle)
        time.sleep(5)
        driver.set_window_size(1293, 707)
        if type == "link":
            return esperar_miniatura(driver)
        else:
            time.sleep(2)
            driver.find_element(
                By.XPATH,
                "//div[@id='main']/footer/div/div/span[2]/div/div[2]/div[2]/button/span",
            ).click()
            # driver.find_element(By.CSS_SELECTOR, ".oq44ahr5 > span").click()
            time.sleep(2)
            return True

    except Exception as e:
        print(e)
        print("Error al enviar mensaje a: " + telefono)
        return False


def esperar_miniatura(driver):
    miniatura_len = len(
        driver.find_elements(
            By.CSS_SELECTOR, "[data-testid='link-preview-thumbnail-jpeg']"
        )
    )
    print(
        driver.find_elements(
            By.CSS_SELECTOR, "QRs[data-testid='link-preview-thumbnail-jpeg']"
        )
    )
    while miniatura_len == 0:
        print("Esperando miniatura...")
        time.sleep(1)
        miniatura_len = len(
            driver.find_elements(
                By.CSS_SELECTOR, "QRs[data-testid='link-preview-thumbnail-jpeg']"
            )
        )
        if miniatura_len > 0:
            print("Miniatura encontrada")
            time.sleep(3)
            driver.find_element(
                By.XPATH,
                "//div[@id='main']/footer/div/div/span[2]/div/div[2]/div[2]/button/span",
            ).click()
            return True
    if miniatura_len > 0:
        print("Miniatura encontrada")
        time.sleep(3)
        driver.find_element(
            By.XPATH,
            "//div[@id='main']/footer/div/div/span[2]/div/div[2]/div[2]/button/span",
        ).click()
        return True


def short_url(url):
    shorter_url = ps.Shortener().tinyurl.short(url)
    return shorter_url
