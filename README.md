# GPTNutri

GPTNutri agora possui duas formas de uso:

1. **GitHub Pages (recomendado):** versão estática em `docs/` com deploy automático.
2. **FastAPI local:** versão backend em `app/` para rodar localmente.

## Acesso no GitHub Pages

Depois de habilitar Pages no repositório, o app fica disponível em:

`https://<seu-usuario>.github.io/<nome-do-repo>/`

### Como habilitar no GitHub

1. Faça push desta branch.
2. No GitHub, vá em **Settings > Pages**.
3. Em **Source**, selecione **GitHub Actions**.
4. Rode o workflow **Deploy static site to GitHub Pages** (ou faça um novo push).

O deploy usa o arquivo `.github/workflows/deploy-pages.yml` e publica a pasta `docs/`.

## Rodar localmente (FastAPI)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Abra `http://127.0.0.1:8000`.

## Testes

```bash
pytest -q
```
