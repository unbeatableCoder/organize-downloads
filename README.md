# organize-downloads

Script Python para organizar automaticamente ficheiros por extensão, movendo-os para as pastas padrão do utilizador (`~/Pictures`, `~/Videos`, `~/Music`, `~/Documents`, `~/Others`).

Usa apenas a standard library. Sem dependências.

## Funcionalidades

- Mapeamento de extensões para pastas de destino
- Criação automática das pastas se não existirem
- Prevenção de conflitos (sufixo numérico em vez de sobrescrever)
- Modo `--dry-run` para pré-visualizar sem mover nada
- Logs detalhados no terminal
- Integração opcional com `systemd --user` para correr automaticamente

## Instalação

```bash
mkdir -p ~/.local/bin
cp organize_downloads.py ~/.local/bin/
chmod +x ~/.local/bin/organize_downloads.py
```

Garante que `~/.local/bin` está no `PATH`:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## Uso

```bash
organize_downloads.py                # organiza ~/Downloads
organize_downloads.py -s /caminho     # organiza outra pasta
organize_downloads.py --dry-run       # mostra o que faria, sem mover
organize_downloads.py -v              # logs verbosos
```

## Automatização (systemd timer)

```bash
mkdir -p ~/.config/systemd/user
cp systemd/organize-downloads.service systemd/organize-downloads.timer ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now organize-downloads.timer
```

Verificar:

```bash
systemctl --user list-timers organize-downloads.timer
journalctl --user -u organize-downloads.service
```

## Mapeamento de extensões

| Categoria   | Extensões                                              | Destino        |
|-------------|---------------------------------------------------------|-----------------|
| Imagens     | png, jpg, jpeg, gif, webp, svg, bmp, tiff, heic, ico, raw | `~/Pictures`   |
| Vídeos      | mp4, mkv, avi, mov, webm, flv, wmv, m4v, mpeg            | `~/Videos`     |
| Áudio       | mp3, flac, wav, aac, ogg, m4a, opus, wma                 | `~/Music`      |
| Documentos  | pdf, docx, doc, txt, odt, xlsx, xls, pptx, ppt, epub, csv, md, rtf, ods | `~/Documents` |
| Outros      | qualquer outra extensão                                  | `~/Others`     |

## Licença

MIT. Ver [LICENSE](LICENSE).
