from base import DEFAULT_COUNTRY
from download import download_reports
from parse import parse_reports
from plot import plot_data
from util import load

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--country',
                        type=str, default=DEFAULT_COUNTRY,
                        help='report by country')
    args = parser.parse_args()

    download_reports()
    parse_reports(args.country)

    report = load(args.country)
    print(f"Analysing {args.country} data")
    plot_data(report)
