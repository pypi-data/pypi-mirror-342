import argparse

from app.rag.config import top_parser, common_parser

help = "Diagnose the RAG system."

parser = argparse.ArgumentParser(
    description = f"{help} Performs comprehensive health checks on all components, validates configurations, and reports issues to ensure optimal system operation",
    add_help = False,
    formatter_class = argparse.ArgumentDefaultsHelpFormatter,
)

subparsers = parser.add_subparsers(
    title = "subcommands",
    dest = "subcommand",
)

subparsers.add_parser(
    "check",
    help = "Check RAG System. Scan all components of the system and diagnose status",
    description = "Check RAG System. Scan all components of the system and diagnose status",
    parents = [top_parser, common_parser],
    add_help = False,
)
