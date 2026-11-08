"""CLI Entrypoint for Simulated Operational Data Generation."""

import argparse
import json
import sys
import logging
from datetime import datetime

from simulator.generators.data_generator import SimulationGenerator
from simulator.generators.database_loader import (
    insert_dataset_into_databases,
    reset_simulated_data,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("simulator")


def json_serializer(obj):
    """JSON serializer for objects not serializable by default json code."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def main():
    parser = argparse.ArgumentParser(
        description="Deterministic Post-Harvest Simulated Operational Data Generator."
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Pseudorandom seed for reproducible generation (default: 42).",
    )
    parser.add_argument(
        "--scale",
        type=str,
        default="demo",
        choices=["small", "medium", "demo"],
        help="Dataset volume profile (small, medium, demo).",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="insert",
        choices=["insert", "dry-run", "export"],
        help="Execution mode: insert into database, dry-run (generate and display counts), or export to JSON.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Optional file path to output dataset in JSON format.",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Purge simulated records from MySQL and MongoDB.",
    )
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Mandatory confirmation flag required when executing --reset.",
    )

    args = parser.parse_args()

    # Handle Reset Operation
    if args.reset:
        if not args.confirm:
            logger.error("Error: --reset requires explicit --confirm flag to prevent accidental data loss.")
            sys.exit(1)

        logger.info("Purging simulated operational data...")
        try:
            purged = reset_simulated_data(confirm=True)
            logger.info("Simulated data reset complete. Records purged: %s", purged)
            sys.exit(0)
        except Exception as exc:
            logger.error("Failed to reset simulated data: %s", exc)
            sys.exit(1)

    # Generation Workflow
    logger.info(
        "Generating simulated dataset (seed=%d, scale='%s', mode='%s')...",
        args.seed,
        args.scale,
        args.mode,
    )
    generator = SimulationGenerator(seed=args.seed, scale=args.scale)
    dataset = generator.generate()

    logger.info("Synthesis complete. Record counts:")
    for key, count in dataset.counts.items():
        logger.info("  - %-15s: %d", key, count)

    if args.output or args.mode == "export":
        out_path = args.output or f"simulated_dataset_{args.scale}_seed{args.seed}.json"
        export_payload = {
            "seed": dataset.seed,
            "scale": dataset.scale,
            "counts": dataset.counts,
            "devices": dataset.devices,
            "models": dataset.models,
            "sessions": dataset.sessions,
            "tasks": dataset.tasks,
            "decisions": dataset.decisions,
            "operations": dataset.operations,
            "system_events": dataset.system_events,
            "detections": dataset.detections,
            "telemetry_logs": dataset.telemetry_logs,
        }
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(export_payload, f, default=json_serializer, indent=2)
        logger.info("Dataset successfully exported to %s", out_path)

    if args.mode == "insert":
        logger.info("Persisting dataset into MySQL and MongoDB...")
        try:
            inserted = insert_dataset_into_databases(dataset)
            logger.info("Database ingestion summary: %s", inserted)
        except Exception as exc:
            logger.warning("Database persistence incomplete: %s", exc)


if __name__ == "__main__":
    main()
