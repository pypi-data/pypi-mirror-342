import math
import yaml
from pathlib import Path
from typing import List, Dict, Any
from collections import Counter
import concurrent.futures
import glob
import multiprocessing
import mmap
import os
from tqdm import tqdm
import queue
import threading


def load_pgn_config():
    """Charge la configuration des PGNs depuis le fichier YAML"""
    config_path = Path(__file__).parent / "pgn_config.yaml"
    with open(config_path, "r") as f:
        # Convertit les clés numériques en chaînes de caractères
        config = yaml.safe_load(f)
        return {str(k): v for k, v in config.items()}


def get_pgn_config(pgn_configs: dict, pgn: str) -> dict:
    """
    Récupère la configuration d'un PGN spécifique

    Args:
        pgn_configs (dict): Configuration complète
        pgn (str): Numéro du PGN

    Returns:
        dict: Configuration du PGN
    """
    if pgn not in pgn_configs:
        return None

    config = pgn_configs[pgn]
    # Convertit la structure plate en liste de champs
    fields = []
    for field_name, field_config in config['fields'].items():
        field_config["name"] = field_name
        fields.append(field_config)
    config["fields"] = fields
    return config


def calculate_bit_position(fields: list, field_index: int) -> int:
    """
    Calcule la position du bit pour un champ donné en fonction de sa position dans la liste

    Args:
        fields (list): Liste des champs
        field_index (int): Index du champ dans la liste

    Returns:
        int: Position du bit (0-63)
    """
    # On part de la fin (bit 63) et on soustrait la longueur des champs précédents
    total_length = sum(f["length"] for f in fields[:field_index + 1])
    return 64 - total_length


def decode_field(data: int, field_config: dict, bit_position: int) -> float:
    """
    Décode un champ selon sa configuration

    Args:
        data (int): Données brutes de la trame
        field_config (dict): Configuration du champ
        bit_position (int): Position du bit dans la trame

    Returns:
        float: Valeur décodée du champ
    """
    # Extraction des bits
    value = (data >> bit_position) & ((1 << field_config["length"]) - 1)
    
    # Gestion des valeurs signées
    if field_config.get("signed", False):
        # Si le bit de poids fort est 1, la valeur est négative
        if value & (1 << (field_config["length"] - 1)):
            # Complément à 2
            value = value - (1 << field_config["length"])
    
    # Conversion selon le type
    if field_config["type"] == "float":
        value = value * field_config.get("ratio", 1)
    
    return value


def decode_pgn(data: int, pgn_config: dict) -> dict:
    """
    Décode une trame N2K selon la configuration du PGN

    Args:
        data (int): Données brutes de la trame
        pgn_config (dict): Configuration du PGN

    Returns:
        dict: Dictionnaire contenant les champs décodés
    """
    result = {}
    for i, field in enumerate(pgn_config["fields"]):
        # print(i, field)
        bit_position = calculate_bit_position(pgn_config["fields"], i)
        result[field["name"]] = decode_field(data, field, bit_position)
    return result


# # # # # # # # # # # # # # # # # # # # #
# FONCTONS GLOBAlES
# # # # # # # # # # # # # # # # # # # # #


def decode_arbitrary_id(arbitrary_id: int) -> dict:
    """
    Décode l'ID arbitraire d'une trame N2K pour extraire les informations de base.

    Args:
        arbitrary_id (int): L'ID arbitraire de la trame N2K (29 bits)

    Returns:
        dict: Dictionnaire contenant:
            - priority (int): Priorité du message (0-7)
            - source_address (int): Adresse source (0-255)
            - pgn (int): Parameter Group Number
    """
    # Les 3 bits de poids fort sont la priorité
    priority = (arbitrary_id >> 26) & 0x3

    # Les bits restants (18 bits) forment le PGN
    pgn = (arbitrary_id >> 8) & 0x3FFFF

    # Les 8 bits de poids faible sont l'adresse source
    source_address = arbitrary_id & 0xFF

    return {
        "pgn": pgn,
        "priority": priority,
        "source_address": source_address,
    }


def analyze_n2k(arbitrary_id: int, data: int) -> List[dict]:
    """
    Analyse une trame N2K complète

    Args:
        arbitrary_id (int): ID arbitraire de la trame
        data (int): Données brutes de la trame

    Returns:
        dict: Résultat de l'analyse
    """
    # Décodage des métadonnées
    meta_infos = decode_arbitrary_id(arbitrary_id)

    # Chargement de la configuration
    pgn_configs = load_pgn_config()


    # Récupération de la configuration du PGN
    pgn_config = get_pgn_config(pgn_configs, str(meta_infos["pgn"]))
    if pgn_config is None:
        # print(f"Pas de configuration définie pour le PGN {meta_infos['pgn']}")
        return {}, {'pgn':meta_infos['pgn']}

    return {
        **meta_infos,
        "name": pgn_config["name"],
        # "data": decode_pgn(data, pgn_config),
    }, {'pgn':meta_infos['pgn']}


def parse_can_line(line: str) -> Dict[str, Any]:
    """
    Parse une ligne de log CAN au format :
    can0  09F1120A   [8]  00 68 A8 FF 7F 14 00 FD
    
    Args:
        line (str): Ligne à parser
        
    Returns:
        dict: Dictionnaire contenant :
            - interface (str): Interface CAN (ex: "can0")
            - arbitrary_id (int): ID arbitraire en hexadécimal
            - length (int): Longueur des données
            - data (int): Données en hexadécimal
    """
    parts = line.strip().split()
    if len(parts) < 4:
        return None
        
    interface = parts[0]
    arbitrary_id = int(parts[1], 16)
    length = int(parts[2].strip('[]'))
    
    # Convertit les octets en un entier
    data_bytes = [int(x, 16) for x in parts[3:3+length]]
    data = 0
    for byte in data_bytes:
        data = (data << 8) | byte
    
    return {
        'interface': interface,
        'arbitrary_id': arbitrary_id,
        'length': length,
        'data': data
    }


def read_can_log(file_path: str) -> List[Dict[str, Any]]:
    """
    Lit un fichier de log CAN et retourne les trames parsées
    
    Args:
        file_path (str): Chemin du fichier
        
    Returns:
        list: Liste des trames parsées
    """
    frames = []
    with open(file_path, 'r') as f:
        for line in f:
            frame = parse_can_line(line)
            if frame:
                frames.append(frame)
    return frames


def analyze_can_log(file_path: str) -> List[Dict[str, Any]]:
    """
    Analyse un fichier de log CAN et retourne les trames décodées
    
    Args:
        file_path (str): Chemin du fichier
        
    Returns:
        list: Liste des trames décodées
    """
    frames = read_can_log(file_path)
    results = []
    pgn_missed = []
    pgn_stats = {}  # Statistiques des PGNs
    
    for frame in frames:
        result, missed = analyze_n2k(frame['arbitrary_id'], frame['data'])
        # if result:
        #     result['interface'] = frame['interface']
        #     result['length'] = frame['length']
        #     results.append(result)
        #     # Mise à jour des statistiques pour les PGNs décodés
        #     pgn = result['pgn']
        #     pgn_stats[pgn] = pgn_stats.get(pgn, 0) + 1
        if 'pgn' in missed:
            pgn = missed['pgn']
            pgn_missed.append(pgn)
            # Mise à jour des statistiques pour les PGNs manquants
            pgn_stats[pgn] = pgn_stats.get(pgn, 0) + 1
    
    return results, pgn_missed, pgn_stats


def process_file(file_path: str) -> tuple:
    """
    Traite un fichier de log CAN et retourne les statistiques
    
    Args:
        file_path (str): Chemin du fichier à analyser
        
    Returns:
        tuple: (pgn_stats, pgns_missed)
    """
    pgn_stats = Counter()
    pgns_missed = set()
    
    try:
        # Vérification de la taille du fichier
        if os.path.getsize(file_path) == 0:
            return dict(pgn_stats), pgns_missed
            
        # Utilisation de mmap pour une lecture plus efficace
        with open(file_path, 'r') as f:
            # Lecture directe si le fichier est petit
            if os.path.getsize(file_path) < 1024 * 1024:  # 1MB
                for line in f:
                    try:
                        parts = line.strip().split()
                        if len(parts) < 4:
                            continue
                            
                        arbitrary_id = int(parts[1], 16)
                        pgn = (arbitrary_id >> 8) & 0x3FFFF
                        
                        pgn_stats[pgn] += 1
                        
                        if str(pgn) not in load_pgn_config():
                            pgns_missed.add(pgn)
                            
                    except Exception:
                        continue
            else:
                # Utilisation de mmap pour les grands fichiers
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    for line in iter(mm.readline, b''):
                        try:
                            parts = line.decode('utf-8').strip().split()
                            if len(parts) < 4:
                                continue
                                
                            arbitrary_id = int(parts[1], 16)
                            pgn = (arbitrary_id >> 8) & 0x3FFFF
                            
                            pgn_stats[pgn] += 1
                            
                            if str(pgn) not in load_pgn_config():
                                pgns_missed.add(pgn)
                                
                        except Exception:
                            continue
    except Exception as e:
        print(f"\nErreur lors du traitement de {file_path}: {str(e)}")
    
    return dict(pgn_stats), pgns_missed


def process_frame(line: str, pgn_configs: dict) -> tuple:
    """
    Traite une trame CAN et retourne les statistiques
    
    Args:
        line (str): Ligne du fichier de log
        pgn_configs (dict): Configuration des PGNs
        
    Returns:
        tuple: (pgn, is_missing)
    """
    try:
        parts = line.strip().split()
        if len(parts) < 4:
            return None, False
            
        arbitrary_id = int(parts[1], 16)
        pgn = (arbitrary_id >> 8) & 0x3FFFF
        
        # Vérification si le PGN est configuré
        is_missing = str(pgn) not in pgn_configs
        
        return pgn, is_missing
    except Exception:
        return None, False


def process_chunk(chunk: list, pgn_configs: dict, pgn_stats: Counter, pgns_missed: set):
    """
    Traite un chunk de trames
    
    Args:
        chunk (list): Liste de lignes à traiter
        pgn_configs (dict): Configuration des PGNs
        pgn_stats (Counter): Compteur de statistiques
        pgns_missed (set): Ensemble des PGNs manquants
    """
    for line in chunk:
        pgn, is_missing = process_frame(line, pgn_configs)
        if pgn is not None:
            pgn_stats[pgn] += 1
            if is_missing:
                pgns_missed.add(pgn)


def analyze_concatenated_log(file_path: str, num_threads: int = None) -> tuple:
    """
    Analyse un fichier de log concaténé en utilisant le multithreading
    
    Args:
        file_path (str): Chemin du fichier
        num_threads (int): Nombre de threads à utiliser (défaut: nombre de cœurs)
        
    Returns:
        tuple: (pgn_stats, pgns_missed)
    """
    if num_threads is None:
        num_threads = os.cpu_count()
    
    # Chargement de la configuration des PGNs
    pgn_configs = load_pgn_config()
    
    # Initialisation des compteurs
    all_pgn_stats = Counter()
    all_pgns_missed = set()
    
    # File pour stocker les chunks de lignes
    line_queue = queue.Queue(maxsize=num_threads * 2)
    
    # Fonction pour le thread de lecture
    def read_file():
        try:
            with open(file_path, 'r') as f:
                chunk = []
                for line in f:
                    chunk.append(line)
                    if len(chunk) >= 1000:  # Taille du chunk
                        line_queue.put(chunk)
                        chunk = []
                if chunk:  # Dernier chunk
                    line_queue.put(chunk)
        except Exception as e:
            print(f"Erreur de lecture: {str(e)}")
        finally:
            # Signal de fin pour les threads de traitement
            for _ in range(num_threads):
                line_queue.put(None)
    
    # Fonction pour les threads de traitement
    def process_thread():
        pgn_stats = Counter()
        pgns_missed = set()
        
        while True:
            chunk = line_queue.get()
            if chunk is None:
                break
            process_chunk(chunk, pgn_configs, pgn_stats, pgns_missed)
            line_queue.task_done()
        
        return pgn_stats, pgns_missed
    
    # Lancement des threads
    print(f"Analyse du fichier avec {num_threads} threads...")
    
    # Thread de lecture
    reader_thread = threading.Thread(target=read_file)
    reader_thread.start()
    
    # Threads de traitement
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process_thread) for _ in range(num_threads)]
        
        # Récupération des résultats
        for future in tqdm(concurrent.futures.as_completed(futures), 
                         total=num_threads,
                         desc="Traitement des trames"):
            pgn_stats, pgns_missed = future.result()
            all_pgn_stats.update(pgn_stats)
            all_pgns_missed.update(pgns_missed)
    
    # Attente de la fin du thread de lecture
    reader_thread.join()
    
    return all_pgn_stats, all_pgns_missed


if __name__ == "__main__":
    # Analyse du fichier concaténé
    file_path = "/data/can/concatenated/all_logs.log"
    
    if not os.path.exists(file_path):
        print(f"Le fichier {file_path} n'existe pas")
        exit(1)
    
    # Analyse avec multithreading
    pgn_stats, pgns_missed = analyze_concatenated_log(file_path)
    
    # Affichage des statistiques
    print("\nStatistiques globales des PGNs:")
    for pgn, count in sorted(pgn_stats.items()):
        print(f"{pgn}\t{count}")
    
    if pgns_missed:
        print("\nPGNs manquants (non configurés):")
        for pgn in sorted(pgns_missed):
            print(f"{pgn}\t{pgn_stats.get(pgn, 0)}")