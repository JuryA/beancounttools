import mt940
from beancount.core import amount, data
from beancount.core.number import D
from beancount.ingest import importer
from beancount.ingest.importers.mixins import identifier


class Importer(identifier.IdentifyMixin, importer.ImporterProtocol):
    """An importer for MT940 files."""

    def __init__(self, regexps, account):
        identifier.IdentifyMixin.__init__(self, matchers=[("filename", regexps)])
        self.account = account

    def identify(self, file):
        return False if file.mimetype() != "text/plain" else super().identify(file)

    def file_account(self, file):
        return self.account

    def extract(self, file, existing_entries):
        entries = []
        transactions = mt940.parse(file.contents())
        for trx in transactions:
            trxdata = trx.data
            metakv = {"ref": ref} if (ref := trxdata["bank_reference"]) else None
            meta = data.new_metadata(file.name, 0, metakv)
            date = trxdata["entry_date"] if "entry_date" in trxdata else trxdata["date"]
            entry = data.Transaction(
                meta,
                date,
                "*",
                self.prepare_payee(trxdata),
                self.prepare_narration(trxdata),
                data.EMPTY_SET,
                data.EMPTY_SET,
                [
                    data.Posting(
                        self.account,
                        amount.Amount(
                            D(trxdata["amount"].amount), trxdata["amount"].currency
                        ),
                        None,
                        None,
                        None,
                        None,
                    ),
                ],
            )
            entries.append(entry)

        return entries

    def prepare_payee(self, trxdata):
        return ""

    def prepare_narration(self, trxdata):
        return trxdata["transaction_details"] + " " + trxdata["extra_details"]
