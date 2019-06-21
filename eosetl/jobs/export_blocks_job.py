# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com, Vasiliy Bondarenko vabondarenko@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from eosetl.mappers.action_mapper import EosActionMapper
from eosetl.mappers.block_mapper import EosBlockMapper
from eosetl.mappers.transaction_mapper import EosTransactionMapper
from eosetl.service.eos_service import EosService
from blockchainetl.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl.jobs.base_job import BaseJob
from blockchainetl.utils import validate_range


# Exports blocks and transactions
class ExportBlocksJob(BaseJob):
    def __init__(
            self,
            start_block,
            end_block,
            batch_size,
            eos_rpc,
            max_workers,
            item_exporter,
            chain,
            export_blocks=True,
            export_transactions=True):
        validate_range(start_block, end_block)
        self.start_block = start_block
        self.end_block = end_block

        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)
        self.item_exporter = item_exporter

        self.export_blocks = export_blocks
        self.export_transactions = export_transactions
        if not self.export_blocks and not self.export_transactions:
            raise ValueError('At least one of export_blocks or export_transactions must be True')

        self.eos_service = EosService(eos_rpc)
        self.block_mapper = EosBlockMapper()
        self.transaction_mapper = EosTransactionMapper()
        self.action_mapper = EosActionMapper()

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        self.batch_work_executor.execute(
            range(self.start_block, self.end_block + 1),
            self._export_batch,
            total_items=self.end_block - self.start_block + 1
        )

    def _export_batch(self, block_number_batch):
        blocks = self.eos_service.get_blocks(block_number_batch, self.export_transactions)
        for block in blocks:
            self._export_block(block)
            self._export_transactions(block)

    def _export_block(self, block):
        if not self.export_blocks:
            return

        self.item_exporter.export_item(self.block_mapper.block_to_dict(block))

    def _export_transactions(self, block):
        if not self.export_transactions:
            return

        for transaction in block["transactions"]:
            self._export_transaction(transaction, block)

    def _export_transaction(self, transaction, block):
        transaction_dict = self.transaction_mapper.transaction_to_dict(transaction, block)
        if not transaction_dict: # skip in None returned
            return

        self.item_exporter.export_item(transaction_dict)
        if transaction_dict.get("trx.transaction.actions") is None:
            return

        for action in transaction_dict["trx.transaction.actions"]:
            action_dict = self.action_mapper.action_to_dict(action, transaction_dict, block)
            self.item_exporter.export_item(action_dict)

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()
