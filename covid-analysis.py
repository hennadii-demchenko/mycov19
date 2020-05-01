from fetch import retrieve_axises
from plot import plot_data


if __name__ == "__main__":
    import argparse
    import pycountry

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--country', type=str, help='report by country')
    group.add_argument('--code', type=str, help='report by country code')

    args = parser.parse_args()

    if args.code is None:
        country = args.country.capitalize()
        code = pycountry.countries.get(name=country).alpha_2
    else:
        code = args.code
        country = pycountry.countries.get(alpha_2=args.code).name

    data = retrieve_axises(code)

    print(f"Analysing {country} data")
    plot_data(country, data)
