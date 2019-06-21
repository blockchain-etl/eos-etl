import logging

from blockchainetl_common.jobs.exporters.console_item_exporter import ConsoleItemExporter
from blockchainetl_common.jobs.exporters.in_memory_item_exporter import InMemoryItemExporter
from eosetl.jobs.export_blocks_job import ExportBlocksJob

from eosetl.service.eos_service import EosService


class EosStreamerAdapter:
    def __init__(
            self,
            eos_rpc,
            item_exporter=ConsoleItemExporter(),
            batch_size=1,
            max_workers=5):
        self.eos_rpc = eos_rpc
        self.eos_service = EosService(eos_rpc)
        self.item_exporter = item_exporter
        self.batch_size = batch_size
        self.max_workers = max_workers

    def open(self):
        self.item_exporter.open()

    def get_current_block_number(self):
        return int(self.eos_service.get_latest_block().get('block_num'))

    def export_all(self, start_block, end_block):
        # Export blocks and transactions
        blocks_item_exporter = InMemoryItemExporter(item_types=['block', 'transaction', 'action'])

        blocks_job = ExportBlocksJob(
            start_block=start_block,
            end_block=end_block,
            batch_size=self.batch_size,
            eos_rpc=self.eos_rpc,
            max_workers=self.max_workers,
            item_exporter=blocks_item_exporter,
            export_blocks=True,
            export_transactions=True
        )
        blocks_job.run()

        blocks = blocks_item_exporter.get_items('block')
        transactions = blocks_item_exporter.get_items('transaction')
        actions = blocks_item_exporter.get_items('action')

        logging.info('Exporting with ' + type(self.item_exporter).__name__)
        self.item_exporter.export_items(blocks + transactions + actions)

    def close(self):
        self.item_exporter.close()
