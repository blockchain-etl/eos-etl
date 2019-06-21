# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com, Vasiliy Bondarenko, vabondarenko@gmail.com
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


import click
from blockchainetl_common.streaming.streaming_utils import configure_logging, configure_signals
from eosetl.rpc.eos_rpc import EosRpc

from blockchainetl_common.logging_utils import logging_basic_config
from blockchainetl_common.thread_local_proxy import ThreadLocalProxy

logging_basic_config()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-l', '--last-synced-block-file', default='last_synced_block.txt', type=str, help='')
@click.option('--lag', default=0, type=int, help='The number of blocks to lag behind the network.')
@click.option('-p', '--provider-uri', default='http://api.main.alohaeos.com', type=str,
              help='The URI of the remote EOS node')
@click.option('-o', '--output', type=str,
              help='Google PubSub topic path e.g. projects/your-project/topics/crypto_eos. '
                   'If not specified will print to console')
@click.option('-s', '--start-block', default=None, type=int, help='Start block')
@click.option('--period-seconds', default=10, type=int, help='How many seconds to sleep between syncs')
@click.option('-b', '--batch-size', default=1, type=int, help='How many blocks to batch in single request')
@click.option('-B', '--block-batch-size', default=1, type=int, help='How many blocks to batch in single sync round')
@click.option('-w', '--max-workers', default=5, type=int, help='The number of workers')
@click.option('--log-file', default=None, type=str, help='Log file')
@click.option('--pid-file', default=None, type=str, help='pid file')
def stream(last_synced_block_file, lag, provider_uri, output, start_block,
           period_seconds=10, batch_size=1, block_batch_size=1, max_workers=5, log_file=None, pid_file=None):
    """Streams all data types to console or Google Pub/Sub."""
    configure_logging(log_file)
    configure_signals()

    from blockchainetl_common.streaming.streaming_utils import get_item_exporter
    from eosetl.streaming.eos_streamer_adapter import EosStreamerAdapter
    from blockchainetl_common.streaming.streamer import Streamer

    streamer_adapter = EosStreamerAdapter(
        eos_rpc=ThreadLocalProxy(lambda: EosRpc(provider_uri)),
        item_exporter=get_item_exporter(output),
        batch_size=batch_size,
        max_workers=max_workers
    )
    streamer = Streamer(
        blockchain_streamer_adapter=streamer_adapter,
        last_synced_block_file=last_synced_block_file,
        lag=lag,
        start_block=start_block,
        period_seconds=period_seconds,
        block_batch_size=block_batch_size,
        pid_file=pid_file,
    )
    streamer.stream()
