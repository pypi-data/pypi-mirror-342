#!/usr/bin/env python
# Example script demonstrating how to use the wyckoff package

from wyckoff import wyckoff_positions, wyckoff_database


def main():
    print("Example usage of the Wyckoff package\n")

    # Get the entire database
    print("Loading the entire Wyckoff database...")
    database = wyckoff_database()
    available_groups = list(database.keys())
    total_space_groups = len(available_groups)
    print(f"number of space groups: {total_space_groups} (230 standard + ({len(available_groups) - 230}) variations)")
    print(f"Available space groups: {available_groups}\n")

    # Get Wyckoff positions for specific space groups
    for sg in [1, 2, 5]:
        print(f"\nSpace group {sg}:")
        positions = wyckoff_positions(sg)
        for label, position_data in positions.items():
            print(f"  {label}: {position_data}")

    positions_148 = wyckoff_positions(148)
    for label, position_data in positions_148.items():
        print(f"  {label}: {position_data}")

    # Try a non-existent space group
    print("\nNon-existent space group 999:")
    print(wyckoff_positions(999))

if __name__ == "__main__":
    main()
