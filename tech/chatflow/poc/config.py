from __future__ import annotations

import argparse
import json

from settings import CONFIG_PATH, clear_config, get_model, masked_api_key, save_config


def main() -> None:
    parser = argparse.ArgumentParser(description="Configure XiaoAn MVP local runtime settings.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    set_parser = subparsers.add_parser("set", help="Set local model and/or OpenAI API key.")
    set_parser.add_argument("--model", help="OpenAI model, e.g. gpt-4o-mini or gpt-4o.")
    set_parser.add_argument("--api-key", help="OpenAI API key. Stored in a local user config file, not in repo.")

    subparsers.add_parser("show", help="Show current config with masked API key.")
    subparsers.add_parser("clear", help="Delete local config file.")

    args = parser.parse_args()

    if args.command == "set":
        if not args.model and not args.api_key:
            parser.error("config set requires --model and/or --api-key")
        path = save_config(model=args.model, api_key=args.api_key)
        print(f"saved={path}")
        print(f"model={get_model()}")
        print(f"api_key={masked_api_key() or '(not set)'}")
        return

    if args.command == "show":
        print(
            json.dumps(
                {
                    "config_path": str(CONFIG_PATH),
                    "model": get_model(),
                    "api_key": masked_api_key() or "(not set)",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    if args.command == "clear":
        clear_config()
        print(f"cleared={CONFIG_PATH}")


if __name__ == "__main__":
    main()
