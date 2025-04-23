import argparse
import logging
import os
import csv
from typing import Optional
from dotenv import load_dotenv
from tldr_tools.tldr_endpoint import APIManager, TLDREndpoints
from tldr_tools.tldr_status import check_job_status

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODULE_CONFIG = {
    "dockopt": {
        "endpoint": "submit/dockopt",
        "description": "Optimization pipeline for DOCK38",
        "required_files": {
            "recpdb": "recpdb",
            "xtalpdb": "xtalpdb",
            "activestgz": "activestgz",
            "decoystgz": "decoystgz",
        },
        "optional": ["memo"],
        "cli_args": [
            {"name": "--activestgz", "help": "Path to actives.tgz file.", "required": True},
            {"name": "--decoystgz", "help": "Path to decoys.tgz file.", "required": True},
            {"name": "--recpdb", "help": "Path to receptor PDB file.", "required": True},
            {"name": "--xtalpdb", "help": "Path to xtal ligand PDB file.", "required": True},
            {"name": "--memo", "help": "Optional memo text.", "required": False},
        ],
    },
    "build": {
        "endpoint": "submit/build3d38",
        "description": "Prepare a 3D library for docking in up to four formats used by popular docking programs using DOCK3.8 pipeline.",
        "required_files": {
            "input": "input.txt",
        },
        "optional": ["memo"],
        "cli_args": [
            {"name": "--input", "help": "File of SMILES ([SMILES] [COMPOUND_NAME] per line).", "required": True},
            {"name": "--memo", "help": "Optional memo text.", "required": False},
        ],
    },
    "decoys": {
        "endpoint": "submit/dudez",
        "description": "Decoy generation module for active compound generation.",
        "required_files": {
            "activesism": "actives.ism",
            "decoygenin": "decoy_generation.in",
        },
        "optional": ["memo"],
        "cli_args": [
            {"name": "--activesism", "help": "Path to actives.ism file.", "required": True},
            {"name": "--decoygenin", "help": "Path to decoy_generation.in file.", "required": True},
            {"name": "--memo", "help": "Optional memo text.", "required": False},
        ],
    },
}

def export_job_to_csv(csv_path: str, memo: str, job_type: str, job_no: str):
    """
    Append a job record to a CSV file with columns: memo, job_type, job_no.
    If the file exists, checks column compatibility before appending.
    """
    expected_fields = ["memo", "job_type", "job_no"]
    file_exists = os.path.isfile(csv_path)

    # If file exists, validate header
    if file_exists:
        with open(csv_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader, None)
        if header != expected_fields:
            logger.error(f"CSV file {csv_path} has incompatible columns: {header}. Expected {expected_fields}.")
            return

    # Open for appending (create with header if new)
    with open(csv_path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=expected_fields)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "memo": memo,
            "job_type": job_type,
            "job_no": job_no,
        })
    logger.info(f"Exported job {job_no} to CSV {csv_path}.")


def add_module_arguments(parser, module_name, module_config):
    """Dynamically add arguments based on module config."""
    module = module_config.get(module_name, {})
    if not module:
        raise ValueError(f"Module {module_name} not found in the configuration.")
    for arg in module.get("cli_args", []):
        parser.add_argument(
            arg["name"],
            type=str,
            required=arg.get("required", False),
            help=arg.get("help", "No description provided."),
        )


def main():
    parser = argparse.ArgumentParser(description="Submit and manage docking tasks via TLDR API.")
    parser.add_argument("--list-modules", action="store_true", help="List all available modules and exit.")
    parser.add_argument("--module", choices=MODULE_CONFIG.keys(), help="Module type to submit.")
    parser.add_argument("--export-csv", help="Path to CSV file to append job records.")

    args, unknown_args = parser.parse_known_args()

    # Handle listing modules
    if args.list_modules:
        print("Available modules:")
        for m, config in MODULE_CONFIG.items():
            print(f"- {m}: {config['description']}")
            for arg in config.get("cli_args", []):
                print(f"   {arg['name']} - {arg.get('help', 'No description provided.')}")
        return

    # Ensure module selection
    if not args.module:
        parser.error("You must specify a module using --module.")
    module_name = args.module

    # Build module-specific parser
    module_parser = argparse.ArgumentParser(add_help=False)
    add_module_arguments(module_parser, module_name, MODULE_CONFIG)
    module_args = module_parser.parse_args(unknown_args)

    # Initialize API manager
    api_manager = APIManager()

    # Submit module
    response = submit_module(api_manager, module_name, **vars(module_args))
    if not response:
        logger.error("Job failed to submit.")
        return

    # Check submission and status
    if hasattr(response, 'text') and response.text:
        logger.info("Job submitted, but unsure if it went through (this is expected). Checking if identified job is running...")
        submitted_job = api_manager.url_to_job_no(response.url)
        job_status = check_job_status(api_manager, submitted_job)

        print(job_status)
        if job_status in ['Submitted', 'Running']:
            logger.info(f"Job {submitted_job} is {job_status} and submitted successfully!")
            # Export to CSV if requested
            if args.export_csv:
                memo_value = getattr(module_args, 'memo', '') or ''
                export_job_to_csv(args.export_csv, memo_value, module_name, submitted_job)
        else:
            logger.error(f"Job {submitted_job} status is unrecognized: {job_status}.")
    else:
        logger.error("Job failed to submit.")


if __name__ == "__main__":
    main()
