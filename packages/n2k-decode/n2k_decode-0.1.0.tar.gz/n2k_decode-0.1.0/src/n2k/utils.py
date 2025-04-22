def get_arbitrary_information(arbitrary_id: int) -> dict:
    """
    Get the arbitrary information from an arbitrary ID.
    """
    # Decode the arbitrary ID
    pgn = (arbitrary_id >> 8) & 0x3FFFF
    source_address = arbitrary_id & 0xFF
    priority = (arbitrary_id >> 26) & 0x3

    return {
        "pgn": pgn,
        "source_address": source_address,
        "priority": priority,
    }

def get_data(data: int, pgn: int) -> dict:
    """
    Get the data from a CAN frame.
    """
    return {}

def analyze(arbitrary_id: int, data: int) -> dict:
    """
    Analyze a CAN frame and return a dictionary with the analysis results.
    Args:
        arbitrary_id (int): The arbitrary ID of the CAN frame.
        data (int): The data of the CAN frame.

    Returns:
        dict: A dictionary with the analysis results.
    """
    # Decode the arbitrary ID
    arbitrary_information = get_arbitrary_information(arbitrary_id)

    # Decode the data
    data = get_data(data, arbitrary_information["pgn"])

    return {
        **arbitrary_information,
        "data": data,
    }

