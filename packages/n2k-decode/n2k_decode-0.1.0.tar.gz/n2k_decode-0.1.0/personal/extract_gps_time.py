import json
import pandas as pd
from pathlib import Path
import logging
from typing import Dict, List, Any

# Configuration du logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configuration des chemins
PATH = Path("/data/can")
CACHE_FILE_JSON = PATH / "all_messages_json.pkl"
OUTPUT_GPS_FILE = PATH / "gps_data.csv"

# PGNs d'intérêt
GPS_PGNS = {
    "126992": "System Time",
    "129033": "Date, Time and Local Offset",
    "129025": "Position, Rapid Update",
    "129029": "GNSS Position Data",
}


def extract_gps_data() -> None:
    """
    Extrait les données GPS et temporelles des messages parsés.
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

        # Filtrage des messages GPS et temporels
        gps_data = []
        for msg in data:
            pgn = str(msg.get("PGN", ""))
            if pgn in GPS_PGNS:
                msg_data = {
                    "PGN": pgn,
                    "PGN_Description": GPS_PGNS[pgn],
                    "Timestamp": msg.get("Timestamp", ""),
                    "Date": msg.get("Date", ""),
                    "Time": msg.get("Time", ""),
                    "Latitude": msg.get("Latitude", ""),
                    "Longitude": msg.get("Longitude", ""),
                    "Altitude": msg.get("Altitude", ""),
                    "Speed": msg.get("Speed", ""),
                    "Course": msg.get("Course", ""),
                    "Raw_Data": msg,
                }
                gps_data.append(msg_data)

        # Création du DataFrame
        df = pd.DataFrame(gps_data)

        if not df.empty:
            # Tri par timestamp
            if "Timestamp" in df.columns:
                df = df.sort_values("Timestamp")

            # Sauvegarde des résultats
            df.to_csv(OUTPUT_GPS_FILE, index=False)
            logger.info(f"Données GPS sauvegardées dans : {OUTPUT_GPS_FILE}")
        else:
            logger.warning("Aucune donnée GPS trouvée dans les messages")
            return

        # Affichage des statistiques
        print("\nStatistiques des données GPS :")
        print(f"Nombre total de messages GPS : {len(df)}")
        print("\nRépartition par PGN :")
        print(df["PGN_Description"].value_counts())

        # Affichage d'un échantillon des données
        print("\nAperçu des données :")
        print(df.head().to_string())

    except Exception as e:
        logger.error(f"Erreur lors de l'extraction des données GPS : {str(e)}")
        raise


if __name__ == "__main__":
    extract_gps_data()
