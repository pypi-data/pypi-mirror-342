#!/usr/bin/env python3
"""
Example script demonstrating the usage of the n2k module.
"""
import os

from n2k.main import main
from n2k import logger

def load_can_files(can_path):
    """
    Load the CAN files from the given path.
    """
    return os.listdir(can_path)

def concatenate_can_files(can_files):
    """
    Read files and Concatenate lines.
    """
    # Sort files by name
    can_files.sort()

    # Read files and concatenate lines
    with open(can_files[0], "r") as file:
        lines = file.readlines()
    for file in can_files[1:]:
        with open(file, "r") as file:
            lines.extend(file.readlines())
    return lines

def process_can_files(concatenated_can_files):
    """
    Process the concatenated CAN files.
    """
    return main(concatenated_can_files)



def run_example():
    """
    Run the example script.
    """

    can_path = os.getenv("CAN_PATH", "")
    if not can_path:
        logger.error("CAN_PATH environment variable not set")
        return

    # Step 1 : Load files
    logger.info("Loading files")
    can_files = load_can_files(can_path)

    # Step 2 : Concatenate files
    logger.info("Concatenating files")
    concatenated_can_files = concatenate_can_files(can_files)

    # Step 3 : Process files
    logger.info("Processing files")
    json_result = process_can_files(concatenated_can_files)

    # Step 4 : Save result
    logger.info("Saving result")
    save_result(json_result)

if __name__ == "__main__":
    run_example() 