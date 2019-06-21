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


class EosService(object):
    def __init__(self, eos_rpc):
        self.eos_rpc = eos_rpc
        self.block_mapper = EosBlockMapper()
        self.transaction_mapper = EosTransactionMapper()
        self.action_mapper = EosActionMapper()

    def get_block(self, block_number):
        return self.eos_rpc.getblock(block_number)

    def get_genesis_block(self):
        return self.get_block(1)

    def get_latest_block(self):
        last_irreversible_block_id = self.eos_rpc.get_info()["last_irreversible_block_id"]
        return self.get_block(last_irreversible_block_id)

    def get_blocks(self, block_number_batch):
        if not block_number_batch:
            return []

        return [self.get_block(x) for x in block_number_batch]
