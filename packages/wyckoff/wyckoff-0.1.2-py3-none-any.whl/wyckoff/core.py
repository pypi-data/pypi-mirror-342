import json
import os
from functools import lru_cache
from sympy import simplify, sympify

# Original implementation is included from the package ...
# https://github.com/SMTG-Bham/doped/tree/main
# S. R. Kavanagh et al. doped: Python toolkit for robust and repeatable charged defect supercell calculations. Journal of Open Source Software 9 (96), 6433, 2024
# That version used a non-standard datafile for parsing the Wyckoff positions
# This implementation uses a standard JSON file for parsing the Wyckoff positions

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
    Returns the entire Wyckoff position database loaded from the JSON file.

    Args:
        json_filename (str): Path to the Wyckoff JSON data file.

    Returns:
        dict: The complete database of Wyckoff positions for all space groups.
              Returns an empty dictionary if loading fails.
    """
    return load_wyckoff_json(json_filename)


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
    all_wyckoff_data = wyckoff_database(json_filename)
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

    wyckoff_label_coords_dict = {}

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
                # Add more replacements if needed (e.g., 3x, 4x...)
                processed_part = (
                    processed_part.replace("3x", "3*x")
                    .replace("3y", "3*y")
                    .replace("3z", "3*z")
                )
                processed_part = (
                    processed_part.replace("4x", "4*x")
                    .replace("4y", "4*y")
                    .replace("4z", "4*z")
                )
                # Sympify and simplify
                sympy_expressions.append(cached_simplify(processed_part))
            except (SyntaxError, TypeError, Exception) as e:
                print(
                    f"Warning: Could not parse coordinate part '{part}' in '{coord_string}'. Error: {e}"
                )
                sympy_expressions.append(part)  # Keep original string on error
        return sympy_expressions

    # Parse the additional positions (equivalent sites) first
    equivalent_sites_str = spacegroup_data.get("additional_positions", [])
    equivalent_sites_parsed = [
        _coord_string_to_sympy_array(coords) for coords in equivalent_sites_str
    ]

    # Iterate through the Wyckoff positions listed in the JSON for this space group
    for wyckoff_info in spacegroup_data.get("wyckoff_positions", []):
        letter = wyckoff_info.get("letter")
        multiplicity = wyckoff_info.get("multiplicity")
        coordinates_str_list = wyckoff_info.get("coordinates", [])

        if letter is None or multiplicity is None:
            print(
                f"Skipping incomplete Wyckoff entry in space group {spacegroup_key}: {wyckoff_info}"
            )
            continue

        label = str(multiplicity) + letter  # e.g. 4d

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
                            combined_coords.append(new_coord)
                        except Exception as e:
                            print(
                                f"Warning: Could not combine {base_coord} and {equiv_site}. Error: {e}"
                            )
                    else:
                        print(
                            f"Warning: Dimension mismatch between base coord {base_coord} and equiv site {equiv_site}"
                        )

        wyckoff_label_coords_dict[label] = combined_coords

    return wyckoff_label_coords_dict
