import re

from tariochbctools.importers.general import mt940importer


class ZkbImporter(mt940importer.Importer):
    def prepare_payee(self, trxdata):
        return ""

    def prepare_narration(self, trxdata):
        extra = trxdata["extra_details"]
        details = trxdata["transaction_details"]

        extraReplacements = {
            "Einkauf ZKB Maestro[- ]Karte": "",
            "LSV:.*": "LSV",
            "Gutschrift:.*": "Gutschrift",
            "eBanking:.*": "eBanking",
            "eBanking Mobile:.*": "eBanking Mobile",
            "E-Rechnung:.*": "E-Rechnung",
            "Kontouebertrag:.*": "Kontouebertrag:",
            "\\?ZKB:\\d+ ": "",
        }

        detailsReplacements = {
            "\\?ZI:\\?9:\\d": "",
            "\\?ZKB:\\d+": "",
            "Einkauf ZKB Maestro[- ]Karte Nr. \\d+,": "Maestro",
        }

        for pattern, replacement in extraReplacements.items():
            extra = re.sub(pattern, replacement, extra)

        for pattern, replacement in detailsReplacements.items():
            details = re.sub(pattern, replacement, details)

        return f"{extra.strip()}: {details.strip()}" if extra else details.strip()
