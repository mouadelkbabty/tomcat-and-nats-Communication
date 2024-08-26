import asyncio
import nats
import time
from nats.errors import ConnectionClosedError, TimeoutError, NoServersError
from nats.aio.client import Client as NATS
import json
from datetime import datetime

async def main():
    # Se connecter au serveur NATS
    nc = await nats.connect(servers=["nats:machineIpAdresse:Port"], user="username", password="password")

    async def messagehandler(msg):
        # Convertir le message reçu en un dictionnaire JSON pour détécter la commande
        received_data = json.loads(msg.data.decode())

        if received_data.get("type") == "TELECOMMANDE" and received_data.get("action") == "GET_DATE&HEURE":
            # Initialiser la date et l'heure actuelles
            now = datetime.now()
            # Préparer la réponse du concentrateur
            response = {
                "dateCourante": now.strftime("%d/%m/%Y"),
                "heureCourante": now.strftime("%H:%M:%S"),
            }
            await nc.publish(msg.reply, json.dumps(response).encode())
            print(f"Réponse envoyée: {response}")
        else:
            # Si le message ne correspond pas, ne rien faire
            print(f"Message ignoré: {receiveddata}")

    # Écoute sur le sujet 'concentrateur.dateheure.get'
    await nc.subscribe("concentrateur.dateheure.get", cb=messagehandler)
    print("En écoute sur 'concentrateur.dateheure.get'...")

    # Maintenir le script en cours d'exécution
    while True:
        await asyncio.sleep(1)

if _name == '__main':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())