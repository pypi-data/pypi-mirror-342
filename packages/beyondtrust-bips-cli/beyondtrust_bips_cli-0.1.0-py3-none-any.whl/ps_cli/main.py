"""
Password Safe CLI Entrypoint
"""

from ps_cli.controllers.assets import Asset
from ps_cli.controllers.folders import Folder
from ps_cli.controllers.managed_systems import ManagedSystem
from ps_cli.controllers.safes import Safe
from ps_cli.controllers.secrets import Secret
from ps_cli.controllers.settings import Settings
from ps_cli.core.app import App


def main() -> None:
    controllers = [
        Safe,
        Folder,
        Secret,
        ManagedSystem,
        Settings,
        Asset,
    ]

    app = App(controllers=controllers)
    app.run()


if __name__ == "__main__":
    main()
