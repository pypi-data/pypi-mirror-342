#!/usr/bin/env python3
# =============================================================================
"""Balena Vars Utils

Author:
    Juan Pablo Castillo - juan.castillo@kiwibot.com
"""
# =============================================================================

import balena
import os
import re
import balena.types.models
import json
from typing import List, Dict, Optional, Tuple
import gspread
import os
import uuid
import json
import base64
import datetime
import pytz
import google.auth
import re
from google.cloud import tasks_v2
from google.oauth2.service_account import Credentials
from google.protobuf import duration_pb2, timestamp_pb2
from fleet_control.utils.python_utils import select_option, printlog
from dotenv import dotenv_values
from pathlib import Path


def load_env_values():
    """Load .env values into a dict, if a file exists."""
    custom_env_path = os.getenv("FCT_ENV_PATH")
    env_path = Path(custom_env_path) if custom_env_path else Path.cwd() / ".env"

    if env_path.exists():
        env_vars = dotenv_values(dotenv_path=env_path)
        print(f"[env] Loaded from: {env_path}")
        return env_vars
    else:
        # print(f"[env] No .env file found at {env_path}. Using defaults and environment variables.")
        return {}
    
env_file_values: dict = load_env_values()

def get_config(key, default: str | None = None) -> str:
    """
    Get config value with priority:
    1. .env file
    2. default
    3. os.environ
    """
    if key in env_file_values:
        return env_file_values[key]
    elif default is not None:
        return default
    else:
        variable = os.getenv(key)
        if variable is None:
            raise EnvironmentError(f"{key} not set. Please export the variable into your environment or add it to a .env file")
        else:
            return variable
    

CREDENTIAL_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

PROJECT_ID = get_config("PROJECT_ID", "sd-gsheets-api")
SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
SPREADSHEET_NAME = get_config("SPREADSHEET_NAME", "SD Scheduled Var Changes")
WORKSHEET_NAME = get_config("WORKSHEET_NAME", "VarChangeLog")
LOCATION_ID = get_config("LOCATION_ID", "us-central1")
QUEUE_ID = get_config("QUEUE_ID", "schedule-vars")
PUBSUB_TOPIC = get_config("PUBSUB_TOPIC", "vars-change")
AUTHOR = get_config("AUTHOR", "default")
ORGANIZATION_HANDLE = get_config("ORGANIZATION_HANDLE", "g_kiwi_berkeley/")
SERVICE_ACCOUNT = get_config("GOOGLE_APPLICATION_CREDENTIALS", "/workspace/configs/gsheet_credentials.json")
BALENA_API_TOKEN = get_config("BALENA_API_KEY")

balena_sdk = balena.Balena()
balena_sdk.auth.login_with_token(BALENA_API_TOKEN)

def load_json(filename):
    with open(filename, "r") as f:
        data = f.read()
    return json.loads(data)

def get_service_id(target: balena.types.models.TypeDevice | int, service_name: str):
    if isinstance(target, int):
        app_id = target
    else:
        app_id = int(target["belongs_to__application"]["__id"])  # type: ignore
    services = balena_sdk.models.service.get_all_by_application(app_id)
    service = next((s["id"] for s in services if s.get("service_name") == service_name), 0)
    return service

def get_fleet_by_id(fleet_name: str) -> balena.types.models.TypeApplication | None:
    """Get device information by ID with 'kiwibot' prefix."""
    fleet = balena_sdk.models.application.get(ORGANIZATION_HANDLE + fleet_name)
    if not fleet:
        print(f"Device {fleet} not found.")
        return None
    return fleet

def get_device_by_id(device_id: str) -> balena.types.models.TypeDevice | None:
    """Get device information by ID with 'kiwibot' prefix."""
    device = balena_sdk.models.device.get_by_name(f"kiwibot{device_id}")
    if not device:
        print(f"Device {device_id} not found.")
        return None
    return device[0]


def get_fleet_variables(fleet: int | str | balena.types.models.TypeApplication) -> Tuple[Dict[str, str], Dict[str, str]]:
    """Fetch variables for a fleet."""
    if isinstance(fleet, str):
        fleet_env_vars = balena_sdk.models.application.env_var.get_all_by_application(ORGANIZATION_HANDLE + fleet)
        fleet_service_vars = balena_sdk.models.service.var.get_all_by_application(ORGANIZATION_HANDLE + fleet)
    elif isinstance(fleet, int):
        fleet_env_vars = balena_sdk.models.application.env_var.get_all_by_application(fleet)
        fleet_service_vars = balena_sdk.models.service.var.get_all_by_application(fleet)
    else:
        fleet_env_vars = balena_sdk.models.application.env_var.get_all_by_application(fleet["id"])
        fleet_service_vars = balena_sdk.models.service.var.get_all_by_application(fleet["id"])

    env_vars = {var["name"]: var["value"] for var in fleet_env_vars}
    service_vars = {var["name"]: var["value"] for var in fleet_service_vars}

    return env_vars, service_vars


def get_device_variables(
    device_info: balena.types.models.TypeDevice, custom: bool = False, fleet_vars=None
) -> Tuple[Dict[str, str], Dict[str, str], int]:
    """Fetch both environment and service variables for a device."""
    device_id = device_info["id"]
    app_id = int(device_info.get("belongs_to__application").get("__id"))  # type: ignore

    # Get device-specific variables
    device_env_vars = balena_sdk.models.device.env_var.get_all_by_device(device_id)
    device_service_vars = balena_sdk.models.device.service_var.get_all_by_device(device_id)

    env_vars, service_vars = {}, {}

    if not custom:
        if not fleet_vars:
            # Get fleet-level variables
            env_vars, service_vars = get_fleet_variables(app_id)
        else:
            env_vars, service_vars = fleet_vars["env_vars"], fleet_vars["service_vars"]["main"]

    service = get_service_id(device_info, "main")

    # Combine fleet and device variables
    env_vars.update({var["name"]: var["value"] for var in device_env_vars})
    service_vars.update({var["name"]: var["value"] for var in device_service_vars})

    return env_vars, service_vars, service


def find_release(fleet: str, semver: str | None) -> balena.types.models.ReleaseType:
    if semver:
        releases = balena_sdk.models.release.get_all_by_application(ORGANIZATION_HANDLE + fleet)
        version, revision = semver.split("+rev")

        for release in releases:
            if (version == "0.0.0" and release.get("revision") == int(revision)) or release.get("semver") == semver:
                return release  # Return the first matching release
        print("No release found")
        exit(1)
    else:
        release = balena_sdk.models.release.get_latest_by_application(ORGANIZATION_HANDLE + fleet)
        if release:
            return release
        else:
            print("No release found")
            exit(1)


def ask_confirmation(message_data, date_object, tz) -> str:
    if message_data["purge"]:
        printlog("Variables will be purged", "WARN")

    printlog("Variables to change: ", msg_type="OKPURPLE")
    for var in message_data["variables"]:
        printlog(f"{var['name']} = {var['value']}")

    printlog("Devices/Fleets to apply changes: ", msg_type="OKPURPLE")
    for dev in message_data["Target"]:
        printlog(f"{'Fleet' if dev['is_fleet'] else 'Device'}: {dev['name']}")

    printlog(
        f"Time selected: {datetime.datetime.strftime(date_object,'%Y-%m-%d %H:%M:%S GMT%Z')}",
        msg_type="OKPURPLE",
    )
    if date_object < pytz.timezone(tz).localize(datetime.datetime.now()):
        printlog(
            "Time selected is earlier than current time, task will run immediately!",
            "WARN",
        )

    opt = select_option(
        "Do you want to continue?",
        ["Yes", "Y", "No", "N"],
        msg_type="OKBLUE",
        case_insensitive=True,
    )
    return opt


def open_sheet(
    credentials_file: str, sheet_name: str, worksheet_name: str
) -> gspread.Worksheet: # type: ignore
    """
    Function to get access to a sheet file
    @param credentials_file (str): API json credentials file path
    @param sheet_key (str): google spreadsheet file key
    @param worksheet_name (str): google worksheet name

    @return gspread.worksheet instance
    """
    global author
    if os.path.isfile(credentials_file):
        printlog("Service account file based credentials used", "INFO")
        credentials = Credentials.from_service_account_file(
            credentials_file, scopes=SCOPES
        )
    else:
        printlog("Application Default Credentials (ADC) used", "INFO")
        credentials, project_id = google.auth.default(
            scopes=SCOPES, quota_project_id=PROJECT_ID
        )

    client = gspread.authorize(credentials) # type: ignore

    if AUTHOR == "default" and isinstance(credentials, Credentials):
        author = credentials.service_account_email

    return client.open(sheet_name).worksheet(worksheet_name)


def format_pubsub_message(message_data):
    return {
        "messages": [
            {
                "data": base64.b64encode(
                    json.dumps(message_data).encode("utf-8")
                ).decode("utf-8"),
                "attributes": {"origin": "cloud-tasks"},
            }
        ]
    }


def format_time(date_string, date_format: str, timezone: str = "America/Bogota"):
    """Creates datetime objects for the datetime input"""

    start = datetime.datetime.strptime(date_string, date_format)
    try:
        tz = pytz.timezone(timezone)
    except pytz.exceptions.UnknownTimeZoneError:
        printlog(f"Unknown Time Zone: {timezone}", "ERROR")
        exit(1)
    date_object = tz.localize(start)

    return date_object


def create_http_task(
    project: str,
    location: str,
    queue: str,
    url: str,
    json_payload: Dict,
    service_account_client_email: str,
    scheduled_datetime: Optional[datetime.datetime] = None,
    task_id: Optional[uuid.UUID] = None,
    deadline_in_seconds: Optional[int] = None,
) -> tasks_v2.Task:
    """Create an HTTP POST google cloud task with a JSON payload.
    Args:
        project: The project ID where the queue is located.
        location: The location where the queue is located.
        queue: The ID of the queue to add the task to.
        url: The target URL of the task.
        json_payload: The JSON payload to send.
        service_account_client_email: Service account email to authorize request.
        scheduled_datetime: Datetime to schedule the task for.
        task_id: ID to use for the newly created task.
        deadline_in_seconds: The deadline in seconds for task.
    Returns:
        The newly created task.
    """

    # Create a client.
    client = tasks_v2.CloudTasksClient()

    # Construct the task.
    task = tasks_v2.Task(
        http_request=tasks_v2.HttpRequest(
            http_method=tasks_v2.HttpMethod.POST,
            url=url,
            headers={"Content-type": "application/json"},
            body=json.dumps(json_payload).encode(),
            oauth_token=tasks_v2.OAuthToken(
                service_account_email=service_account_client_email
            ),
        ),
        name=(
            client.task_path(project, location, queue, str(task_id))
            if task_id is not None
            else None
        ),
    )

    if scheduled_datetime is not None:
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(scheduled_datetime)
        task.schedule_time = timestamp

    if deadline_in_seconds is not None:
        duration = duration_pb2.Duration()
        duration.FromSeconds(deadline_in_seconds)
        task.dispatch_deadline = duration

    return client.create_task(
        tasks_v2.CreateTaskRequest(
            # The queue to add the task to
            parent=client.queue_path(project, location, queue),
            task=task,
        )
    )

def parse_targets_variables(targets: list[str], variables: str) -> dict:
    """
    Create a JSON structure with the given list of names.

    Args:
        targets list[str]: List of targets to be added to the Target array
        variables (str): List of variables to be added to the variables array
                    should be in the form 'variable1=value=service'

    Returns:
        dict: Formatted JSON with the targets and variables added
    """

    # Create the base structure
    json_structure = {"purge": False, "Target": [], "variables": []}

    pattern = r"^[a-zA-Z0-9_]+=.*(=[a-zA-Z0-9_*]+)?$"

    for variable in variables.split(" "):
        if not re.match(pattern, variable):
            raise ValueError("Variable must be in the format 'variable1=value=service'")
        variable = variable.split("=")
        var_entry = {"name": variable[0], "value": variable[1], "service": variable[2]}
        json_structure["variables"].append(var_entry)

    # Define the regular expression for the desired format: 4X000
    pattern = r"^\d[A-Za-z]\d{3}$"

    for target in targets:
        if re.match(pattern, target):
            target_entry = {"is_fleet": False, "name": target}
        else:
            target_entry = {"is_fleet": True, "name": target}
        json_structure["Target"].append(target_entry)

    return json_structure