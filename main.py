from parser import SantanderParser

parser = SantanderParser(
    "entries/2026-06.pdf"
)

parser.exportar_json(
    "parsed-jsons/2026-06.json"
)

print("Importação concluída.")