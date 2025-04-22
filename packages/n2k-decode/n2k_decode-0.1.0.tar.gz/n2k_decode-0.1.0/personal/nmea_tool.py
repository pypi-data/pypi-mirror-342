import json
import re
from typing import Dict, List, Optional
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class PGNField:
    def __init__(self, name: str, resolution: str, size: str):
        self.name = name
        self.resolution = resolution
        self.size = size

    def to_dict(self) -> Dict:
        return {"name": self.name, "resolution": self.resolution, "size": self.size}


class PGN:
    def __init__(self, number: int, name: str, fields: List[PGNField]):
        self.number = number
        self.name = name
        self.fields = fields

    def to_dict(self) -> Dict:
        return {
            "number": self.number,
            "name": self.name,
            "fields": [field.to_dict() for field in self.fields],
        }


def parse_pgn_line(line: str) -> Optional[PGNField]:
    """Parse une ligne de définition de champ PGN."""
    # Pattern pour extraire le nom, la résolution et la taille
    pattern = r"\| (\d+)\s+\| ([^|]+)\s+\| ([^|]+)\s+\| ([^|]+)\s+\|"
    match = re.search(pattern, line)

    if match:
        _, name, resolution, size = match.groups()
        return PGNField(
            name=name.strip(), resolution=resolution.strip(), size=size.strip()
        )
    return None


def parse_pgn_section(lines: List[str]) -> Optional[PGN]:
    """Parse une section complète de PGN."""
    if not lines:
        return None

    # Pattern pour extraire le numéro et le nom du PGN
    header_pattern = r"## (\d+)\s+([^\n]+)"
    header_match = re.search(header_pattern, lines[0])

    if not header_match:
        return None

    pgn_number = int(header_match.group(1))
    pgn_name = header_match.group(2).strip()

    fields = []
    for line in lines[1:]:
        field = parse_pgn_line(line)
        if field:
            fields.append(field)

    return PGN(pgn_number, pgn_name, fields)


def parse_canboat_documentation(content: str) -> List[PGN]:
    """Parse le contenu de la documentation CANBoat."""
    pgns = []
    current_section = []

    for line in content.split("\n"):
        if line.startswith("## "):
            if current_section:
                pgn = parse_pgn_section(current_section)
                if pgn:
                    pgns.append(pgn)
            current_section = [line]
        elif current_section:
            current_section.append(line)

    # Traiter la dernière section
    if current_section:
        pgn = parse_pgn_section(current_section)
        if pgn:
            pgns.append(pgn)

    return pgns


def save_pgns_to_json(pgns: List[PGN], output_file: str):
    """Sauvegarde les PGNs dans un fichier JSON."""
    pgn_dicts = [pgn.to_dict() for pgn in pgns]
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(pgn_dicts, f, indent=2, ensure_ascii=False)
    logger.info(f"PGNs sauvegardés dans {output_file}")


def main():
    try:
        # Lire le contenu de la documentation
        with open("canboat_documentation.html", "r", encoding="utf-8") as f:
            content = f.read()

        # Parser les PGNs
        pgns = parse_canboat_documentation(content)
        logger.info(f"Nombre de PGNs trouvés: {len(pgns)}")

        # Sauvegarder en JSON
        save_pgns_to_json(pgns, "nmea_pgns.json")

    except Exception as e:
        logger.error(f"Erreur lors du traitement: {str(e)}")


if __name__ == "__main__":
    main()
