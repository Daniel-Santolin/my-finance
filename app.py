# from importers.importer_santander import SantanderImporter
from pathlib import Path
from parsers.parser_santander import SantanderParser
from database import db
from models.transaction import Transaction

entries = Path("entries")
output = Path("parsed-jsons")
accounts = (
    'Santander',
    'Santader - Cartão',
    'Itaú',
    'Íon'
)

def parseAccount(account):
    print(f"> Parsing: {account}")
    for pdf_path in sorted(entries_dir.glob("*.pdf")):
        output_path = output_dir / f"{pdf_path.stem}.json"
        parser_type = f"{account}Parser"
        parser = globals()[parser_type](str(pdf_path))
        parser.exportar_json(str(output_path))

        print(f"|Parse concluded: {pdf_path.name}")

# def importAccount(account):
#     print(f"> Importing: {account}")
#     for json_path in sorted(output_dir.glob("*.json")):
#         importer_type = f"{account}Importer"
#         importer = globals()[importer_type](str(json_path))
#         importer.importar()

#         print(f"|Import concluded: {json_path.name}")

for account in accounts:
    entries_dir = entries / account
    output_dir = output / account

    output_dir.mkdir(parents=True, exist_ok=True)

    parseAccount(account)
    # importAccount(account)