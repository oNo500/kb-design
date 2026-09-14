"""Compatibility entry point for the shared display rebase implementation."""
import argparse
import json
from pathlib import Path
from kb_vocab.display import rebase_display


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--previous',required=True,type=Path)
    parser.add_argument('--base',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    print(json.dumps(rebase_display(args.previous,args.base,args.output),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
