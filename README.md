
## v1.2 (containerized GUI on Fedora GNOME)
- Tkinter GUI runs in its own container
- Connects to host Ollama via `OLLAMA_HOST`
- Uses `xhost +local:` and `--security-opt label=disable` to avoid SELinux/XWayland issues
- Run: `./gui-run.sh` (bind-mounts `bin/` and opens the GUI)
