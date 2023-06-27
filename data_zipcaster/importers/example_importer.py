from data_zipcaster.base_plugins import BaseImporter


class ExampleImporter(BaseImporter):
    @property
    def get_options(self) -> list[BaseImporter.Options]:
        OPTIONS = [
            BaseImporter.Options(
                option_name_1="-x",
                option_name_2="--example",
                type_=str,
                help="An example option.",
                default="example",
            ),
            BaseImporter.Options(
                option_name_1="-y",
                option_name_2="--example2",
                is_flag=True,
                help="An example flag.",
                default=False,
            ),
        ]
        return OPTIONS

    @property
    def name(self) -> str:
        return "example"

    @property
    def help(self) -> str:
        return "An example importer."

    def do_run(self, **kwargs) -> None:
        print("Example importer running!")
        print("Flags:")
        for key, value in kwargs.items():
            print(f"{key}: {value}")

        print("Parsing Options:")
