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

import json

from eosetl.domain.transaction import BtcTransaction


class EosActionMapper(object):

    # def json_dict_to_transaction(self, json_dict, block=None):
    #     transaction = BtcTransaction()
    #     transaction.hash = json_dict.get('txid')
    #     transaction.size = json_dict.get('size')
    #     transaction.virtual_size = json_dict.get('vsize')
    #     transaction.version = json_dict.get('version')
    #     transaction.lock_time = json_dict.get('locktime')
    #
    #     if block is not None:
    #         transaction.block_number = block.number
    #
    #     transaction.block_hash = json_dict.get('blockhash')
    #     if block is not None:
    #         transaction.block_hash = block.hash
    #
    #     transaction.block_timestamp = json_dict.get('blocktime')
    #     if block is not None:
    #         transaction.block_timestamp = block.timestamp
    #
    #     transaction.inputs = self.transaction_input_mapper.vin_to_inputs(json_dict.get('vin'))
    #     transaction.outputs = self.transaction_output_mapper.vout_to_outputs(json_dict.get('vout'))
    #
    #     return transaction
    #
    def action_to_dict(self, action, tx_dict, block=None):
        try:
            # remember to update
            # blocks_and_transactions_item_exporter.py as well

            result = {
                'type': 'action',
                'transaction_hash': tx_dict['trx.hash'],
                'block_hash': tx_dict['block_hash'],
                'account': action["account"],
                'name': action["name"],
                'authorization': action["authorization"],
                'data': action["data"],
                'hex_data': action["hex_data"] if "hex_data" in action else "NULL",
            }

            action.pop('account', None)
            action.pop('name', None)
            action.pop('authorization', None)
            action.pop('data', None)
            action.pop('hex_data', None)
            # unset all this fields and check what's left
            if action != {}:
                print(f"raw action: {action}")

            return result
        except Exception as e:
            block_id = block['id'] if block is not None else "unknown"
            print(f"""
Skipping action{json.dumps(action)}
from transaction: {transaction_id}
from block id: {block_id}
because: {e}""")
            raise e
            return None
    #
    # def dict_to_transaction(self, dict):
    #     transaction = BtcTransaction()
    #     transaction.hash = dict.get('hash')
    #     transaction.size = dict.get('size')
    #     transaction.virtual_size = dict.get('virtual_size')
    #     transaction.version = dict.get('version')
    #     transaction.lock_time = dict.get('lock_time')
    #     transaction.block_number = dict.get('block_number')
    #     transaction.block_hash = dict.get('block_hash')
    #     transaction.block_timestamp = dict.get('block_timestamp')
    #     transaction.is_coinbase = dict.get('is_coinbase')
    #
    #     transaction.inputs = self.transaction_input_mapper.dicts_to_inputs(dict.get('inputs'))
    #     transaction.outputs = self.transaction_output_mapper.dicts_to_outputs(dict.get('outputs'))
    #
    #     return transaction
