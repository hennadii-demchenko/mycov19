from base import DEFAULT_COUNTRY
from fetch import retrieve_axises
from plot import plot_data


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--country',
                        type=str, default=DEFAULT_COUNTRY,
                        help='report by country')
    args = parser.parse_args()

    data = retrieve_axises(args.country)

    print(f"Analysing {args.country} data")
    plot_data(data)
