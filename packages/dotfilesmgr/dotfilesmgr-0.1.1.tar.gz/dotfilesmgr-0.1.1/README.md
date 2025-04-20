## Dotfilesmgr
Simple tool to manage your dotfiles.
### Installation
```bash
pip install dotfilesmgr
```
### Configutation
```toml
[settings]
mirror = "/home/<your_name>/.dotfile_mirror"

[[files]]
source = "/home/<your_name>/dotfiles/kitty"
destination = "/home/<your_name>/.config/kitty"
type = "dir"

[[files]]
source = "/home/<your_name>/dotfiles/.condarc"
destination = "/home/<your_name>/.condarc"
type = "file"
```
#### TODO's
- better configuration
- documentation
- better terminal output