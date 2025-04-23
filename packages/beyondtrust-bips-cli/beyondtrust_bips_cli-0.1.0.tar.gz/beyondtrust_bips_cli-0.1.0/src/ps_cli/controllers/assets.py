from secrets_safe_library import assets, exceptions, smart_rules, workgroups
from secrets_safe_library.constants.endpoints import (
    GET_ASSETS_ID,
    GET_WORKGROUPS_ID_ASSETS,
    GET_WORKGROUPS_NAME_ASSETS_NAME,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.assets import fields as asset_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class Asset(CLIController):
    """
    List, create, retrive, or print BeyondInsight Asset Information
    That API user has rights to.

    See the 'Assets' Section of the PBPS API Guide.
    Requires permissions: Asset Management.
    """

    def __init__(self):
        super().__init__(
            name="assets",
            help="Asset management commands",
        )

    _workgroup_object: workgroups.Workgroup = None
    _smartrule_object: smart_rules.SmartRule = None

    @property
    def class_object(self) -> assets.Asset:
        if self._class_object is None and self.app is not None:
            self._class_object = assets.Asset(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @property
    def smartrule_object(self) -> smart_rules.SmartRule:
        if self._smartrule_object is None and self.app is not None:
            self._smartrule_object = smart_rules.SmartRule(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._smartrule_object

    @property
    def workgroup_object(self) -> workgroups.Workgroup:
        if self._workgroup_object is None and self.app is not None:
            self._workgroup_object = workgroups.Workgroup(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._workgroup_object

    @command
    @aliases("list")
    @option(
        "-wgn",
        "--workgroup-name",
        help="Workgroup name, either name or ID is requied",
        type=str,
        required=False,
    )
    @option(
        "-wgi",
        "--workgroup-id",
        help="Workgroup ID, either name or ID is requied",
        type=int,
        required=False,
    )
    @option(
        "-l",
        "--limit",
        help="Number of records to return. Default 100000",
        type=int,
        required=False,
        default=100000,
    )
    @option(
        "-o",
        "--offset",
        help=(
            "Number of records to skip before returning records (can only be used in "
            "conjunction with limit). Default 0"
        ),
        type=int,
        required=False,
    )
    def list_assets(self, args):
        """
        Returns a list of assets by Workgroup name (-wgn) or ID (-wgi).
        """
        try:
            if not args.workgroup_id and not args.workgroup_name:
                print_it("Please provide either --workgroup-id or --workgroup-name")
                return

            fields = self.get_fields(
                GET_WORKGROUPS_ID_ASSETS, asset_fields, Version.DEFAULT
            )
            self.display.v("Calling list_assets function")
            assets = self.class_object.list_assets(
                workgroup_id=args.workgroup_id,
                workgroup_name=args.workgroup_name,
                limit=args.limit,
                offset=args.offset,
            )
            self.display.show(assets, fields)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list assets")

    @command
    @aliases("list-by-smart-rule", "list-by-sr")
    @option(
        "-t",
        "--title",
        help="Smart Rule title",
        type=str,
        required=False,
    )
    @option(
        "-id",
        "--smart-rule-id",
        help="Smart Rule ID",
        type=int,
        required=False,
    )
    @option(
        "-l",
        "--limit",
        help="Number of records to return. Default 100000",
        type=int,
        required=False,
        default=100000,
    )
    @option(
        "-o",
        "--offset",
        help=(
            "Number of records to skip before returning records (can only be used in "
            "conjunction with limit). Default 0"
        ),
        type=int,
        required=False,
    )
    def list_assets_by_smart_rule(self, args):
        """
        Returns a list of assets by Smart Rule title or ID.
        """
        try:
            if args.smart_rule_id:
                self.display.v("Using provided smart rule ID")
                smart_rule_id = args.smart_rule_id
            elif args.title:
                self.display.v("Calling get_smart_rule_by_title function")
                smart_rule = self.smartrule_object.get_smart_rule_by_title(args.title)
                smart_rule_id = smart_rule["SmartRuleID"]
            else:
                print_it("Please provide either --title or --smart-rule-id")
                return

            assets = self.smartrule_object.list_assets_by_smart_rule_id(
                smart_rule_id=smart_rule_id,
                limit=args.limit,
                offset=args.offset,
            )

            fields = self.get_fields(GET_ASSETS_ID, asset_fields, Version.DEFAULT)
            self.display.show(assets, fields)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list assets by smart rule")

    @command
    @aliases("get-by-id")
    @option(
        "-id",
        "--asset-id",
        help="Asset ID",
        type=int,
        required=True,
    )
    def get_asset_by_id(self, args):
        """
        Returns an asset by Asset ID (-id).
        """
        try:
            fields = self.get_fields(GET_ASSETS_ID, asset_fields, Version.DEFAULT)
            self.display.v("Getting asset by ID")
            asset = self.class_object.get_asset_by_id(asset_id=args.asset_id)
            self.display.show(asset, fields)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(f"It was not possible to get the asset for ID: {args.asset_id}")

    @command
    @aliases("get-by-wg")
    @option(
        "-wgn",
        "--workgroup-name",
        help="Workgroup name, either workgroup name or ID is required",
        type=str,
        required=False,
    )
    @option(
        "-wgi",
        "--workgroup-id",
        help="Workgroup ID, either workgroup name or ID is required",
        type=int,
        required=False,
    )
    @option(
        "-an",
        "--asset-name",
        help="Asset name",
        type=str,
        required=True,
    )
    def get_asset_by_workgroup(self, args):
        """
        Returns an asset by workgroup name or ID (-wgn | -wgi) and asset name (-an).
        """
        try:
            if not args.workgroup_id and not args.workgroup_name:
                print_it("Please provide either workgroup name (-wgn) or ID (-wgi)")
                return

            fields = self.get_fields(
                GET_WORKGROUPS_NAME_ASSETS_NAME, asset_fields, Version.DEFAULT
            )

            if args.workgroup_id:
                self.display.v("Getting workgroup name using its ID")
                workgroup = self.workgroup_object.get_workgroup_by_id(args.workgroup_id)
                workgroup_name = workgroup["Name"]
            elif args.workgroup_name:
                self.display.v("Getting asset by workgroup name directly")
                workgroup_name = args.workgroup_name

            asset = self.class_object.get_asset_by_workgroup_name(
                workgroup_name=workgroup_name,
                asset_name=args.asset_name,
            )
            self.display.show(asset, fields)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to get the asset")

    @command
    @aliases("search")
    @option("-n", "--asset-name", help="Asset name", type=str)
    @option("-dns", "--dns-name", help="DNS name", type=str)
    @option("-domain", "--domain-name", help="Domain name", type=str)
    @option("-ip", "--ip-address", help="IP address", type=str)
    @option("-mac", "--mac-address", help="MAC address", type=str)
    @option("-t", "--asset-type", help="Asset type", type=str)
    @option(
        "-l",
        "--limit",
        help="Number of records to return. Default 100000",
        type=int,
        required=False,
        default=100000,
    )
    @option(
        "-o",
        "--offset",
        help=(
            "Number of records to skip before returning records (can only be used in "
            "conjunction with limit). Default 0"
        ),
        type=int,
        required=False,
    )
    def search_assets(self, args):
        """
        Returns a list of assets that match the given search options.

        At least one search option should be provided; any property not provided is
        ignored. All search criteria is case insensitive and is an exact match
        (equality), except for IPAddress.
        """
        try:
            fields = self.get_fields(
                GET_WORKGROUPS_ID_ASSETS, asset_fields, Version.DEFAULT
            )
            self.display.v("Calling search_assets function")
            assets = self.class_object.search_assets(
                asset_name=args.asset_name,
                dns_name=args.dns_name,
                domain_name=args.domain_name,
                ip_address=args.ip_address,
                mac_address=args.mac_address,
                asset_type=args.asset_type,
                limit=args.limit,
                offset=args.offset,
            )
            self.display.show(assets, fields)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to search the assets")
        except exceptions.OptionsError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("At least one search option should be provided")
