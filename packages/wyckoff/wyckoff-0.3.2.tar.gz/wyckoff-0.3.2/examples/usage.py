#!/usr/bin/env python
# Example script demonstrating how to use the wyckoff package

from wyckoff import WyckoffDatabase

def main():
    print("Example usage of the Wyckoff package\n")

    wycoff = WyckoffDatabase()
    data = wycoff.data

    available_groups = list(data.keys())
    total_space_groups = len(available_groups)
    print(f"Number of space groups: {total_space_groups} (230 standard + {len(available_groups) - 230} variations)")

    print("\nSpace group 1:")
    print(data["1"])

    print("\nSpace group 1:")
    print(f"\t{data['1'].wyckoff_positions[0].label}: {data['1'].wyckoff_positions[0].positions}")

    print("\nSpace group 5:")
    print(data["5"])

    print("\nSpace group 3 first label:")
    print(data["3"].wyckoff_positions[0].label)

    print("\nNon-existent space group 999:")
    print(data["999"])

    # def wyckoff_positions(sgn):
    #     try:
    #         space_group = data[str(sgn)]
    #         return {item.label: item.positions for item in space_group.wyckoff_positions if item.label is not None}
    #     except KeyError:
    #         return {}

    # print("\nSpace group 48-1:")
    # positions = wyckoff_positions("48-1")
    # for label, position_data in positions.items():
    #     print(f"\t{label}: {position_data}")


    # print("\nSpace group 148-hexagonal:")
    # positions = wyckoff_positions("148-hexagonal") #148
    # for label, position_data in positions.items():
    #     print(f"\t{label}: {position_data}")

if __name__ == "__main__":
    main()
