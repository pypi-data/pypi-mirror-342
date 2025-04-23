#!/usr/bin/env python3
"""
Command-line interface for nerd-mega-compute job management.
This module provides commands to list, cancel, and manage cloud compute jobs.
"""

import sys
import argparse
from .cloud import list_active_jobs, cancel_job, cancel_all_jobs

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="nerd-mega-compute CLI - Manage cloud compute jobs"
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # List command
    list_parser = subparsers.add_parser("list", help="List active jobs")

    # Cancel command
    cancel_parser = subparsers.add_parser("cancel", help="Cancel a specific job")
    cancel_parser.add_argument("job_id", help="ID of the job to cancel")

    # Cancel all command
    cancel_all_parser = subparsers.add_parser("cancel-all", help="Cancel all active jobs")

    # Parse arguments
    args = parser.parse_args()

    # Execute the appropriate command
    if args.command == "list":
        list_active_jobs()
    elif args.command == "cancel":
        success = cancel_job(args.job_id)
        sys.exit(0 if success else 1)
    elif args.command == "cancel-all":
        cancelled = cancel_all_jobs()
        print(f"Successfully cancelled {cancelled} jobs")
        sys.exit(0 if cancelled > 0 or len(list_active_jobs()) == 0 else 1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()