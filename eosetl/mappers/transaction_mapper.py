# MIT License
#
# Copyright (c) 2018 Omidiora Samuel, samparsky@gmail.com
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

from eosetl.mappers.transaction_input_mapper import BtcTransactionInputMapper
import json

# http://chainquery.com/bitcoin-api/getblock
# http://chainquery.com/bitcoin-api/getrawtransaction
class EosTransactionMapper(object):

    def __init__(self):
        self.transaction_input_mapper = BtcTransactionInputMapper()

    def transaction_to_dict(self, transaction, block = False):
        try:
            # remember to update
            # blocks_and_transactions_item_exporter.py as well

            if isinstance(transaction["trx"], str):
                # this is deferred transaction, it does not include any transaction data.
                # Example: {
                #   "status": "executed",
                #   "cpu_usage_us": 934,
                #   "net_usage_words": 0,
                #   "trx": "c962ca108b24828aca08abb4a62a1ce9392c565c6bc81aaada7ceb2cbdfafd8b"
                # }
                # todo: decide - what should we do about it?..
                # for now it's just ignored
                return

            block_hash = block['id'] if block else ""

            return {
                'type': 'transaction',
                'block_hash': block_hash,
                'status': transaction["status"],
                'cpu_usage_us': transaction["cpu_usage_us"],
                'net_usage_words': transaction["net_usage_words"],
                'trx.hash': transaction["trx"]["id"],
                'trx.signatures': transaction["trx"]["signatures"],
                'trx.compression': transaction["trx"]["compression"],
                'trx.packed_context_free_data': transaction["trx"]["packed_context_free_data"],
                'trx.context_free_data': transaction["trx"]["context_free_data"],
                'trx.packed_trx': transaction["trx"]["packed_trx"],
                'trx.transaction.expiration': transaction["trx"]["transaction"]["expiration"],
                'trx.transaction.ref_block_num': transaction["trx"]["transaction"]["ref_block_num"],
                'trx.transaction.ref_block_prefix': transaction["trx"]["transaction"]["ref_block_prefix"],
                'trx.transaction.max_net_usage_words': transaction["trx"]["transaction"]["max_net_usage_words"],
                'trx.transaction.max_cpu_usage_ms': transaction["trx"]["transaction"]["max_cpu_usage_ms"],
                'trx.transaction.delay_sec': transaction["trx"]["transaction"]["delay_sec"],
                'trx.transaction.transaction_extensions': transaction["trx"]["transaction"]["transaction_extensions"],
                'trx.transaction.actions': transaction["trx"]["transaction"]["actions"],
            }
        except Exception as e:
            print(f"Skipping transaction:\n{json.dumps(transaction)}\nfrom block id: {block_hash}\nbecause: {e}")
            return None
