import shutil
import hashlib
import argparse
import toml
from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)

def sha256sum(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def sync_file(src_path, dest_path, store_base, log_file=None):
    src_path = Path(src_path).expanduser().resolve()
    dest_path = Path(dest_path).expanduser()
    rel_path = src_path.name
    store_path = store_base / rel_path

    store_path.parent.mkdir(parents=True, exist_ok=True)

    needs_update = not store_path.exists() or sha256sum(src_path) != sha256sum(store_path)
    needs_link = not dest_path.exists() or not dest_path.is_symlink() or dest_path.resolve() != store_path.resolve()

    copied = linked = False

    if needs_update:
        if store_path.exists():
            store_path.chmod(0o644)
        shutil.copy2(src_path, store_path)
        store_path.chmod(0o444)
        print(f"{Fore.GREEN}Copied and locked: {src_path} -> {store_path}")
        copied = True

    if needs_link:
        if dest_path.exists() or dest_path.is_symlink():
            dest_path.unlink()
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.symlink_to(store_path)
        print(f"{Fore.GREEN}Linked: {store_path} -> {dest_path}")
        linked = True

    # Log the sync details
    if log_file:
        with open(log_file, 'a') as f:
            f.write(f"Synced: {store_path} -> {dest_path}\n")

    return int(copied), int(linked)

def sync_directory(src_dir, dest_dir, store_base, log_file=None):
    src_dir = Path(src_dir).expanduser().resolve()
    dest_dir = Path(dest_dir).expanduser()
    store_subdir = store_base / src_dir.name

    copied_count = linked_count = 0

    for file_path in src_dir.rglob("*"):
        if file_path.is_file():
            relative_path = file_path.relative_to(src_dir)
            store_path = store_subdir / relative_path
            dest_path = dest_dir / relative_path

            copied, linked = sync_file(file_path, dest_path, store_path.parent, log_file=log_file)
            copied_count += copied
            linked_count += linked

    return copied_count, linked_count

def load_config(config_path):
    config_path = Path(config_path).expanduser()

    if not config_path.exists():
        print(f"{Fore.RED}Config file not found: {config_path}")
        exit(1)

    try:
        config = toml.load(config_path)
    except toml.TomlDecodeError as e:
        print(f"{Fore.RED}Failed to parse TOML config: {e}")
        exit(1)

    dotfiles_root = Path(config.get("settings", {}).get("dotfiles_dir", "")).expanduser().resolve()
    mappings = []

    for program, entry in config.items():
        if program == "settings":
            continue

        if not isinstance(entry, dict):
            print(f"{Fore.RED}Invalid config entry for [{program}] – expected a table.")
            continue

        try:
            raw_source = entry["source"]
            destination = Path(entry["destination"]).expanduser()
        except KeyError as e:
            print(f"{Fore.RED}Missing key '{e.args[0]}' in [{program}] config.")
            continue

        if raw_source.startswith("./"):
            if dotfiles_root:
                source = (dotfiles_root / raw_source[2:]).resolve()
            else:
                print(f"{Fore.RED}Relative source '{raw_source}' in [{program}] but no dotfiles_dir defined.")
                continue
        else:
            source = Path(raw_source).expanduser().resolve()

        if not source.exists():
            print(f"{Fore.YELLOW}Source path does not exist yet: {source} (in [{program}])")

        kind = "dir" if source.is_dir() else "file"

        mappings.append({
            "program": program,
            "source": source,
            "destination": destination,
            "type": kind
        })

    return mappings

def print_group_header(name):
    print(f"\n{Style.BRIGHT}{Fore.CYAN} Syncing: {name}{Style.RESET_ALL}")

def list_symlinks(store):
    store.mkdir(parents=True, exist_ok=True)

    log_file = store / 'sync_log.txt'
    if log_file.exists():
        with open(log_file, 'r') as f:
            logs = f.readlines()

        if logs:
            print(f"{Style.BRIGHT}{Fore.BLUE}Listing symlinks from sync log:{Style.RESET_ALL}")
            for log in logs:
                print(f"  {Fore.GREEN}{log.strip()}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}No symlinks found in the sync log.")
    else:
        print(f"{Fore.YELLOW}No sync log found in the store.")

def remove_symlinks(store):
    log_file = store / 'sync_log.txt'
    if not log_file.exists():
        print(f"{Fore.YELLOW}No sync log found in the store.")
        return

    with open(log_file, 'r') as f:
        logs = f.readlines()

    if not logs:
        print(f"{Fore.YELLOW}No symlinks found in the sync log to remove.")
        return

    print(f"{Style.BRIGHT}{Fore.RED}Removing the following symlinks:{Style.RESET_ALL}")
    for log in logs:
        log = log.strip()
        if log.startswith("Synced: ") and " -> " in log:
            try:
                _, paths = log.split("Synced: ", 1)
                store_path_str, dest_path_str = paths.split(" -> ")
                dest_path = Path(dest_path_str.strip())

                if dest_path.exists() and dest_path.is_symlink():
                    dest_path.unlink()
                    print(f"{Fore.RED}Removed symlink: {dest_path}")
                else:
                    print(f"{Fore.YELLOW}Symlink not found or not a symlink: {dest_path}")
            except ValueError:
                print(f"{Fore.YELLOW}Malformed log line: {log}")
                continue

    log_file.unlink()
    print(f"{Fore.GREEN}Removal completed and log file cleared.")


def main():
    parser = argparse.ArgumentParser(description="Sync dotfiles (file & dir) with a read-only store and symlinks.")
    parser.add_argument("-c", "--config", default="dotfiles_config.toml", help="Path to TOML config file")
    parser.add_argument("-s", "--sync", action="store_true", help="Perform dotfile syncing")
    parser.add_argument("-l", "--list", action="store_true", help="List synced symlinks")
    parser.add_argument("-r", "--remove", action="store_true", help="Remove the currently active symlinks")
    args = parser.parse_args()

    # Hardcoded store path
    store = Path("~/.local/share/dotfiles_store").expanduser()

    if args.list:
        list_symlinks(store)
        return

    if args.remove:
        remove_symlinks(store)  # Removes symlinks based on the sync log
        return

    # Clear the log file at the beginning of sync
    log_file = store / 'sync_log.txt'
    if log_file.exists():
        log_file.unlink()  # This clears the log file

    file_mappings = load_config(args.config)
    store.mkdir(parents=True, exist_ok=True)

    for mapping in file_mappings:
        src = Path(mapping["source"]).expanduser().resolve()
        dst = Path(mapping["destination"]).expanduser()
        kind = mapping["type"]
        group_name = mapping["program"]

        print_group_header(group_name)

        if kind == "dir":
            copied, linked = sync_directory(src, dst, store, log_file=log_file)
        elif kind == "file":
            copied, linked = sync_file(src, dst, store / group_name, log_file=log_file)
        else:
            print(f"{Fore.RED}Unknown type '{kind}' for {src}")
            copied = linked = 0

        tag = f"{Fore.YELLOW}[DRY RUN]" if not args.sync else f"{Fore.GREEN}󰄬"

        if copied == 0 and linked == 0:
            print(f"{tag} No changes")
        else:
            print(f"{tag} {copied} file(s) updated, {linked} symlink(s) created")


def cli():
    main()

if __name__ == "__main__":
    cli()
