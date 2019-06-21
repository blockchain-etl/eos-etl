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


from blockchainetl_common.jobs.exporters.composite_item_exporter import CompositeItemExporter

BLOCK_FIELDS_TO_EXPORT = [
    'hash',
    'block_num',
    'ref_block_prefix',
    'previous',
    'action_mroot',
    'transaction_mroot',
    'new_producers',
    'header_extensions',
    'block_extensions',
    'timestamp',
    'producer',
    'transaction_count'
]

TRANSACTION_FIELDS_TO_EXPORT = [
    'block_hash',
    'status',
    'cpu_usage_us',
    'net_usage_words',
    'trx.hash',
    'trx.signatures',
    'trx.compression',
    'trx.packed_context_free_data',
    'trx.context_free_data',
    'trx.packed_trx',
    'trx.transaction.expiration',
    'trx.transaction.ref_block_num',
    'trx.transaction.ref_block_prefix',
    'trx.transaction.max_net_usage_words',
    'trx.transaction.max_cpu_usage_ms',
    'trx.transaction.delay_sec',
    'trx.transaction.transaction_extensions',
]

ACTION_FIELDS_TO_EXPORT = [
    'transaction_hash',
    'block_hash',
    "account",
    "name",
    "authorization",
    "data",
    "hex_data",
]


def blocks_and_transactions_item_exporter(blocks_output=None, transactions_output=None, actions_output=None):
    filename_mapping = {}
    field_mapping = {}

    if blocks_output is not None:
        filename_mapping['block'] = blocks_output
        field_mapping['block'] = BLOCK_FIELDS_TO_EXPORT

    if transactions_output is not None:
        filename_mapping['transaction'] = transactions_output
        field_mapping['transaction'] = TRANSACTION_FIELDS_TO_EXPORT

    if actions_output is not None:
        filename_mapping['action'] = actions_output
        field_mapping['action'] = ACTION_FIELDS_TO_EXPORT

    return CompositeItemExporter(
        filename_mapping=filename_mapping,
        field_mapping=field_mapping
    )
