import argparse

help = "Train the RAG system."

parser = argparse.ArgumentParser(
    description = f"{help} Processes documents, extracts knowledge, generates embeddings, and builds a searchable vector database for efficient semantic retrieval and contextual responses",
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
)
