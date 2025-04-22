import math
import yaml
import json
from pathlib import Path
from typing import List, Dict, Any
from collections import Counter
import concurrent.futures
import mmap
import os
from tqdm import tqdm
import queue
import threading
from datetime import datetime

# Import des fonctions depuis le module original
from analyze_n2k import (
    load_pgn_config,
    get_pgn_config,
    calculate_bit_position,
    decode_field,
    decode_pgn,
    decode_arbitrary_id,
    analyze_n2k
)

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
    try:
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
    except Exception as e:
        print(f"Erreur de parsing: {str(e)}")
        return None

def process_frame(frame: Dict[str, Any]) -> tuple:
    """
    Traite une trame CAN avec analyse complète
    
    Args:
        frame (dict): Trame CAN parsée
        
    Returns:
        tuple: (result, missed)
    """
    if frame is None:
        return None, None
        
    try:
        result, missed = analyze_n2k(frame['arbitrary_id'], frame['data'])
        return result, missed
    except Exception as e:
        print(f"Erreur d'analyse: {str(e)}")
        return None, None

def process_chunk(chunk: list, results: list, pgn_stats: Counter, pgns_missed: set):
    """
    Traite un chunk de trames avec analyse complète
    
    Args:
        chunk (list): Liste de lignes à traiter
        results (list): Liste pour stocker les résultats détaillés
        pgn_stats (Counter): Compteur de statistiques
        pgns_missed (set): Ensemble des PGNs manquants
    """
    for line in chunk:
        frame = parse_can_line(line)
        if frame:
            result, missed = process_frame(frame)
            if result:
                result['interface'] = frame['interface']
                result['length'] = frame['length']
                results.append(result)
                pgn = result['pgn']
                pgn_stats[pgn] += 1
            if missed and 'pgn' in missed:
                pgn = missed['pgn']
                pgns_missed.add(pgn)
                pgn_stats[pgn] += 1

def analyze_concatenated_log(file_path: str, num_threads: int = None) -> tuple:
    """
    Analyse un fichier de log concaténé en utilisant le multithreading
    
    Args:
        file_path (str): Chemin du fichier
        num_threads (int): Nombre de threads à utiliser (défaut: nombre de cœurs)
        
    Returns:
        tuple: (results, pgn_stats, pgns_missed)
    """
    if num_threads is None:
        num_threads = os.cpu_count()
    
    # Initialisation des compteurs
    all_results = []
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
        results = []
        pgn_stats = Counter()
        pgns_missed = set()
        
        while True:
            chunk = line_queue.get()
            if chunk is None:
                break
            process_chunk(chunk, results, pgn_stats, pgns_missed)
            line_queue.task_done()
        
        return results, pgn_stats, pgns_missed
    
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
            results, pgn_stats, pgns_missed = future.result()
            all_results.extend(results)
            all_pgn_stats.update(pgn_stats)
            all_pgns_missed.update(pgns_missed)
    
    # Attente de la fin du thread de lecture
    reader_thread.join()
    
    return all_results, all_pgn_stats, all_pgns_missed

def save_results(results: List[Dict], pgn_stats: Counter, pgns_missed: set, output_dir: str):
    """
    Sauvegarde les résultats de l'analyse dans des fichiers JSON
    
    Args:
        results (List[Dict]): Liste des résultats d'analyse
        pgn_stats (Counter): Statistiques des PGNs
        pgns_missed (set): Ensemble des PGNs manquants
        output_dir (str): Répertoire de sortie
    """
    # Création du répertoire de sortie
    os.makedirs(output_dir, exist_ok=True)
    
    # Timestamp pour les noms de fichiers
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Sauvegarde des résultats détaillés
    results_file = os.path.join(output_dir, f"results_{timestamp}.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nRésultats détaillés sauvegardés dans {results_file}")
    
    # Sauvegarde des statistiques
    stats = {
        "pgn_stats": dict(pgn_stats),
        "pgns_missed": list(pgns_missed)
    }
    stats_file = os.path.join(output_dir, f"stats_{timestamp}.json")
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
    print(f"Statistiques sauvegardées dans {stats_file}")

if __name__ == "__main__":
    # Chemins des fichiers
    input_file = "/data/can/concatenated/all_logs.log"
    output_dir = "/data/can/analysis_results"
    
    if not os.path.exists(input_file):
        print(f"Le fichier {input_file} n'existe pas")
        exit(1)
    
    # Analyse avec multithreading
    results, pgn_stats, pgns_missed = analyze_concatenated_log(input_file)
    
    # Affichage des statistiques
    print(f"\nNombre total de trames analysées: {len(results)}")
    print("\nStatistiques globales des PGNs:")
    for pgn, count in sorted(pgn_stats.items()):
        print(f"{pgn}\t{count}")
    
    if pgns_missed:
        print("\nPGNs manquants (non configurés):")
        for pgn in sorted(pgns_missed):
            print(f"{pgn}\t{pgn_stats.get(pgn, 0)}")
    
    # Sauvegarde des résultats
    save_results(results, pgn_stats, pgns_missed, output_dir) 