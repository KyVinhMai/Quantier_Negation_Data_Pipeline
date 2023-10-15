import NPR_webscrawler
import Ambiguity_Search

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Replace entities with an assigned substitutes")
    option = parser.add_mutually_exclusive_group(required=True)

    option.add_argument(
        "--all",
        type = str,
        nargs = "+",
        default=None,
        help = "Specify the directory to read. Will parse through the entire corpus. Generating character lists and assigning characters." )

    #Modification Options
    option.add_argument(
        "--last_batch",
        type = str,
        nargs = "+",
        default=None,
        help = "Will replace characters within the book. Assumes there already is a character list" ) #error handling for books

    option.add_argument(
        "--file",
        type=str,
        nargs = "+",
        default=None,
        help="Assumes you want a single file that will be modified. CANNOT generate it's own character list")

    #add random seed
    #Perhaps just create a random character list?

    parsed_args = parser.parse_args()

    if parsed_args.all is None and parsed_args.book is None and parsed_args.file is None:
        parsed_args.error("At least one of the parsing options is required")

    main(parsed_args)

    crawl_NPR_archives("npr_links.txt")