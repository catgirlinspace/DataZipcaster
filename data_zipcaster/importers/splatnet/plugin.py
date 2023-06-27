import os

import rich_click as click
from splatnet3_scraper.constants import TOKENS
from splatnet3_scraper.scraper import SplatNet_Scraper

from data_zipcaster.base_plugins import BaseImporter


class SplatNetImporter(BaseImporter):
    @property
    def name(self):
        return "splatnet"

    @property
    def help(self):
        return (
            "Imports data from SplatNet 3. This is the default importer.  "
            + "This requires one of the following arguments: \n"
            + " 1) `--session-token` to load your SplatNet 3 session token "
            + "directly from the command line. \n"
            + " 2) `--config` to load your SplatNet 3 tokens from a config "
            + "file. If no path is specified, the default path is "
            + "[bold yellow].splatnet3_scraper[/] in the current directory. \n"
            + "If neither of these are specified, the importer will "
            + "attempt to load your SplatNet 3 session token from the "
            + "environment variables [bold yellow]SESSION_TOKEN[/], "
            + "[bold yellow]GTOKEN[/], and [bold yellow]BULLET_TOKEN[/]."
            + "\n"
            + "If you do not have a SplatNet 3 session token, you can "
            + "generate one by following the instructions at "
        )

    def get_options(self) -> list[BaseImporter.Options]:
        OPTIONS = [
            BaseImporter.Options(
                option_name_1="-s",
                option_name_2="--salmon",
                is_flag=True,
                help="Import Salmon Run data.",
                default=False,
            ),
            BaseImporter.Options(
                option_name_1="-x",
                option_name_2="--xbattle",
                is_flag=True,
                help="Import XBattle data.",
                default=False,
            ),
            BaseImporter.Options(
                option_name_1="-t",
                option_name_2="--turf",
                is_flag=True,
                help="Import Turf War data.",
                default=False,
            ),
            BaseImporter.Options(
                option_name_1="-n",
                option_name_2="--anarchy",
                is_flag=True,
                help="Import Anarchy data.",
                default=False,
            ),
            BaseImporter.Options(
                option_name_1="-p",
                option_name_2="--private",
                is_flag=True,
                help="Import Private Battle data.",
                default=False,
            ),
            BaseImporter.Options(
                option_name_1="-c",
                option_name_2="--challenge",
                is_flag=True,
                help="Import Challenge data.",
                default=False,
            ),
            BaseImporter.Options(
                option_name_1="-a",
                option_name_2="--all",
                is_flag=True,
                help="Import all data.",
                default=False,
            ),
            BaseImporter.Options(
                option_name_1="--config",
                type_=click.Path(exists=False, dir_okay=False),
                help=(
                    "Path to the config file. If not specified, the default "
                    + "path is [bold yellow]config.ini[/] in the current "
                    + "directory."
                ),
                default=os.path.join(os.getcwd(), "config.ini"),
            ),
            BaseImporter.Options(
                option_name_1="--session-token",
                type_=str,
                help=(
                    "Your SplatNet 3 session token. This is required if "
                    + "you do not have a config file."
                ),
                default=None,
                nargs=1,
            ),
        ]
        return OPTIONS

    def get_scraper(self, config_data: dict[str, str]) -> SplatNet_Scraper:
        session_token = config_data.get(TOKENS.SESSION_TOKEN, None)
        gtoken = config_data.get(TOKENS.GTOKEN, None)
        bullet_token = config_data.get(TOKENS.BULLET_TOKEN, None)
        env_vars = config_data.get("env_vars", False)

        if env_vars:
            return SplatNet_Scraper.from_env()
        elif session_token is not None:
            out = SplatNet_Scraper.from_session_token(session_token)
            token_manager = out._query_handler.config.token_manager
            if gtoken is not None:
                token_manager.add_token(gtoken, TOKENS.GTOKEN)
            if bullet_token is not None:
                token_manager.add_token(bullet_token, TOKENS.BULLET_TOKEN)
            return out
        else:
            raise ValueError(
                "No session token was provided. Please provide a session token "
                + "by adding ``session_token = <your session token>`` to the "
                + "``[splatnet]`` section of your config file"
            )

    def do_run(
        self,
        config: dict[str, dict[str, str]],
        flags: dict[str, bool],
        *args,
        **kwargs,
    ):
        settings = config.get("settings", None)
        config_data = config[self.name]

        scraper = self.get_scraper(config_data)
