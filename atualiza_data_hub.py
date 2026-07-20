# -*- coding: utf-8 -*-
"""
Atualiza a data "Atualizado DD/MM/AAAA" do card de um dashboard no hub
(https://hapvida-hub.vercel.app/  ->  index.html).

Uso:
    python atualiza_data_hub.py vendas      # card "Vendas Diaria 2026"
    python atualiza_data_hub.py conversao   # card "Conversao do Time"
    python atualiza_data_hub.py vendas --data 24/06/2026   # data explicita

Sem --data usa a data de hoje. Identifica o card pelo href (robusto a
reordenacao dos cards). NAO da commit/push (a skill cuida disso).
"""
import re, sys, argparse, datetime, os

HERE = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(HERE, "index.html")

# chave -> trecho do href que identifica o card
CARDS = {
    "vendas":         "vendas-diaria-deploy.vercel.app",
    "conversao":      "conversao-time.vercel.app",
    "atendimento":    "atendimento-hapvida.vercel.app",
    "redermsp":       "redermsprj.vercel.app",
    "vendas_digital": "vendas-digital-2025-2026.vercel.app",
    "ofertaplanos":   "ofertaplanos.vercel.app",
    "gup":            "leads-gup.vercel.app",
    "eugenia":        "eugenia-seven.vercel.app",
    "quem_indica":    "quem-indica.vercel.app",
    "cac":            "cac-vgfq.vercel.app",
    "extrato":        "painelvendedores-hap.vercel.app",
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("card", choices=sorted(CARDS), help="qual card atualizar")
    ap.add_argument("--data", default=None, help="DD/MM/AAAA (default: hoje)")
    a = ap.parse_args()

    data = a.data or datetime.date.today().strftime("%d/%m/%Y")
    href = CARDS[a.card]

    html = open(INDEX, encoding="utf-8").read()

    # localiza o bloco <a ... href="...href...">...</a> e troca a 1a data dentro dele
    pat = re.compile(
        r'(<a class="dash-card"[^>]*href="[^"]*' + re.escape(href) +
        r'[^"]*"[^>]*>.*?Atualizado )\d{2}/\d{2}/\d{4}',
        re.DOTALL,
    )
    new, n = pat.subn(lambda m: m.group(1) + data, html, count=1)
    if n != 1:
        sys.exit(f"ERRO: card '{a.card}' (href ~ {href}) nao encontrado em index.html")

    open(INDEX, "w", encoding="utf-8").write(new)
    print(f"OK: card '{a.card}' -> Atualizado {data}")

if __name__ == "__main__":
    main()
