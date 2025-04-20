import argparse
import json

# module logger
import logging
from datetime import datetime

from tabulate import tabulate

from .paths import DATA_DIR, IDS_FILE, LOG_DIR
from .user import Consent, ConsentManager, IDManager, Profile
from .utils import get_localtion_data, get_python_data, get_system_data, get_usage_data

logger = logging.getLogger(__name__)


def records_list() -> None:
    # print records
    table = []
    for record in list(DATA_DIR.glob("*.json")):
        # load record
        with open(record, "r") as f:
            data = json.load(f)
            logger.debug(f"Extracting data from record {record}: {data}")

        # extract data
        timestamp = data["user"]["timestamp"]
        request_id = data["uuid"]
        for app in data["app"]:
            profile = app["profile"]
            package = app["name"]

            # table
            table.append([request_id, profile, package, timestamp])

    # sort by started_on
    table = sorted(table, key=lambda x: x[3], reverse=True)

    # format started_on yyyy-mm-dd hh:mm:ss
    for row in table:
        row[3] = row[3].replace("T", " ").replace("Z", "").split(".")[0]

    # print table
    print(tabulate(table, headers=["ID", "Profile", "Package", "Started On"]))


def _get_run_ids_for_stem(run_id: str) -> list[str]:
    record_files = list(DATA_DIR.glob("*.json"))
    return [record.stem for record in record_files if record.stem.startswith(run_id)]


def _complete_run_if(run_id: str) -> str | None:
    run_ids = _get_run_ids_for_stem(run_id)
    if len(run_ids) == 1:
        return run_ids[0]
    return None


def _flatten_json(data: dict, parent_key: str = "", sep: str = " / ") -> dict:
    items = []
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(_flatten_json(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def record_show(run_id: str) -> None:
    # complete run_id
    if len(run_id) < 36:
        run_id = _complete_run_if(run_id)
        assert run_id, f"Run with id {run_id} does not exist"

    # get record file
    record_file = DATA_DIR / f"{run_id}.json"
    assert record_file.exists(), f"Record with id {run_id} does not exist"

    # check if record exists
    if not record_file.exists():
        print(f"Record with id {run_id} does not exist")
        return

    # load record
    with open(record_file, "r") as f:
        record = json.load(f)

    # print record information
    table = [
        [
            app["uuid"],
            app["name"],
            app["profile"],
            app["version"],
            record["user"]["timestamp"],
            app["runtime"],
        ]
        for app in record["app"]
    ]

    print(
        tabulate(
            table,
            headers=["ID", "Package", "Profile", "Version", "Started On", "Runtime"],
        )
    )
    print()

    # print user information
    fdata = _flatten_json(record["user"])
    table = [[k, v] for k, v in fdata.items()]
    print(tabulate(table, headers=["Key", "Value"]))

    # print data
    # for app in record["app"]:
    #   fdata = _flatten_json(app)
    #   table = [[k, v] for k, v in fdata.items()]
    #   print(tabulate(table, headers=["Key", "Value"]))


def records_overview() -> None:
    # get all records
    record_files = list(DATA_DIR.glob("*.json"))

    # load data
    packages = {}
    for record_file in record_files:
        # read record file
        with open(record_file, "r") as f:
            record = json.load(f)

        for app in record["app"]:
            # extract run data
            package = app["name"]
            profile = app["profile"].lower()
            runtime = app["runtime"]
            started_on = record["user"]["timestamp"]

            # create empty package entry
            if package not in packages:
                if ConsentManager.get().isPackageBlacklisted(package):
                    package_consent = "DENY (blacklisted)"
                elif ConsentManager.get().isPackageWhitelisted(package):
                    package_consent = "ALLOW (whitelisted)"
                else:
                    package_consent = ConsentManager.get().consent.name + " (default)"

                packages[package] = {
                    "user": 0,
                    "package": 0,
                    "anonymous": 0,
                    "runtime": 0,
                    "last_execution": None,
                    "profile": ConsentManager.get().getPackageProfile(package).name,
                    "consent": package_consent,
                }

            # update package entry
            packages[package][profile] += 1
            packages[package]["runtime"] += runtime
            packages[package]["last_execution"] = (
                started_on
                if packages[package]["last_execution"] is None
                else max(packages[package]["last_execution"], started_on)
            )

    # create table
    table = []
    for package, data in packages.items():
        table.append(
            [
                package,
                data["user"],
                data["package"],
                data["anonymous"],
                data["runtime"] / (data["user"] + data["package"] + data["anonymous"]),
                data["profile"],
                data["consent"],
                data["last_execution"],
            ]
        )

    # print table
    print(
        tabulate(
            table,
            headers=[
                "Package",
                "User",
                "Package",
                "Anonymous",
                "Average Runtime",
                "Profile",
                "Consent",
                "Last Execution",
            ],
        )
    )


def print_consent() -> None:
    # load consent manager
    cm = ConsentManager.get()

    # print global consent and default profile
    print("\033[1m\033[94mGlobal Consent:\033[0m")
    print(f"  Consent: {cm.consent.name}")
    print(f"  Profile: {cm.profile.name}")

    # print whitelist
    print("\033[1m\033[92m\nWhitelist:\033[0m")
    if cm.whitelist:
        for package, profile in cm.whitelist.items():
            print(f"  {package}: {profile.name}")
    else:
        print("  \033[93mNo packages in the whitelist.\033[0m")

    # print blacklist
    print("\033[1m\033[91m\nBlacklist:\033[0m")
    if cm.blacklist:
        for package in cm.blacklist:
            print(f"  {package}")
    else:
        print("  \033[93mNo packages in the blacklist.\033[0m")


def cli() -> None:
    # create parser
    parser = argparse.ArgumentParser(description="Plausipy CLI")
    subparsers = parser.add_subparsers(dest="command")
    parser.set_defaults(command="overview")

    # list command
    # subparsers.add_parser("list", help="List all stored data")

    # overview command
    subparsers.add_parser("overview", help="Show an overview of all stored data")

    # show command
    # show_parser = subparsers.add_parser("show", help="Show a specific stored data")
    # show_parser.add_argument("run_id", type=str, help="The id of the run to show")

    # delete command
    # subparsers.add_parser("delete", help="Delete a specific stored data")

    # clear command
    clear_parser = subparsers.add_parser("clear", help="Delete all locally stored data")
    group = clear_parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--runs", action="store_true", help="Delete all locally stored runs"
    )
    group.add_argument(
        "--ids", action="store_true", help="Delete all locally stored ids"
    )
    group.add_argument(
        "--logs", action="store_true", help="Delete all locally stored logs"
    )
    group.add_argument(
        "--all", action="store_true", help="Delete all locally stored data"
    )

    # profile command
    settings = subparsers.add_parser(
        "consent", help="Specify the settings for plausipy and packages"
    )
    settings.add_argument(
        "packages",
        default=[],
        nargs="*",
        help="Specify optional package names to white or blacklist",
    )
    consent_group = settings.add_mutually_exclusive_group()
    consent_group.add_argument(
        "--yes",
        "--allow",
        "--whitelist",
        "-y",
        action="store_true",
        help="Consent to (allow) tracking",
    )
    consent_group.add_argument(
        "--no",
        "--deny",
        "--blacklist",
        "-n",
        action="store_true",
        help="Disallow tracking",
    )
    consent_group.add_argument(
        "--ask", "-a", action="store_true", help="Ask for consent every time"
    )
    settings.add_argument(
        "--profile",
        "-p",
        type=str,
        choices=[p.value for p in Profile],
        help="Set the tracking profile",
    )
    settings.add_argument(
        "--reset", action="store_true", help="Reset the settings to factory defaults"
    )
    settings.add_argument("--raw", action="store_true", help="Print raw settings")

    # me command
    subparsers.add_parser(
        "me", help="Show information the user provides / aggregated of the user"
    )

    # parse arguments
    args = parser.parse_args()

    # execute command
    if args.command == "list":
        logger.debug("List all stored data")
        records_list()

    elif args.command == "overview":
        logger.debug("Show an overview of all stored data")
        records_overview()

    elif args.command == "show":
        logger.debug(f"Show a specific stored data with id {args.run_id}")
        record_show(args.run_id)

    elif args.command == "delete":
        logger.debug("Delete a specific stored data")
        print("\033[31mWARNING: This functionality is not yet implemented\033[0m")

        # just print all tracking ids that would be used for deletion of one or multiple records
        # NOTE: when a package makes anonymous calls, it is not possible to delete data for that specific pacakge only without risking a sensitive link on the user's system
        # NOTE: in general, albeit this information beeing local, unless it is encrypted, it's not really safe. So we should either minimize the information or encrypt local records for transparency.

        id_manager = IDManager()
        data = id_manager._data
        print(json.dumps(data, indent=2))

    elif args.command == "clear":
        # ask for confirmation
        if (
            not input("Are you sure you want to delete all stored data? (y/n): ")
            .lower()
            .startswith("y")
        ):
            print("Aborted")
            return

        if args.runs or args.all:
            for record in DATA_DIR.glob("*.json"):
                record.unlink()
            print("Deleted all stored runs")

        if args.ids or args.all:
            if IDS_FILE.exists():
                IDS_FILE.unlink()
            print("Deleted all stored ids")

        if args.logs or args.all:
            for log in LOG_DIR.glob("*.log*"):
                log.unlink()
            print("Deleted all stored logs")

    elif args.command == "consent":
        # get consent manager instance
        cm = ConsentManager.get()

        # reset consent manager
        if args.reset:
            if not args.packages:
                logger.info("Resetting consent selection to factory defaults")
                cm.reset()
            else:
                logger.info(
                    "Resetting consent selection for specific packages to factory defaults"
                )
                for package in args.packages:
                    cm.removePackageFromWhitelist(package)
                    cm.removePackageFromBlacklist(package)

        # specify consent (saves automatically)
        assert sum([args.yes, args.no, args.ask]) <= 1, (
            "Only one of --allow, --no, --ask can be set."
        )
        assert not (args.ask and args.packages), (
            "The ask option cannot be specified on specific packages."
        )

        if not args.packages:
            # update default consent
            if args.yes:
                cm.consent = Consent.ALLOW
            elif args.no:
                cm.consent = Consent.DENY
            elif args.ask:
                cm.consent = Consent.ASK

            # update default profile
            if args.profile:
                cm.profile = Profile(args.profile)

        else:
            # white-/blacklist specific packages
            for package in args.packages:
                if args.yes:
                    whitelist_with_profile = (
                        Profile(args.profile) if args.profile else Profile.ANONYMOUS
                    )
                    cm.addPackageToWhitelist(package, whitelist_with_profile)
                elif args.no:
                    cm.addPackageToBlacklist(package)

        # print settings
        if args.raw:
            print(json.dumps(cm._data, indent=2))
        else:
            print_consent()

    elif args.command == "me":
        logger.debug("Show information the user provides / aggregated of the user")
        print(
            "\033[1m\033[94mThe following information is uploaded when data collection is permitted:\033[0m"
        )

        # collect the information the user provides
        data = {
            "Location": {k.capitalize(): v for k, v in get_localtion_data().items()},
            "Usage": {k.capitalize(): v for k, v in get_usage_data().items()},
            "System": {k.capitalize(): v for k, v in get_system_data().items()},
            "Python": {k.capitalize(): v for k, v in get_python_data().items()},
            "Timestamp": str(datetime.now()),
        }

        # flatten
        data = _flatten_json(data)

        # print data
        table = [[k, v] for k, v in data.items()]
        print(tabulate(table))

    else:
        logger.debug("No command provided, display help")
        parser.print_help()
