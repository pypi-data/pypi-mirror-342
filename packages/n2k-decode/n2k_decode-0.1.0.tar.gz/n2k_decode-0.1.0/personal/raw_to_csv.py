import os
import glob
import pickle
import logging
from typing import List, Dict, Any
import pandas as pd
from marulc import parse_from_iterator, NMEA2000Parser
from pathlib import Path
import json

# Configuration du logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configuration des chemins
PATH = Path("/data/can")
CACHE_FILE = PATH / "all_messages.pkl"
CACHE_FILE_JSON = PATH / "all_messages_json.pkl"
OUTPUT_CSV = PATH / "data.csv"
OUTPUT_EXCEL = PATH / "data.xlsx"
FAILED_MESSAGES_FILE = PATH / "failed_messages.txt"

# PGNs d'intérêt
GPS_PGNS = {
    "126992": "System Time",
    "129033": "Date, Time and Local Offset",
    "129025": "Position, Rapid Update",
    "129029": "GNSS Position Data",
}


def read_multi_frame_file(filepath: str) -> List[str]:
    """
    Lit un fichier de messages CAN et extrait les données.

    Args:
        filepath: Chemin vers le fichier à lire

    Returns:
        Liste des messages CAN extraits
    """
    messages = []
    try:
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data_1 = line.split("[")[0].split()[-1]
                    data_2 = line.split("]")[-1]
                    data = f" {data_1} {data_2}".strip()
                    messages.append(data)
                except IndexError:
                    logger.warning(f"Format de ligne invalide dans {filepath}: {line}")
    except Exception as e:
        logger.error(f"Erreur lors de la lecture du fichier {filepath}: {str(e)}")
        raise
    return messages


def load_or_create_cache() -> List[str]:
    """
    Charge les messages depuis le cache ou les crée si nécessaire.

    Returns:
        Liste de tous les messages CAN
    """
    if CACHE_FILE.exists():
        logger.info(f"Chargement depuis le cache : {CACHE_FILE}")
        try:
            with open(CACHE_FILE, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            logger.error(f"Erreur lors du chargement du cache : {str(e)}")
            raise

    logger.info("Lecture des fichiers bruts...")
    directory_raw_path = PATH / "raw" / "*.log"
    all_messages = []

    try:
        for file in glob.glob(str(directory_raw_path)):
            all_messages.extend(read_multi_frame_file(file))
    except Exception as e:
        logger.error(f"Erreur lors de la lecture des fichiers bruts : {str(e)}")
        raise

    logger.info(f"Nombre total de messages : {len(all_messages)}")

    try:
        with open(CACHE_FILE, "wb") as f:
            pickle.dump(all_messages, f)
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde du cache : {str(e)}")
        raise

    return all_messages


def parse_messages(messages: List[str]) -> tuple[List[Dict[str, Any]], List[str]]:
    """
    Parse les messages CAN en utilisant le parser NMEA2000.

    Args:
        messages: Liste des messages CAN à parser

    Returns:
        Tuple contenant la liste des messages parsés et la liste des messages en échec
    """
    parser = NMEA2000Parser()
    parsed_data = []
    failed_messages = []

    for i, raw_msg in enumerate(messages, 1):
        if i % 2500000 == 0:
            logger.info(f"Progression : {i}/{len(messages)} messages traités")

        try:
            for parsed in parse_from_iterator(parser, [raw_msg], quiet=True):
                if parsed.get("Fields"):
                    d = parsed["Fields"].copy()
                    d["PGN"] = parsed["PGN"]
                    parsed_data.append(d)
        except Exception as e:
            # logger.warning(f"Erreur lors du parsing du message {i}: {str(e)}")
            failed_messages.append(raw_msg)

    # Sauvegarde des messages en échec
    if failed_messages:
        try:
            with open(FAILED_MESSAGES_FILE, "w") as f:
                for msg in failed_messages:
                    f.write(f"{msg}\n")
            logger.info(f"Messages en échec sauvegardés dans : {FAILED_MESSAGES_FILE}")
        except Exception as e:
            logger.error(
                f"Erreur lors de la sauvegarde des messages en échec : {str(e)}"
            )

    return parsed_data, failed_messages


def save_dataframe(df: pd.DataFrame) -> None:
    """
    Sauvegarde le DataFrame dans différents formats.

    Args:
        df: DataFrame à sauvegarder
    """
    try:
        # Tentative de remplissage des valeurs manquantes pour date et time
        if "date" in df.columns and "time" in df.columns:
            df[["date", "time"]] = df[["date", "time"]].ffill()

        # Sauvegarde en CSV
        df.to_csv(OUTPUT_CSV, index=False)
        logger.info(f"Données sauvegardées en CSV : {OUTPUT_CSV}")

        # Sauvegarde en Excel avec gestion des grandes tailles
        max_rows = 1_000_000  # Limite Excel - marge de sécurité
        if len(df) > max_rows:
            logger.info(
                f"Le dataset est trop grand pour un seul fichier Excel ({len(df)} lignes). Découpage en plusieurs fichiers..."
            )

            # Calcul du nombre de fichiers nécessaires
            n_files = (len(df) // max_rows) + 1

            for i in range(n_files):
                start_idx = i * max_rows
                end_idx = min((i + 1) * max_rows, len(df))
                df_part = df.iloc[start_idx:end_idx]

                output_file = (
                    OUTPUT_EXCEL.parent
                    / f"{OUTPUT_EXCEL.stem}_{i+1}{OUTPUT_EXCEL.suffix}"
                )
                df_part.to_excel(output_file, index=False)
                logger.info(f"Partie {i+1}/{n_files} sauvegardée dans : {output_file}")
        else:
            df.to_excel(OUTPUT_EXCEL, index=False)
            logger.info(f"Données sauvegardées en Excel : {OUTPUT_EXCEL}")

    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde des données : {str(e)}")
        raise


def save_json_data(data: List[Dict[str, Any]]) -> None:
    """
    Sauvegarde les données parsées en format JSON.

    Args:
        data: Liste des données à sauvegarder
    """
    try:
        with open(CACHE_FILE_JSON, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Données sauvegardées en JSON : {CACHE_FILE_JSON}")
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde en JSON : {str(e)}")
        raise


def filter_gps_messages(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filtre les messages pour ne garder que ceux liés au GPS et au temps.

    Args:
        messages: Liste des messages à filtrer

    Returns:
        Liste des messages filtrés
    """
    return [msg for msg in messages if str(msg.get("PGN", "")) in GPS_PGNS]


def main():
    """Fonction principale du script."""
    try:
        # Vérification si le fichier JSON existe déjà
        if CACHE_FILE_JSON.exists():
            logger.info(f"Chargement depuis le fichier JSON : {CACHE_FILE_JSON}")
            with open(CACHE_FILE_JSON, "r") as f:
                parsed_data = json.load(f)
            failed_messages = []
        else:
            # Chargement des messages
            all_messages = load_or_create_cache()

            # Parsing des messages
            parsed_data, failed_messages = parse_messages(all_messages)

            if failed_messages:
                logger.warning(f"Nombre de messages en échec : {len(failed_messages)}")

            # Sauvegarde des messages en JSON
            save_json_data(parsed_data)

        # Filtrage des messages GPS
        parsed_data = filter_gps_messages(parsed_data)
        logger.info(f"Nombre de messages GPS/temps : {len(parsed_data)}")

        # Création et sauvegarde du DataFrame
        df = pd.DataFrame(data=parsed_data)
        save_dataframe(df)

        logger.info("Traitement terminé avec succès")

    except Exception as e:
        logger.error(f"Erreur critique : {str(e)}")
        raise


if __name__ == "__main__":
    main()
