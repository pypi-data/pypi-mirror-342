import argparse

help = "Test the RAG system."

parser = argparse.ArgumentParser(
    description = f"{help} Evaluates system performance by running predefined test cases, measuring accuracy, relevance, and latency metrics to validate retrieval and generation capabilities",
    add_help = False,
    formatter_class = argparse.ArgumentDefaultsHelpFormatter,
)
