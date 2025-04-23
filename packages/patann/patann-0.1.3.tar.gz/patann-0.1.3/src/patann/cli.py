# patann/cli.py
import argparse
import patann

def main():
    parser = argparse.ArgumentParser(description="PatANN: Pattern-Aware Approximate Nearest Neighbors Search")
    parser.add_argument('--help-examples', action='store_true', help='Show information about examples')
    parser.add_argument('--list-examples', action='store_true', help='List available examples')
    parser.add_argument('--copy-examples', metavar='DEST', nargs='?', const='.', 
                        help='Copy examples to specified directory (default: current directory)')
    
    args = parser.parse_args()
    
    if args.help_examples:
        patann.help()
    elif args.list_examples:
        patann.list_examples()
    elif args.copy_examples is not None:
        patann.copy_examples(args.copy_examples)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
