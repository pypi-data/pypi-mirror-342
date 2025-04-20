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


def sync_file(src_path, dest_path, mirror_base, dry_run=False):
    src_path = Path(src_path).expanduser().resolve()
    dest_path = Path(dest_path).expanduser()
    rel_path = src_path.name
    mirror_path = mirror_base / rel_path

    mirror_path.parent.mkdir(parents=True, exist_ok=True)

    needs_update = not mirror_path.exists() or sha256sum(src_path) != sha256sum(mirror_path)
    needs_link = not dest_path.exists() or not dest_path.is_symlink() or dest_path.resolve() != mirror_path.resolve()

    copied = linked = False

    if dry_run:
        if needs_update:
            print(f"{Fore.YELLOW}[DRY RUN] Would copy {src_path} -> {mirror_path}")
        if needs_link:
            print(f"{Fore.YELLOW}[DRY RUN] Would symlink {dest_path} -> {mirror_path}")
    else:
        if needs_update:
            if mirror_path.exists():
                mirror_path.chmod(0o644)
            shutil.copy2(src_path, mirror_path)
            mirror_path.chmod(0o444)
            print(f"{Fore.GREEN}Copied and locked: {src_path} -> {mirror_path}")
            copied = True

        if needs_link:
            if dest_path.exists() or dest_path.is_symlink():
                dest_path.unlink()
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            dest_path.symlink_to(mirror_path)
            print(f"{Fore.GREEN}Linked: {dest_path} -> {mirror_path}")
            linked = True

    return copied, linked


def sync_directory(src_dir, dest_dir, mirror_base, dry_run=False):
    src_dir = Path(src_dir).expanduser().resolve()
    dest_dir = Path(dest_dir).expanduser()
    mirror_subdir = mirror_base / src_dir.name

    copied_count = linked_count = 0

    for file_path in src_dir.rglob("*"):
        if file_path.is_file():
            relative_path = file_path.relative_to(src_dir)
            mirror_path = mirror_subdir / relative_path
            dest_path = dest_dir / relative_path

            copied, linked = sync_file(file_path, dest_path, mirror_path.parent, dry_run=dry_run)
            copied_count += copied
            linked_count += linked

    return copied_count, linked_count


def load_config(config_path):
    config = toml.load(config_path)
    mirror = Path(config["settings"]["mirror"]).expanduser()
    mappings = config.get("files", [])
    return mirror, mappings

def print_group_header(name):
    print(f"\n{Style.BRIGHT}{Fore.CYAN} Syncing: {name}{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(description="Sync dotfiles (file & dir) with read-only mirror and symlinks.")
    parser.add_argument("--config", default="dotfiles_config.toml", help="Path to TOML config file")
    parser.add_argument("--dry-run", action="store_true", help="Simulate the sync without making changes")
    args = parser.parse_args()

    mirror, file_mappings = load_config(args.config)
    mirror.mkdir(parents=True, exist_ok=True)

    for mapping in file_mappings:
        src = Path(mapping["source"]).expanduser().resolve()
        dst = Path(mapping["destination"]).expanduser()
        kind = mapping.get("type", "file")

        group_name = src.name if kind == "dir" else src.parent.name
        print_group_header(group_name)

        copied = linked = 0

        if kind == "dir":
            copied, linked = sync_directory(src, dst, mirror, dry_run=args.dry_run)
        elif kind == "file":
            copied, linked = sync_file(src, dst, mirror / group_name, dry_run=args.dry_run)
        else:
            print(f"{Fore.RED}Unknown type '{kind}' for {src}")

        # Print group stats
        if args.dry_run:
            tag = f"{Fore.YELLOW}[DRY RUN]"
        else:
            tag = f"{Fore.GREEN}󰄬"

        if copied == 0 and linked == 0:
            print(f"{tag} No changes")
        else:
            print(f"{tag} {copied} file(s) updated, {linked} symlink(s) created")

def cli():
    main()

if __name__ == "__main__":
    cli()