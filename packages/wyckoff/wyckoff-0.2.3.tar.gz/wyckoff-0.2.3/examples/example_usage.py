#!/usr/bin/env python
# Example script demonstrating how to use the wyckoff package

from wyckoff import WyckoffDatabase
# or import these functions
#from wyckoff import wyckoff_positions, wyckoff_database


def main():
    print("Example usage of the Wyckoff package\n")

    wycoff = WyckoffDatabase()
    data = wycoff.data # or wyckoff_database()
    wyckoff_positions = wycoff.wyckoff_positions #or wyckoff_positions

    available_groups = list(data.keys())
    total_space_groups = len(available_groups)
    print(f"Number of space groups: {total_space_groups} (230 standard + {len(available_groups) - 230} variations)")

    print("\nSpace group 1(unformatted):")
    print(data["1"]) # Type Wyckoff

    print("\nSpace group 1(formatted):")
    print(f"\t{data['1'][0].label}: {data['1'][0].positions}")

    print("\nSpace group 2:")
    for item in data["2"]:
        print(f"\t{item.label}: {item.positions}")

    # space group for 5 is variant 5-b
    for sg in [3, 5]:
        print(f"\nSpace group {sg}:")
        positions = wyckoff_positions(sg)
        for label, position_data in positions.items():
            print(f" \t{label}: {position_data}")

    # print("\nSpace group 48-1:")
    # positions = wyckoff_positions("48-1")
    # for label, position_data in positions.items():
    #     print(f"\t{label}: {position_data}")


    # print("\nSpace group 148-hexagonal:")
    # positions = wyckoff_positions("148-hexagonal") #148
    # for label, position_data in positions.items():
    #     print(f"\t{label}: {position_data}")

    # # Try a non-existent space group
    print("\nNon-existent space group 999:")
    print(wyckoff_positions(999))

if __name__ == "__main__":
    main()
