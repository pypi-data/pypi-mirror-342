import json
import os
import time
import functools
from dataclasses import dataclass, field
from typing import List, Dict, Union, Any, Optional, Tuple
from sympy import simplify, sympify

# Original implementation is included from the package ...
# https://github.com/SMTG-Bham/doped/tree/main
# S. R. Kavanagh et al. doped: Python toolkit for robust and repeatable charged defect supercell calculations. Journal of Open Source Software 9 (96), 6433, 2024
# That version used a non-standard datafile for parsing the Wyckoff positions
# This implementation uses a standard JSON file for parsing the Wyckoff positions

def profile_execution(func):
    """Decorator to measure and report execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper


def safe_coord_processing(func):
    """Decorator to safely process coordinate expressions and handle exceptions."""
    @functools.wraps(func)
    def wrapper(part, *args, **kwargs):
        try:
            return func(part, *args, **kwargs)
        except (SyntaxError, TypeError, Exception) as e:
            print(f"Warning: Could not parse coordinate part '{part}'. Error: {e}")
            return part  # Return original string on error
    return wrapper


def validate_wyckoff_info(func):
    """Decorator to validate required Wyckoff position fields."""
    @functools.wraps(func)
    def wrapper(self_or_wyckoff_info, *args, **kwargs):
        # If this is a method, the first arg is self and wyckoff_info is the second arg
        # If this is a function, the first arg is wyckoff_info
        if hasattr(self_or_wyckoff_info, '_process_wyckoff_position'):
            # This is a method call (self is first arg)
            self = self_or_wyckoff_info
            wyckoff_info = args[0]
            spacegroup_key = args[1]
            remaining_args = args[2:]
        else:
            # This is a function call (wyckoff_info is first arg)
            self = None
            wyckoff_info = self_or_wyckoff_info
            spacegroup_key = args[0]
            remaining_args = args[1:]

        letter = wyckoff_info.get("letter")
        multiplicity = wyckoff_info.get("multiplicity")

        if letter is None or multiplicity is None:
            print(f"Skipping incomplete Wyckoff entry in space group {spacegroup_key}: {wyckoff_info}")
            return None

        # Ensure types are correct
        if not isinstance(letter, str) or not isinstance(multiplicity, int):
            try:
                letter = str(letter)
                multiplicity = int(multiplicity)
                # Update the dictionary with converted values
                wyckoff_info["letter"] = letter
                wyckoff_info["multiplicity"] = multiplicity
            except (ValueError, TypeError):
                print(f"Invalid types in Wyckoff entry for space group {spacegroup_key}: {wyckoff_info}")
                return None

        if self is not None:
            # Method call
            return func(self, wyckoff_info, spacegroup_key, *remaining_args, **kwargs)
        else:
            # Function call
            return func(wyckoff_info, spacegroup_key, *remaining_args, **kwargs)
    return wrapper


@dataclass
class Wyckoff:
    """Represents a single Wyckoff position with its properties and coordinates."""
    letter: str
    multiplicity: int
    site_symmetry: str = ""
    coordinates: List[str] = field(default_factory=list)
    positions: List[List[Any]] = field(default_factory=list)
    label: Optional[str] = None

    def __post_init__(self):
        """Calculate the label if not provided."""
        if self.label is None:
            self.label = f"{self.multiplicity}{self.letter}"


# Core functionality

@functools.lru_cache(maxsize=int(1e5))
def cached_simplify(eq):
    """Cached simplification function for ``sympy`` equations, for efficiency."""
    # Ensure input is a sympy object before simplifying
    return simplify(sympify(eq))


class WyckoffDatabase:
    """Class for handling Wyckoff position data with processing capabilities."""

    def __init__(self, json_filename: str = "wyckoff.json"):
        """Initialize the database handler.

        Args:
            json_filename: Path to the JSON file containing Wyckoff positions.
        """
        self.json_filename = json_filename
        self._raw_data = None
        self._processed_data = None

    def _get_data_file_path(self, filename: str) -> str:
        """Helper function to get the path to a data file in the package.

        Args:
            filename: Name of the data file to find

        Returns:
            Full path to the data file
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

    def load_raw_data(self) -> Dict:
        """Load the raw Wyckoff data from the JSON file.

        Returns:
            The raw Wyckoff position data as a dictionary.
        """
        if self._raw_data is None:
            try:
                # Find the data file
                data_path = self._get_data_file_path(self.json_filename)
                with open(data_path, "r") as f:
                    self._raw_data = json.load(f)
            except FileNotFoundError:
                print(f"Error: Wyckoff JSON file '{self.json_filename}' not found.")
                self._raw_data = {}  # Set to empty dict to avoid repeated load attempts
            except json.JSONDecodeError:
                print(f"Error: Could not decode JSON from file '{self.json_filename}'.")
                self._raw_data = {}
            except Exception as e:
                print(f"An unexpected error occurred loading '{self.json_filename}': {e}")
                self._raw_data = {}

        return self._raw_data

    @property
    def data(self) -> Dict[str, List[Wyckoff]]:
        """Get the fully processed Wyckoff database.

        Returns:
            A dictionary mapping space group numbers/settings to lists of
            WyckoffPosition objects with processed coordinates.
        """
        if self._processed_data is None:
            self._processed_data = self._process_database()
        return self._processed_data

    @safe_coord_processing
    def _process_coordinate_part(self, part: str) -> Any:
        """Process a single coordinate part into a sympy expression.

        Args:
            part: String representation of a coordinate part (e.g., 'x', '1-y')

        Returns:
            Simplified sympy expression
        """
        # Replace common patterns like '2x' with '2*x' for sympy
        processed_part = part.replace("2x", "2*x").replace("2y", "2*y").replace("2z", "2*z")
        # Sympify and simplify
        return cached_simplify(processed_part)

    def _coord_string_to_sympy_array(self, coord_string: str) -> List[Any]:
        """Convert a coordinate string to a list of sympy expressions.

        Args:
            coord_string: String like "(x,y,z)" representing coordinates

        Returns:
            List of sympy expressions
        """
        # Remove parentheses and split by comma
        parts = coord_string.strip("()").split(",")
        return [self._process_coordinate_part(part) for part in parts]

    def _is_coord_in_list(self, coord: List[Any], coord_list: List[List[Any]]) -> bool:
        """Check if a coordinate is mathematically equivalent to any in the list.

        Args:
            coord: List of sympy expressions representing a coordinate
            coord_list: List of existing coordinates to check against

        Returns:
            True if an equivalent coordinate exists, False otherwise
        """
        for existing_coord in coord_list:
            if len(coord) != len(existing_coord):
                continue

            # Check if all elements are mathematically equivalent
            all_equal = True
            for c1, c2 in zip(coord, existing_coord):
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

    @validate_wyckoff_info
    def _process_wyckoff_position(self, wyckoff_info: Dict, spacegroup_key: str,
                                 equivalent_sites_parsed: List[List[Any]]) -> Optional[Wyckoff]:
        """Process a single Wyckoff position from the raw data.

        Args:
            wyckoff_info: Dictionary containing raw Wyckoff position data
            spacegroup_key: Space group number/setting for error messages
            equivalent_sites_parsed: List of parsed equivalent sites

        Returns:
            Processed WyckoffPosition object or None if processing fails
        """
        # The decorator already validates letter and multiplicity are not None
        # and converts them to the correct types
        letter = wyckoff_info["letter"]  # Now safe to use direct access
        multiplicity = wyckoff_info["multiplicity"]
        site_symmetry = wyckoff_info.get("site_symmetry", "")
        coordinates_str_list = wyckoff_info.get("coordinates", [])

        # Create Wyckoff position object
        position = Wyckoff(
            letter=letter,
            multiplicity=multiplicity,
            site_symmetry=site_symmetry,
            coordinates=coordinates_str_list
        )

        # Parse the base coordinates for this Wyckoff position
        base_wyckoff_coords = [
            self._coord_string_to_sympy_array(coords_str)
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
                            if not self._is_coord_in_list(new_coord, combined_coords):
                                combined_coords.append(new_coord)
                        except Exception as e:
                            print(
                                f"Warning: Could not combine {base_coord} and {equiv_site}. Error: {e}"
                            )
                    else:
                        print(
                            f"Warning: Dimension mismatch between base coord {base_coord} and equiv site {equiv_site}"
                        )

        # Set the processed positions
        position.positions = combined_coords
        return position

    def _process_space_group(self, spacegroup_data: Dict, spacegroup_key: str) -> List[Wyckoff]:
        """Process all Wyckoff positions for a single space group.

        Args:
            spacegroup_data: Raw data for a space group from the JSON
            spacegroup_key: Space group number/setting

        Returns:
            List of processed WyckoffPosition objects
        """
        if spacegroup_data is None:
            return []

        # Parse the additional positions (equivalent sites) first
        equivalent_sites_str = spacegroup_data.get("additional_positions", [])
        equivalent_sites_parsed = [
            self._coord_string_to_sympy_array(coords) for coords in equivalent_sites_str
        ]

        # Process each Wyckoff position
        positions = []
        for wyckoff_info in spacegroup_data.get("wyckoff_positions", []):
            position = self._process_wyckoff_position(
                wyckoff_info, spacegroup_key, equivalent_sites_parsed
            )
            if position is not None:
                positions.append(position)

        return positions

    def _process_database(self) -> Dict[str, List[Wyckoff]]:
        """Process the entire database of Wyckoff positions.

        Returns:
            Dictionary mapping space group numbers/settings to lists of
            processed WyckoffPosition objects.
        """
        raw_data = self.load_raw_data()
        if not raw_data:
            return {}

        processed_data = {}
        for spacegroup_key, spacegroup_data in raw_data.items():
            processed_positions = self._process_space_group(spacegroup_data, spacegroup_key)
            if processed_positions:
                processed_data[spacegroup_key] = processed_positions

        return processed_data

    def find_space_group_variant(self, sgn: Union[int, str]) -> Tuple[Optional[str], Optional[Dict]]:
        """Find a space group or a suitable variant in the database.

        Args:
            sgn: Space group number or label (e.g., "15-c")

        Returns:
            Tuple of (space group key, space group data) or (None, None) if not found
        """
        raw_data = self.load_raw_data()
        if not raw_data:
            return None, None

        spacegroup_key = str(sgn)
        spacegroup_data = raw_data.get(spacegroup_key)

        # If exact match found, return it
        if spacegroup_data is not None:
            return spacegroup_key, spacegroup_data

        # Try to find a default setting
        if not isinstance(sgn, str) or "-" not in spacegroup_key:
            # Look for variants with this base number
            base_sg_number = spacegroup_key.split("-")[0] if "-" in spacegroup_key else spacegroup_key
            variants = [k for k in raw_data.keys() if k.startswith(f"{base_sg_number}-")]

            if variants:
                # Use the first variant as default (usually -b setting)
                spacegroup_key = variants[0]
                spacegroup_data = raw_data.get(spacegroup_key)
                # print(f"Note: Using space group '{spacegroup_key}' as default setting for space group {base_sg_number}.")
                # print(f"Available variants: {', '.join(variants)}")
                return spacegroup_key, spacegroup_data
            else:
                print(f"Warning: Space group '{sgn}' not found.")
        else:
            print(f"Warning: Space group '{spacegroup_key}' not found.")

        return None, None

    def wyckoff_positions(self, sgn: Union[int, str]) -> Dict[str, List[List[Any]]]:
        """Get dictionary of {Wyckoff label: coordinates} for a given space group.

        Args:
            sgn: Space group number or label (e.g., "15-c")

        Returns:
            Dictionary mapping Wyckoff labels to lists of coordinate arrays
        """
        # Try to find the space group in the processed data
        spacegroup_key = str(sgn)
        if spacegroup_key in self.data:
            positions = self.data[spacegroup_key]
            # Ensure we only include positions with valid labels
            return {pos.label: pos.positions for pos in positions if pos.label is not None}

        # If not found in processed data, try to find a variant
        sg_key, sg_data = self.find_space_group_variant(sgn)
        if sg_key is None or sg_data is None:
            return {}

        # Process the space group and extract positions
        positions = self._process_space_group(sg_data, sg_key)
        # Ensure we only include positions with valid labels
        return {pos.label: pos.positions for pos in positions if pos.label is not None}


# Public API functions

_wyckoff_db_instance = None

def get_wyckoff_database(json_filename: str = "wyckoff.json") -> WyckoffDatabase:
    """Get a singleton instance of the WyckoffDatabase.

    Args:
        json_filename: Path to the JSON file containing Wyckoff positions

    Returns:
        WyckoffDatabase instance
    """
    global _wyckoff_db_instance
    if _wyckoff_db_instance is None or _wyckoff_db_instance.json_filename != json_filename:
        _wyckoff_db_instance = WyckoffDatabase(json_filename)
    return _wyckoff_db_instance


def wyckoff_database(json_filename: str = "wyckoff.json") -> Dict[str, List[Wyckoff]]:
    """Get the fully processed Wyckoff position database.

    Args:
        json_filename: Path to the JSON file containing Wyckoff positions

    Returns:
        Dictionary mapping space group numbers/settings to lists of
        WyckoffPosition objects with processed coordinates
    """
    db = get_wyckoff_database(json_filename)
    return db.data


def wyckoff_positions(sgn: Union[int, str], json_filename: str = "wyckoff.json") -> Dict[str, List[List[Any]]]:
    """Get dictionary of {Wyckoff label: coordinates} for a given space group.

    Args:
        sgn: Space group number or label (e.g., "15-c")
        json_filename: Path to the JSON file containing Wyckoff positions

    Returns:
        Dictionary mapping Wyckoff labels to lists of coordinate arrays
    """
    db = get_wyckoff_database(json_filename)
    return db.wyckoff_positions(sgn)
