import logging
from pathlib import Path
import pandas as pd
from typing import List, Dict
import re

# Configuration du logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configuration des chemins
PATH = Path("/data/can")
FAILED_MESSAGES_FILE = PATH / "failed_messages.txt"
FAILED_PGN_FILE = PATH / "failed_pgns.csv"


def extract_pgn_from_message(message: str) -> str:
    """
    Extrait le PGN d'un message CAN.

    Args:
        message: Message CAN brut

    Returns:
        PGN extrait ou None si non trouvé
    """
    # Pattern pour extraire le PGN (3 bytes après le timestamp)
    pattern = r"^\d+\s+([0-9A-F]{6})"
    match = re.match(pattern, message)
    if match:
        return match.group(1)
    return None


def analyze_failed_messages() -> None:
    """
    Analyse les messages en échec et extrait leurs PGNs.
    """
    try:
        # Lecture des messages en échec
        if not FAILED_MESSAGES_FILE.exists():
            logger.error(
                f"Fichier des messages en échec non trouvé : {FAILED_MESSAGES_FILE}"
            )
            return

        with open(FAILED_MESSAGES_FILE, "r") as f:
            failed_messages = f.readlines()

        # Analyse des PGNs
        pgn_counts: Dict[str, int] = {}
        for message in failed_messages:
            pgn = extract_pgn_from_message(message.strip())
            if pgn:
                pgn_counts[pgn] = pgn_counts.get(pgn, 0) + 1

        # Création du DataFrame
        df = pd.DataFrame(
            {"PGN": list(pgn_counts.keys()), "Count": list(pgn_counts.values())}
        )

        # Tri par nombre d'occurrences
        df = df.sort_values("Count", ascending=False)

        # Sauvegarde des résultats
        df.to_csv(FAILED_PGN_FILE, index=False)
        logger.info(f"Analyse des PGNs en échec sauvegardée dans : {FAILED_PGN_FILE}")
        logger.info(f"Nombre total de PGNs différents en échec : {len(pgn_counts)}")

        # Affichage des statistiques
        print("\nStatistiques des PGNs en échec :")
        print(df.to_string(index=False))

    except Exception as e:
        logger.error(f"Erreur lors de l'analyse des messages en échec : {str(e)}")
        raise


if __name__ == "__main__":
    analyze_failed_messages()
