from ..convert import convert
from .parser import cli_parser


def main() -> None:
    args = cli_parser.parse_args()
    match args.command:
        case "convert":
            return convert(args.input_file, **vars(args), export=True)
        case _:
            print(args)
            return None


if __name__ == "__main__":
    main()
