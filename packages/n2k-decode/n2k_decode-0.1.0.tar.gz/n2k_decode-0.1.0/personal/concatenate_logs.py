import glob
import os
from datetime import datetime
from pathlib import Path
from tqdm import tqdm

def extract_date_from_filename(filename):
    """Extrait la date du nom de fichier au format YYYYMMDD_HHMMSS"""
    try:
        # Format attendu: can_YYYYMMDD_HHMMSS.log
        date_str = filename.split('_')[1] + '_' + filename.split('_')[2].split('.')[0]
        return datetime.strptime(date_str, '%Y%m%d_%H%M%S')
    except:
        return None

def concatenate_logs(input_dir, output_file):
    """
    Concatène tous les fichiers de log dans l'ordre chronologique
    
    Args:
        input_dir (str): Répertoire contenant les fichiers de log
        output_file (str): Fichier de sortie
    """
    # Récupération de tous les fichiers .log
    files = glob.glob(os.path.join(input_dir, "*.log"))
    
    # Tri des fichiers par date
    files_with_dates = []
    for file in files:
        date = extract_date_from_filename(os.path.basename(file))
        if date:
            files_with_dates.append((date, file))
    
    # Tri par date
    files_with_dates.sort(key=lambda x: x[0])
    
    print(f"Concaténation de {len(files_with_dates)} fichiers...")
    
    # Création du répertoire de sortie si nécessaire
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # Concaténation des fichiers
    with open(output_file, 'w') as outfile:
        for date, file in tqdm(files_with_dates, desc="Concaténation"):
            try:
                with open(file, 'r') as infile:
                    # Copie du contenu
                    for line in infile:
                        outfile.write(line)
            except Exception as e:
                print(f"\nErreur lors de la lecture de {file}: {str(e)}")

if __name__ == "__main__":
    # Chemins des fichiers
    input_dir = "/data/can/raw"
    output_file = "/data/can/concatenated/all_logs.log"
    
    # Concaténation
    concatenate_logs(input_dir, output_file)
    print(f"\nConcaténation terminée. Fichier de sortie: {output_file}") 