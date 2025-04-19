import json
import os
from functools import lru_cache
from sympy import simplify, sympify

# Original implementation is included from the package ...
# https://github.com/SMTG-Bham/doped/tree/main
# S. R. Kavanagh et al. doped: Python toolkit for robust and repeatable charged defect supercell calculations. Journal of Open Source Software 9 (96), 6433, 2024
# That version used a non-standard datafile for parsing the Wyckoff positions
# This implementation uses a standard JSON file for parsing the Wyckoff positions
# adds additional checks for redundant Wyckoff positions. Adds functions to return the full database

_WYCKOFF_JSON_DATA = None


@lru_cache(maxsize=int(1e5))
def cached_simplify(eq):
    """
    Cached simplification function for ``sympy`` equations, for efficiency.
    """
    # Ensure input is a sympy object before simplifying
    return simplify(sympify(eq))


def _get_data_file_path(filename):
    """
    Helper function to get the path to a data file in the package.

    Args:
        filename (str): Name of the data file to find

    Returns:
        str: Full path to the data file
    """
    # First check if the file exists in the specified path
    if os.path.isfile(filename):
        return filename

    # Then look in the package's data directory
    package_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(package_dir, 'data', filename)

    if os.path.isfile(data_path):
        return data_path

    # If not found, return the original filename and let the caller handle errors
    return filename


def load_wyckoff_json(json_filename="wyckoff.json"):
    """Loads the Wyckoff data from the JSON file."""
    global _WYCKOFF_JSON_DATA
    if _WYCKOFF_JSON_DATA is None:
        try:
            # Find the data file
            data_path = _get_data_file_path(json_filename)
            with open(data_path, "r") as f:
                _WYCKOFF_JSON_DATA = json.load(f)
        except FileNotFoundError:
            print(f"Error: Wyckoff JSON file '{json_filename}' not found.")
            _WYCKOFF_JSON_DATA = {}  # Set to empty dict to avoid repeated load attempts
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from file '{json_filename}'.")
            _WYCKOFF_JSON_DATA = {}
        except Exception as e:
            print(f"An unexpected error occurred loading '{json_filename}': {e}")
            _WYCKOFF_JSON_DATA = {}
    return _WYCKOFF_JSON_DATA

def wyckoff_database(json_filename="wyckoff.json"):
    """
    Returns the entire Wyckoff position database with processed coordinates.

    This function processes all coordinates into sympy expressions and applies the equivalent
    sites logic for each space group, just like wyckoff_positions() does for a
    single space group.

    Args:
        json_filename (str): Path to the Wyckoff JSON data file.

    Returns:
        dict: A dictionary where keys are space group numbers/settings and values
              are lists of processed Wyckoff position objects. Each Wyckoff position
              object contains 'label', 'letter', 'multiplicity', 'coordinates', and
              'positions' fields. Returns an empty dictionary if loading fails.
    """
    all_wyckoff_data = load_wyckoff_json(json_filename)
    if not all_wyckoff_data:
        return {}

    processed_database = {}
    for spacegroup_key, spacegroup_data in all_wyckoff_data.items():
        processed_positions = _process_space_group_positions(spacegroup_data, spacegroup_key)
        if processed_positions:
            processed_database[spacegroup_key] = processed_positions

    return processed_database


def _coord_string_to_sympy_array(coord_string):
    """
    Converts a coordinate string "(x,y,z)" into a list of
    simplified sympy expressions.
    Handles replacements like '2x' -> '2*x' for sympy compatibility.
    """
    # Remove parentheses and split by comma
    parts = coord_string.strip("()").split(",")
    sympy_expressions = []
    for part in parts:
        try:
            # Replace common patterns like '2x' with '2*x' for sympy
            processed_part = (
                part.replace("2x", "2*x").replace("2y", "2*y").replace("2z", "2*z")
            )
            # Sympify and simplify
            sympy_expressions.append(cached_simplify(processed_part))
        except (SyntaxError, TypeError, Exception) as e:
            print(
                f"Warning: Could not parse coordinate part '{part}' in '{coord_string}'. Error: {e}"
            )
            sympy_expressions.append(part)  # Keep original string on error
    return sympy_expressions


def _is_coord_in_list(coord, coord_list):
    """Check if a coordinate is mathematically equivalent to any in the list."""
    for existing_coord in coord_list:
        if len(coord) != len(existing_coord):
            continue

        # Check if all elements are mathematically equivalent
        all_equal = True
        for c1, c2 in zip(coord, existing_coord):
            # Try to check if c1 - c2 simplifies to 0
            try:
                diff = cached_simplify(c1 - c2)
                if diff != 0:
                    all_equal = False
                    break
            except Exception:
                # If comparison fails, assume they're different
                all_equal = False
                break

        if all_equal:
            return True
    return False


def _process_space_group_positions(spacegroup_data, spacegroup_key):
    """
    Process the Wyckoff positions for a single space group.
    
    Args:
        spacegroup_data (dict): The raw data for a single space group from the JSON.
        spacegroup_key (str): The space group number or label for error messages.
        
    Returns:
        list: A list of processed Wyckoff positions with embedded processed coordinates.
    """
    if spacegroup_data is None:
        return []
    
    # Parse the additional positions (equivalent sites) first
    equivalent_sites_str = spacegroup_data.get("additional_positions", [])
    equivalent_sites_parsed = [
        _coord_string_to_sympy_array(coords) for coords in equivalent_sites_str
    ]

    # List to store all processed Wyckoff positions
    processed_positions = []

    # Iterate through the Wyckoff positions listed in the JSON for this space group
    for wyckoff_info in spacegroup_data.get("wyckoff_positions", []):
        # Create a copy of the wyckoff_info to modify
        processed_wyckoff_info = wyckoff_info.copy()
        
        letter = wyckoff_info.get("letter")
        multiplicity = wyckoff_info.get("multiplicity")
        coordinates_str_list = wyckoff_info.get("coordinates", [])

        if letter is None or multiplicity is None:
            print(
                f"Skipping incomplete Wyckoff entry in space group {spacegroup_key}: {wyckoff_info}"
            )
            continue

        # Create Wyckoff label (e.g., "4d")
        label = str(multiplicity) + letter
        processed_wyckoff_info["label"] = label  # Store label in the processed info

        # Parse the base coordinates for this Wyckoff position
        base_wyckoff_coords = [
            _coord_string_to_sympy_array(coords_str)
            for coords_str in coordinates_str_list
        ]

        # Combine base coordinates with equivalent sites
        combined_coords = []
        if not equivalent_sites_parsed:
            combined_coords = base_wyckoff_coords  # No additional positions
        else:
            for base_coord in base_wyckoff_coords:
                # Start with the base coordinate itself
                combined_coords.append(base_coord)
                # Add combinations with equivalent sites
                for equiv_site in equivalent_sites_parsed:
                    if len(base_coord) == len(equiv_site):  # Ensure dimensions match
                        try:
                            # Perform element-wise addition using sympy objects
                            new_coord = [
                                cached_simplify(b + e)
                                for b, e in zip(base_coord, equiv_site)
                            ]
                            # Only add if this coordinate isn't already in the list
                            if not _is_coord_in_list(new_coord, combined_coords):
                                combined_coords.append(new_coord)
                        except Exception as e:
                            print(
                                f"Warning: Could not combine {base_coord} and {equiv_site}. Error: {e}"
                            )
                    else:
                        print(
                            f"Warning: Dimension mismatch between base coord {base_coord} and equiv site {equiv_site}"
                        )

        # Add the positions to the wyckoff info
        processed_wyckoff_info["positions"] = combined_coords
        
        # Add the processed wyckoff info to the list
        processed_positions.append(processed_wyckoff_info)

    return processed_positions


def _extract_label_positions_dict(processed_positions):
    """
    Helper function to extract a dictionary mapping Wyckoff labels to positions
    from the new processed data structure. This is for backward compatibility.
    
    Args:
        processed_positions (list): List of processed Wyckoff positions from _process_space_group_positions
        
    Returns:
        dict: A dictionary where keys are Wyckoff labels (e.g., "4a")
              and values are lists of coordinate arrays (sympy expressions).
    """
    label_positions_dict = {}
    
    if not processed_positions:
        return {}
        
    for wyckoff_info in processed_positions:
        # Get the label and positions
        letter = wyckoff_info.get("letter")
        multiplicity = wyckoff_info.get("multiplicity")
        positions = wyckoff_info.get("positions", [])
        
        if letter is None or multiplicity is None:
            continue
            
        label = str(multiplicity) + letter  # e.g. 4d
        label_positions_dict[label] = positions
    
    return label_positions_dict


def wyckoff_positions(sgn, json_filename="wyckoff.json"):
    """
    Get dictionary of {Wyckoff label: coordinates} for a given space group
    number (sgn) by reading from a pre-parsed JSON file.

    Args:
        sgn (int or str): The space group number or label (e.g., "15-c").
        json_filename (str): Path to the Wyckoff JSON data file.

    Returns:
        dict: A dictionary where keys are Wyckoff labels (e.g., "4a")
              and values are lists of coordinate arrays (sympy expressions).
              Returns an empty dictionary if the space group is not found
              or an error occurs.
    """
    # Get the database using the wyckoff_database function
    all_wyckoff_data = load_wyckoff_json(json_filename)
    if not all_wyckoff_data:  # Check if loading failed
        return {}

    # Get the data for the specific space group
    spacegroup_key = str(sgn)
    spacegroup_data = all_wyckoff_data.get(spacegroup_key)

    # If exact match not found, try to find variants (e.g., "3-b", "3-c" for input "3")
    if spacegroup_data is None:
        # Try to find a default setting
        if not isinstance(sgn, str) or "-" not in spacegroup_key:
            # Look for variants with this base number
            base_sg_number = spacegroup_key.split("-")[0] if "-" in spacegroup_key else spacegroup_key
            variants = [k for k in all_wyckoff_data.keys() if k.startswith(f"{base_sg_number}-")]

            if variants:
                # Use the first variant as default (usually -b setting)
                spacegroup_key = variants[0]
                spacegroup_data = all_wyckoff_data.get(spacegroup_key)
                print(f"Note: Using space group '{spacegroup_key}' as default setting for space group {base_sg_number}.")
                print(f"Available variants: {', '.join(variants)}")
            else:
                print(f"Warning: Space group '{sgn}' not found in '{json_filename}'.")
                return {}
        else:
            print(f"Warning: Space group '{spacegroup_key}' not found in '{json_filename}'.")
            return {}

    # If we still don't have valid data, return empty dict
    if spacegroup_data is None:
        return {}

    # Process the space group data using our helper function
    processed_data = _process_space_group_positions(spacegroup_data, spacegroup_key)
    
    # Extract the {label: positions} dictionary for backward compatibility
    return _extract_label_positions_dict(processed_data)
