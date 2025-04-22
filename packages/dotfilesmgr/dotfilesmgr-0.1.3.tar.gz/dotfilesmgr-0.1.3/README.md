## Dotfilesmgr
Simple tool to manage your dotfiles.
### Installation
```bash
pipx install dotfilesmgr
```
### Options
```bash
  -h, --help           show this help message and exit
  -c, --config CONFIG  Path to TOML config file
  -s, --sync           Perform dotfile syncing
  -l, --list           List synced symlinks
  -r, --remove         Remove the currently active symlinks
```
### Configutation
```toml
[settings]
dotfiles_dir = "~/dotfiles"  # optional, used as base for relative sources

[kitty]
source = "./kitty"
destination = "~/.config/kitty"

[nvim]
source = "./nvim/init.lua"
destination = "~/.config/test/nvim/init.lua"

[custom_script]
source = "~/scripts/special_config.sh"  # absolute path, ignored dotfiles_dir
destination = "~/.config/special.sh"
```
#### TODO's
- documentation
- better terminal output