import argparse

parser = argparse.ArgumentParser(description="Generate split line for the given file")
parser.add_argument("--title", type=str, help="file to generate split line")
parser.add_argument("--num", type=str, help="file to generate split line")


def main():
    n = int(parser.parse_args().num)
    title = f" {parser.parse_args().title} ".center(n, "-")
    print("# " + title)
    print("# " + "-" * n)


if __name__ == "__main__":
    main()
