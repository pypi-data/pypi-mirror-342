import argparse, os
from dotenv import load_dotenv
from loguru import logger

load_dotenv(dotenv_path=os.environ.get('ENV_FILE', '.env'), override=True)

from app.rag.config import top_parser, common_parser, setup_logger
from app.rag.doctor import help as doctor_help, parser as doctor_parser, route as doctor_route
from app.rag.train import help as train_help, parser as train_parser, route as train_route
from app.rag.ask import help as ask_help, parser as ask_parser, route as ask_route
from app.rag.test import help as test_help, parser as test_parser, route as test_route

# Main parser
parser = argparse.ArgumentParser(
    formatter_class = argparse.ArgumentDefaultsHelpFormatter,
    description = 'Pilot of On-Premise RAG',
    parents = [top_parser],
    add_help = False,
)

# Commands
subparsers = parser.add_subparsers(
    title = 'commands',
    dest = 'command',
)

subparsers.add_parser(
    'doctor',
    help = doctor_help,
    description = doctor_parser.description,
    parents = [top_parser, common_parser, doctor_parser],
    add_help = False,
)

subparsers.add_parser(
    'train',
    help = train_help,
    description = train_parser.description,
    parents = [top_parser, common_parser, train_parser],
    add_help = False,
)

subparsers.add_parser(
    'test',
    help = test_help,
    description = test_parser.description,
    parents = [top_parser, common_parser, test_parser],
    add_help = False,
)

subparsers.add_parser(
    'ask',
    help = ask_help,
    description = ask_parser.description,
    parents = [top_parser, common_parser, ask_parser],
    add_help = False,
)

def main():
    args = parser.parse_args()

    command_message = f"with command: {args.command}" if args.command else ""
    logger.info(f"RAG Started {command_message}")
    
    setup_logger(args.log_level)
    logger.debug(f"Parsed arguments: {args}")

    if args.command == 'doctor':
        doctor_route(args)
    elif args.command == 'ask':
        ask_route(args)
    elif args.command == 'train':
        train_route(args)
    elif args.command == 'test':
        test_route(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
