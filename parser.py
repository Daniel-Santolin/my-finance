import pdfplumber
import re
import json
from pathlib import Path


class SantanderParser:

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def parse(self):

        transacoes = []

        with pdfplumber.open(self.pdf_path) as pdf:

            for pagina in pdf.pages:

                texto = pagina.extract_text()

                if not texto:
                    continue

                linhas = texto.split("\n")

                modo = None

                for linha in linhas:

                    linha = linha.strip()

                    if "Compras com Cartão de Débito" in linha:
                        modo = "cartao"
                        continue

                    if "Comprovantes de Pagamento" in linha:
                        modo = None

                    if modo == "cartao":

                        resultado = self.parse_cartao(linha)

                        if resultado:
                            transacoes.append(resultado)

        return transacoes

    def parse_cartao(self, linha):

        regex = re.compile(
            r"^(\d{2}/\d{2})\s+([\d\.]+)\s+(.*?)\s+([\d\.,]+)$"
        )

        match = regex.match(linha)

        if not match:
            return None

        data = match.group(1)

        cartao = match.group(2)

        descricao = match.group(3)

        valor = (
            match.group(4)
            .replace(".", "")
            .replace(",", ".")
        )

        return {
            "origem": "cartao_debito",
            "data": data,
            "cartao": cartao,
            "descricao": descricao.strip(),
            "valor": float(valor)
        }

    def exportar_json(self, destino):

        dados = self.parse()

        with open(destino, "w", encoding="utf-8") as file:
            json.dump(
                dados,
                file,
                indent=4,
                ensure_ascii=False
            )
