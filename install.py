import os
from pathlib import Path
from launch import git, run
import launch
import sys
import logging
from packaging import version as pv
import importlib.metadata as metadata

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

REPO_LOCATION = Path(__file__).parent
auto_update = True
extension_branch = "master"

if auto_update:
    logging.info("[Auto-Photoshop-SD] Attempting auto-update...")

    try:
        checkout_result = run(
            f'"{git}" -C "{REPO_LOCATION}" checkout {extension_branch}',
            "[Auto-Photoshop-SD] switch branch to extension branch.",
        )
        logging.info(f"checkout_result: {checkout_result}")

        branch_result = run(
            f'"{git}" -C "{REPO_LOCATION}" branch',
            "[Auto-Photoshop-SD] Current Branch.",
        )
        logging.info(f"branch_result: {branch_result}")

        fetch_result = run(
            f'"{git}" -C "{REPO_LOCATION}" fetch', "[Auto-Photoshop-SD] Fetch upstream."
        )
        logging.info(f"fetch_result: {fetch_result}")

        pull_result = run(
            f'"{git}" -C "{REPO_LOCATION}" pull', "[Auto-Photoshop-SD] Pull upstream."
        )
        logging.info(f"pull_result: {pull_result}")

    except Exception as e:
        logging.error("[Auto-Photoshop-SD] Auto-update failed:")
        logging.error(e)
        logging.error("[Auto-Photoshop-SD] Ensure git was used to install extension.")

def install_or_update_package(package_name, package_version):
    try:
        installed_version = metadata.version(package_name)
        if installed_version:
            installed_version = pv.parse(installed_version)
            if installed_version != pv.parse(package_version):
                logging.info(
                    f"{package_name} version: {installed_version} will update to version: {package_version}"
                )
                launch.run_pip(
                    f"install {package_name}=={package_version}",
                    "update requirements for Auto-Photoshop Image Search",
                )
        else:
            logging.info(f"Unable to determine installed version of {package_name}.")
    except metadata.PackageNotFoundError:
        logging.error(f"Error: {package_name} is not installed.")
        launch.run_pip(
            f"install {package_name}=={package_version}",
            "install requirements for Auto-Photoshop Image Search",
        )
    except Exception as e:
        logging.error(f"An unexpected error occurred while checking {package_name}: {e}")

# Example usage:
install_or_update_package("duckduckgo_search", "3.9.9")
install_or_update_package("httpx", "0.24.1")

