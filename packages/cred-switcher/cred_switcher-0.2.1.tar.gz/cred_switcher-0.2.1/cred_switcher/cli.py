#!/usr/bin/env python3
import json
import subprocess
import os
from pathlib import Path
from getpass import getpass
from pyfiglet import Figlet

CONFIG_PATH = Path.home() / ".cred-switcher" / "config.json"
AWS_DIR = Path.home() / ".aws"

def prompt(msg):
    return input(msg).strip()

def set_git(git_config):
    subprocess.run(["git", "config", "--global", "user.name", git_config["name"]], check=True)
    subprocess.run(["git", "config", "--global", "user.email", git_config["email"]], check=True)
    print(f"Git set: {git_config['name']} <{git_config['email']}>")

def set_aws(aws_config):
    AWS_DIR.mkdir(exist_ok=True)
    credentials_path = AWS_DIR / "credentials"
    config_path = AWS_DIR / "config"
    credentials_path.write_text(f"""[default]
aws_access_key_id = {aws_config['access_key_id']}
aws_secret_access_key = {aws_config['secret_access_key']}
""")
    config_path.write_text(f"""[default]
region = {aws_config['region']}
output = json
""")
    print(f"AWS credentials set (region: {aws_config['region']})")

def switch_profile(profile_name):
    if not CONFIG_PATH.exists():
        print(f"Config file not found at {CONFIG_PATH}")
        return

    with open(CONFIG_PATH) as f:
        config = json.load(f)

    profile = config["profiles"].get(profile_name)
    if not profile:
        print(f"Profile '{profile_name}' not found in config.")
        return

    print(f"Switching to profile: {profile_name}")
    set_git(profile["git"])
    set_aws(profile["aws"])

def add_profile(profile_name):
    config_dir = CONFIG_PATH.parent
    config_dir.mkdir(exist_ok=True)
    config = {}

    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            config = json.load(f)

    if profile_name in config.get("profiles", {}):
        print(f"Profile '{profile_name}' already exists.")
        return

    print(f"Adding new profile: {profile_name}")
    git_name = prompt("Git Name: ")
    git_email = prompt("Git Email: ")
    aws_access_key_id = prompt("AWS Access Key ID: ")
    aws_secret_access_key = getpass("AWS Secret Access Key: ")
    aws_region = prompt("AWS Region (e.g., us-east-1): ")

    profile = {
        "git": {
            "name": git_name,
            "email": git_email
        },
        "aws": {
            "access_key_id": aws_access_key_id,
            "secret_access_key": aws_secret_access_key,
            "region": aws_region
        }
    }

    config.setdefault("profiles", {})[profile_name] = profile

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Profile '{profile_name}' added successfully!")

def list_profiles():
    if not CONFIG_PATH.exists():
        print("No config file found.")
        return

    with open(CONFIG_PATH) as f:
        config = json.load(f)

    profiles = config.get("profiles", {})
    if not profiles:
        print("No profiles saved.")
        return

    print("Available Profiles:")
    for name in profiles:
        print(f"- {name}")

def show_current():
    print("Current Git Identity:")
    try:
        git_name = subprocess.check_output(["git", "config", "--global", "user.name"]).decode().strip()
        git_email = subprocess.check_output(["git", "config", "--global", "user.email"]).decode().strip()
        print(f"{git_name} <{git_email}>")
    except subprocess.CalledProcessError:
        print("Git identity not set globally.")

    print("\nCurrent AWS Identity:")
    try:
        result = subprocess.check_output(["aws", "sts", "get-caller-identity", "--output", "json"])
        identity = json.loads(result)
        print(f"Account: {identity['Account']}")
        print(f"ARN: {identity['Arn']}")
        print(f"UserId: {identity['UserId']}")
    except subprocess.CalledProcessError:
        print("Failed to fetch AWS identity. Check your credentials.")


def print_banner():
    figlet = Figlet(font="slant")
    print(figlet.renderText("cred-switcher"))

def main():
    import sys
    print_banner()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  cred-switcher set <profile>")
        print("  cred-switcher add <profile>")
        print("  cred-switcher list")
        print("  cred-switcher show")
        return

    command = sys.argv[1]

    if command == "set":
        if len(sys.argv) != 3:
            print("Usage: cred-switcher set <profile>")
            return
        profile_name = sys.argv[2]
        switch_profile(profile_name)

    elif command == "add":
        if len(sys.argv) != 3:
            print("Usage: cred-switcher add <profile>")
            return
        profile_name = sys.argv[2]
        add_profile(profile_name)

    elif command == "list":
        list_profiles()
    elif command == "show":
        show_current()

    else:
        print(f"Unknown command: {command}")
        print("Available commands: set, add, list")