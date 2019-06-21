# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
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

from blockchainetl.utils import rpc_response_batch_to_results
from eosetl.enumeration.chain import Chain
from eosetl.json_rpc_requests import generate_get_block_hash_by_number_json_rpc
from eosetl.mappers.action_mapper import EosActionMapper
from eosetl.mappers.block_mapper import EosBlockMapper
from eosetl.mappers.transaction_mapper import EosTransactionMapper


class EosService(object):
    def __init__(self, eos_rpc):
        self.eos_rpc = eos_rpc
        self.block_mapper = EosBlockMapper()
        self.transaction_mapper = EosTransactionMapper()
        self.action_mapper = EosActionMapper()

    def get_block(self, block_number, with_transactions=False):
        return self.eos_rpc.getblock(block_number)

    def get_genesis_block(self, with_transactions=False):
        return self.get_block(1, with_transactions)

    def get_latest_block(self, with_transactions=False):
        last_irreversible_block_id = self.eos_rpc.get_info()["last_irreversible_block_id"]
        return self.get_block(last_irreversible_block_id, with_transactions)

    def get_blocks(self, block_number_batch, with_transactions=False):
        if not block_number_batch:
            return []

        return [self.get_block(x) for x in block_number_batch]

        # block_hashes = self.get_block_hashes(block_number_batch)
        # return self.get_blocks_by_hashes(block_hashes, with_transactions)

    def get_block_hashes(self, block_number_batch):
        block_hash_rpc = list(generate_get_block_hash_by_number_json_rpc(block_number_batch))
        block_hashes_response = self.eos_rpc.batch(block_hash_rpc)
        block_hashes = rpc_response_batch_to_results(block_hashes_response)
        return block_hashes

ADDRESS_TYPE_SHIELDED = 'shielded'
