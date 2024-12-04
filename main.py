import argparse
from repoinit import initialize_repo
from staging import stage_file
from commit_change import commit

def main():
    parser = argparse.ArgumentParser(description="PesaPal Simple version control system.")
    subparsers = parser.add_subparsers(dest="command")

    # 'init' command
    init_parser = subparsers.add_parser("init", help="Initialize a new repository.")
    init_parser.set_defaults(func=initialize_repo)

    # 'add' command
    add_parser = subparsers.add_parser("add", help="Stage a file.")
    add_parser.add_argument("file_path", help="Path to the file to be staged.")
    add_parser.set_defaults(func=stage_file)

    # 'commit' command
    commit_parser = subparsers.add_parser("commit", help="Commit staged changes.")
    commit_parser.add_argument("commit_message", help="Commit message.")
    commit_parser.set_defaults(func=commit)

    args = parser.parse_args()
    if args.command:
        # Check if a file path is provided for 'add'
        if args.command == "add":
            args.func(args.file_path)
        # Check if a commit message is provided for 'commit'
        elif args.command == "commit":
            args.func(args.commit_message)
        else:
            args.func()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
