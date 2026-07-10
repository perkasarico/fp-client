"""CLI interface for fp-client."""

import argparse
import json
import sys
import os

from fp_client import FPClient


def cmd_health(args):
    """Check API health."""
    with FPClient(base_url=args.url, token=args.token) as client:
        result = client.health()
        print(json.dumps(result, indent=2))


def cmd_generate(args):
    """Generate fingerprint(s)."""
    with FPClient(base_url=args.url, token=args.token) as client:
        result = client.generate(
            count=args.count,
            proxy=args.proxy,
            chrome=args.chrome,
            target=args.target,
            encrypt=not args.no_encrypt,
            pretty=args.pretty,
        )
        print(json.dumps(result.model_dump(), indent=2 if args.pretty else None, by_alias=True))


def cmd_stats(args):
    """Show cache stats."""
    with FPClient(base_url=args.url, token=args.token) as client:
        result = client.stats()
        print(json.dumps(result.model_dump(), indent=2))


def cmd_export(args):
    """Generate and export fingerprints to file."""
    with FPClient(base_url=args.url, token=args.token) as client:
        result = client.generate(
            count=args.count,
            proxy=args.proxy,
            chrome=args.chrome,
            target=args.target,
            encrypt=not args.no_encrypt,
        )
        data = result.model_dump(by_alias=True)
        with open(args.output, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Exported {args.count} fingerprint(s) to {args.output}")


def main():
    parser = argparse.ArgumentParser(
        prog="fp-client",
        description="Fingerprint Generator API client",
    )
    parser.add_argument(
        "--url", default=os.getenv("FP_URL", "https://fp.mahiru.my.id"),
        help="API base URL (default: env FP_URL or public endpoint)",
    )
    parser.add_argument(
        "--token", default=os.getenv("FP_TOKEN"),
        help="Bearer token (default: env FP_TOKEN)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # health
    sub.add_parser("health", help="Check API health")

    # generate
    p_gen = sub.add_parser("generate", help="Generate fingerprint(s)")
    p_gen.add_argument("-n", "--count", type=int, default=1, help="Number of fingerprints (1-100)")
    p_gen.add_argument("-p", "--proxy", help="Proxy URL to bind identity to")
    p_gen.add_argument("--chrome", type=int, help="Pin Chrome major version")
    p_gen.add_argument("--target", default="amazon", help="Antibot target (default: amazon)")
    p_gen.add_argument("--no-encrypt", action="store_true", help="Omit encrypted payload")
    p_gen.add_argument("--pretty", action="store_true", help="Pretty-print JSON")

    # stats
    sub.add_parser("stats", help="Show cache statistics")

    # export
    p_exp = sub.add_parser("export", help="Generate and export to file")
    p_exp.add_argument("-o", "--output", required=True, help="Output file path")
    p_exp.add_argument("-n", "--count", type=int, default=1, help="Number of fingerprints")
    p_exp.add_argument("-p", "--proxy", help="Proxy URL to bind identity to")
    p_exp.add_argument("--chrome", type=int, help="Pin Chrome major version")
    p_exp.add_argument("--target", default="amazon", help="Antibot target")
    p_exp.add_argument("--no-encrypt", action="store_true", help="Omit encrypted payload")

    args = parser.parse_args()
    cmds = {
        "health": cmd_health,
        "generate": cmd_generate,
        "stats": cmd_stats,
        "export": cmd_export,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
