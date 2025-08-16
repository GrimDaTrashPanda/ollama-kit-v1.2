# Ollama-Kit v1.2 – Full Container

## Full AI Stack Download
The complete Ollama Kit v1.2 (backend container + GUI container) is available here:

- [Direct ZIP Download – 17.6 GB](https://archive.org/download/ollama-kit-v1.2-full-container/ollama-kit-v1.2-full-container.zip)
- [Optional Torrent Download](https://archive.org/download/ollama-kit-v1.2-full-container/ollama-kit-v1.2-full-container_archive.torrent)

For a code-only setup (no models or containers), see this repository.

---

## Ollama-Kit v1.2 – Portable AI Stack

### WHAT THIS IS
This release builds on v1.1 by containerizing the **Gramified Tkinter GUI** to solve SELinux/XWayland issues on Fedora GNOME.

**Contents:**
- Ollama backend container (same as v1.1, prepped for models)
- Gramified Tkinter GUI in its own Podman container
- `gui.Dockerfile` and `gui-run.sh` for reproducibility
- Updated `requirements.txt` (tkhtmlview, duckduckgo-search, ollama)

### WHY IT'S COOL
- Fedora GNOME safe – GUI no longer depends on host python3-tk  
- Two-container workflow – clean separation of backend and GUI  
- Portable – copy to another Linux machine with Podman, works offline  
- Reproducible – rebuild GUI container with included Dockerfile  

---

## HOW TO USE (Generic Linux)

1. Install prerequisites:
```bash
sudo dnf install -y podman xorg-x11-server-Xwayland xorg-x11-xauth
xhost +local:
```

2. Copy the `ollama-kit-v1.2-full_container` folder to your machine.

3. Run Ollama backend (same as v1.1):
```bash
cd ollama-kit-v1.2-full_container/container
podman run -d --name ollama -p 11434:11434 \
  -v "$HOME/.ollama:/root/.ollama" \
  --security-opt label=disable \
  docker.io/ollama/ollama:0.11.4
```

4. Launch the Gramified GUI:
```bash
cd ollama-kit-v1.2-full_container
./gui-run.sh
```

---

## HOW TO USE (WSL – Windows Subsystem for Linux)

For Debian inside WSL, setup is the same as v1.1, except the GUI now runs in its own container:
```bash
cd ~/ai-stack/ollama-kit-v1.2
./gui-run.sh
```

All backend/container steps remain the same as v1.1.

---

## NOTES

* Models live in the `models/` folder – offline once copied  
* To update Ollama inside the backend container:
```bash
podman pull docker.io/ollama/ollama:<version>
podman restart ollama
```
* To rebuild the GUI container if needed:
```bash
cd ollama-kit-v1.2-full_container
podman build -t localhost/gramified-gui:v1.2 -f gui.Dockerfile .
```

---

## VERSION

* v1.1 – Initial full container release with models + GUI (host Tkinter)  
* v1.2 – GUI containerized for Fedora GNOME (SELinux/XWayland safe)  

---

## License

MIT

