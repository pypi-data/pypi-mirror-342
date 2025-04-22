import pandas as pd
import folium
from pathlib import Path
import logging
from typing import List, Dict, Any
import json

# Configuration du logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configuration des chemins
PATH = Path("/data/can")
CACHE_FILE_JSON = PATH / "all_messages_json.pkl"
OUTPUT_MAP = PATH / "gps_map.html"


def create_gps_map() -> None:
    """
    Crée une carte interactive avec les positions GPS.
    """
    try:
        # Vérification si le fichier JSON existe
        if not CACHE_FILE_JSON.exists():
            logger.error(f"Fichier JSON non trouvé : {CACHE_FILE_JSON}")
            logger.info(
                "Veuillez d'abord exécuter raw_to_csv.py pour générer les données JSON"
            )
            return

        # Lecture des données JSON
        with open(CACHE_FILE_JSON, "r") as f:
            data = json.load(f)

        # Filtrage des messages GPS
        gps_messages = [
            msg
            for msg in data
            if str(msg.get("PGN", ""))
            in ["129025", "129029"]  # Position Rapid Update et GNSS Position Data
            and "latitude" in msg
            and "longitude" in msg
            and msg["latitude"] is not None
            and msg["longitude"] is not None
        ]

        logger.debug(gps_messages[:5])

        if not gps_messages:
            logger.warning("Aucune position GPS trouvée dans les données")
            # Affichage des PGNs disponibles
            available_pgns = set(str(msg.get("PGN", "")) for msg in data)
            logger.info("\nPGNs disponibles dans les données :")
            for pgn in sorted(available_pgns):
                if pgn:  # Ne pas afficher les PGNs vides
                    logger.info(f"- PGN {pgn}")
            return

        # Création de la carte centrée sur la première position
        first_pos = gps_messages[0]
        m = folium.Map(
            location=[first_pos["latitude"], first_pos["longitude"]], zoom_start=15
        )

        # Ajout des points sur la carte
        for msg in gps_messages:
            # Création du popup avec les informations
            popup_text = f"""
            <b>Date:</b> {msg.get('Date', 'N/A')}<br>
            <b>Heure:</b> {msg.get('Time', 'N/A')}<br>
            <b>Vitesse:</b> {msg.get('Speed', 'N/A')} noeuds<br>
            <b>Cap:</b> {msg.get('Course', 'N/A')}°
            """

            # Ajout du marqueur
            folium.CircleMarker(
                location=[msg["latitude"], msg["longitude"]],
                radius=3,
                popup=folium.Popup(popup_text, max_width=300),
                color="blue",
                fill=True,
                fill_color="blue",
            ).add_to(m)

        # Ajout d'une ligne pour tracer le parcours
        coordinates = [[msg["latitude"], msg["longitude"]] for msg in gps_messages]
        folium.PolyLine(coordinates, weight=2, color="red", opacity=0.5).add_to(m)

        # Sauvegarde de la carte
        m.save(OUTPUT_MAP)
        logger.info(f"Carte GPS sauvegardée dans : {OUTPUT_MAP}")
        logger.info(f"Nombre de points GPS tracés : {len(gps_messages)}")

    except Exception as e:
        logger.error(f"Erreur lors de la création de la carte GPS : {str(e)}")
        raise


if __name__ == "__main__":
    create_gps_map()
