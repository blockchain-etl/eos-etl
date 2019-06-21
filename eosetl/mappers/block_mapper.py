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


from eosetl.domain.block import BtcBlock
from eosetl.mappers.transaction_mapper import EosTransactionMapper


class EosBlockMapper(object):
    def __init__(self, transaction_mapper=None):
        if transaction_mapper is None:
            self.transaction_mapper = EosTransactionMapper()
        else:
            self.transaction_mapper = transaction_mapper

    def block_to_dict(self, block):
        return {
            'type': 'block',
            'hash': block["id"],
            'block_num': block["block_num"],
            'ref_block_prefix': block["ref_block_prefix"],
            'previous': block["previous"],
            'action_mroot': block["action_mroot"],
            'transaction_mroot': block["transaction_mroot"],
            'new_producers': block["new_producers"],
            'header_extensions': block["header_extensions"],
            'block_extensions': block["block_extensions"],
            'timestamp': block["timestamp"],
            'producer': block["producer"],
            'transaction_count': len(block["transactions"])
        }


def to_hex(val):
    if val is None:
        return None

    if isinstance(val, str):
        return val
    elif isinstance(val, int):
        return format(val, 'x')
    else:
        return val
