#Evaluation
#Proyecto desarrollado por: Masaru González y Gustavo Monzón

#ETAPAS - Para la elaboración del proyecto identificamos dos etapas:

#1. La primera etapa consistió en obtener las direcciones IP de usuarios conectados a una red WI-FI
# (el proceso se mostrará en el código), para lo cual se llevó a cabo una búsqueda de información en Google,
# StackOverFlow, entre otras plataformas.

#2. Al contar con el código que nos permite identificar las direcciones IP de los usuarios conectados
# a la misma red WI-FI, surgió la pregunta si podíamos automatizar el proceso de obtención de la
# puerta de enlace predeterminada, la cual es necesaria para poder conocer la cantidad de usuarios conectados
# a la red WI-FI, ya que a través de ella se envían los paquetes ARP (Address Resolution Protocol).


#DESARROLLO DEL PROYECTO


#Importamos una de las librerías que sirven para web scraping, en este caso scapy
#Para usar scapy en Windows es necesario instalar Npcap or Winpcap, de lo contrario arrojará un error
from scapy.all import *
import platform
import subprocess

#ETAPA 2 DEL PROYECTO

#Como se mencionó anteriormente, se buscó la forma de automatizar el proceso de la obtención de la
# puerta de enlace predeterminada con el fin de que el individuo que quiera obtener la cantidad de usuarios
# conectados a una red wi-fi no manipule manualmente el código y haga la búsqueda de dicha puerta de enlace
# en el cmd de su computador.

#Proceso

# Comprobar el sistema operativo
if platform.system() == "Windows":
    # Ejecutar el comando "ipconfig" en la consola (si se tiene sistema operativo Linux el comando es ifconfig)
    output = subprocess.check_output("ipconfig").decode("cp1252")

    # Para saber cuántos dispositivos están conectados a la red, es necesario analizar la red en la cual
    # está conectado nuestro computador

    # Se busca la línea que contiene la puerta de enlace predeterminada
    for line in output.split("\n"):
        if "Puerta de enlace predeterminada . . . . . :" in line:
            # Extraer la dirección IP de la puerta de enlace predeterminada
            default_gateway = line.split(":")[1].strip()
            print(f"La puerta de enlace predeterminada es: {default_gateway}")
            break


#ETAPA 1 DEL PROYECTO

# Al momento de iniciar el desarrollo del proyecto la variable target_ip era colocada manualmente
# dependiendo de la puerta de enlace a la que estabamos conectados (WI-FI). Posteriormnete, dado el
# desarrollo de la etapa 2 ya no es necesario hacer dicha búsqueda.

#Proceso

# En esta etapa se creó un paquete ARP (Address Resolution Protocol) el cual se utilizó para determinar
# la direccion MAC (Media Access Control), la cual se encuentra asociada a una dirección IP en una red local;
# el paquete ARP se envía a una subred específica (default_gateway) y al obtener respuesta a dicho paquete
# se contabilizan y almacenan las direcciones MAC y a su vez las direcciones IP obtenidas.

target_ip = default_gateway+'/24' #Para identificar los dispositivos conectados a la puerta de enlace
# predeterminada establecida es necesario añadir '/24'


#Crear el paquete ARP

#Variable arp

#Segunda capa ARP

arp_header = ARP(pdst=target_ip)

#Tercera capa ARP
ether_header = Ether(dst="ff:ff:ff:ff:ff:ff") #El comando ETHER permite extraer la dirección MAC de los
#dispositivos conectados a la red.

#Crear paquete

packet = ether_header/arp_header

answers = srp(packet,timeout=2,verbose=0)[0] #Pregunta a cada solicitud del router a quien pertenecer la IP.

ip_list = [] #Lista donde se almacenarán las IPS conectadas a la red.

for sent,received in answers:
    ip_list+=[[received.psrc,received.hwsrc]]

total_ips = len(ip_list)

for i in range(total_ips):
    print("IP:{} MAC:{}".format(ip_list[i][0],ip_list[i][1]))

total_ips = len(ip_list)
print(f"Total de direcciones IP encontradas: {total_ips}")


