import sys
import argparse
import aadish

def main():
    parser = argparse.ArgumentParser(
        description='Aadish: CLI AI assistant',
        epilog='''Examples:\n  python -m aadish --talk\n  python -m aadish --model gemma "What is the weather today?"\n  python -m aadish --model llama3.3 --system "Reply like a poet." "Tell me about love"\n''',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--talk', action='store_true', help='Start interactive chat')
    parser.add_argument('--model', default='compound', help='Model name or ID')
    parser.add_argument('--system', help='Override system prompt')
    parser.add_argument('message', nargs=argparse.REMAINDER, help='Message to send')
    args = parser.parse_args()

    if args.talk:
        aadish.aadishtalk(model=args.model, system=args.system)
    else:
        msg = ' '.join(args.message).strip()
        if not msg:
            print("Error: No message provided.")
            sys.exit(1)
        aadish.aadish(msg, model=args.model, system=args.system)

if __name__ == "__main__":
    main()
