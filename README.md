# EOS ETL

[![Join the chat at https://gitter.im/ethereum-eth](https://badges.gitter.im/ethereum-etl.svg)](https://gitter.im/ethereum-etl/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/blockchain-etl/eos-etl.png)](https://travis-ci.org/blockchain-etl/eos-etl)
[Join Telegram Group](https://t.me/joinchat/GsMpbA3mv1OJ6YMp3T5ORQ)

Install EOS ETL:

```bash
pip install eos-etl
```

Export blocks and transactions ([Schema](#blocksjson), [Reference](#export_blocks_and_transactions)):

```bash
> eosetl export_blocks_and_transactions --start-block 0 --end-block 500000 \
--provider-uri http://user:pass@localhost:8332 \
--blocks-output blocks.json --transactions-output transactions.json
```

Stream blockchain data continually to console:

```bash
> pip install eos-etl[streaming]
> eosetl stream -p http://user:pass@localhost:8332 --start-block 500000
```

For the latest version, check out the repo and call 
```bash
> pip install -e .[streaming] 
> python eosetl.py
```

## Table of Contents

- [Schema](#schema)
  - [blocks.json](#blocksjson)
  - [transactions.json](#transactionsjson)
  - [actions.json](#actionsjson)
- [Exporting the Blockchain](#exporting-the-blockchain)
  - [Running in Docker](#running-in-docker)
  - [Command Reference](#command-reference)
- [Public Datasets in BigQuery](#public-datasets-in-bigquery)


## Schema

### blocks.json

Field               | Type            |
--------------------|-----------------|
hash                | hex_string      | 
size                | bigint          |
stripped_size       | bigint          |
weight              | bigint          |
number              | bigint          |
version             | bigint          |
merkle_root         | hex_string      |
timestamp           | bigint          |
nonce               | hex_string      |
bits                | hex_string      |
coinbase_param      | hex_string      |
transaction_count   | bigint          |

### transactions.json

Field                   | Type                  |
------------------------|-----------------------|
hash                    | hex_string            | 
size                    | bigint                |
virtual_size            | bigint                |
version                 | bigint                |
lock_time               | bigint                |
block_number            | bigint                |
block_hash              | hex_string            |
block_timestamp         | bigint                |
is_coinbase             | boolean               |
inputs                  | []transaction_input   |
outputs                 | []transaction_output  |
input_count             | bigint                |
output_count            | bigint                |
input_value             | bigint                |
output_value            | bigint                |
fee                     | bigint                |

### actions.json

TODO


You can find column descriptions in [schemas](https://github.com/blockchain-etl/eos-etl-airflow/tree/master/dags/resources/stages/enrich/schemas)

## Exporting the Blockchain

1. Install python 3.5.3+ https://www.python.org/downloads/

1. Install EOS node or get access to EOS node maintained by someone else (because running your own node is not so easy).
Some docs:
- [https://developers.eos.io/eosio-nodeos/docs/](https://developers.eos.io/eosio-nodeos/docs/)
- [https://eosnode.tools/](https://eosnode.tools/)
- [https://github.com/CryptoLions/EOS-MainNet](https://github.com/CryptoLions/EOS-MainNet)

1. Make sure it downloaded the blocks that you need by executing in the terminal:
```bash
curl --request POST \
  --url https://localhost:8080/v1/chain/get_info \
  --header 'accept: application/json'
```
You can export blocks below `last_irreversible_block_num`, there is no need to wait until the full sync

1. Install EOS ETL:

    ```bash
    > pip install eos-etl
    ```

1. Export blocks & transactions:

    ```bash
    > eosetl export_all --start 0 --end 499999  \
    --provider-uri http://user:pass@localhost:8332
    ```
    
    In case `eosetl` command is not available in PATH, use `python -m eosetl` instead.
  
    The result will be in the `output` subdirectory, partitioned in Hive style:

    ```bash
    output/blocks/start_block=00000000/end_block=00000099/blocks_00000000_00000099.csv
    output/blocks/start_block=00000100/end_block=00000199/blocks_00000100_=00000199.csv
    ...
    output/transactions/start_block=00000000/end_block=00000099/transactions_00000000_00000099.csv
    ...
    output/actions/start_block=00000000/end_block=00000099/actions_00000000_00000099.csv
    ...
    ```
    
### Running in Docker

1. Install Docker https://docs.docker.com/install/

1. Build a docker image
    ```bash
    > docker build -t eos-etl:latest .
    > docker image ls
    ```

1. Run a container out of the image
    ```bash
    > MSYS_NO_PATHCONV=1 docker run -v $HOME/output:/eos-etl/output eos-etl:latest \
        export_blocks_and_transactions --max-workers 50 --start-block 30000000 \
        --end-block 30000100 --provider-uri http://your_eos_node:node_port \
        --blocks-output ./output/blocks.csv --transactions-output ./output/transactions.csv \
        --actions-output ./output/actions.csv
    ```
    
1. Run streaming to console or Pub/Sub
    ```bash
    > MSYS_NO_PATHCONV=1 docker build -t eos-etl:latest-streaming -f Dockerfile_with_streaming .
    > echo "Stream to console"
    > MSYS_NO_PATHCONV=1 docker run eos-etl:latest-streaming stream -p http://user:pass@localhost:8332 --start-block 500000
    > echo "Stream to Pub/Sub"
    > MSYS_NO_PATHCONV=1 docker run -v /path_to_credentials_file/:/eos-etl/ --env GOOGLE_APPLICATION_CREDENTIALS=/eos-etl/credentials_file.json eos-etl:latest-streaming stream -p http://user:pass@localhost:8332 --start-block 500000 --output projects/your-project/topics/crypto_eos
    ```

1. Refer to https://github.com/blockchain-etl/blockchain-etl-streaming for deploying the streaming app to 
Google Kubernetes Engine.

### Command Reference

- [export_blocks_and_transactions](#export_blocks_and_transactions)
- [get_block_range_for_date](#get_block_range_for_date)
- [export_all](#export_all)
- [stream](#stream)

All the commands accept `-h` parameter for help, e.g.:

```bash
> python eosetl.py export_blocks_and_transactions --help
Usage: eosetl.py export_blocks_and_transactions [OPTIONS]

  Export blocks and transactions.

Options:
  -s, --start-block INTEGER   Start block
  -e, --end-block INTEGER     End block  [required]
  -p, --provider-uri TEXT     The URI of the remote EOS node
  -w, --max-workers INTEGER   The maximum number of workers.
  --blocks-output TEXT        The output file for blocks. If not provided
                              blocks will not be exported. Use "-" for stdout
  --transactions-output TEXT  The output file for transactions. If not
                              provided transactions will not be exported. Use
                              "-" for stdout
  --actions-output TEXT       The output file for actions. If not provided
                              transactions will not be exported. Use "-"
                              for stdout
  --help                      Show this message and exit.
```

For the `--output` parameters the supported type is json. The format type is inferred from the output file name.

#### export_blocks_and_transactions

```bash
> python eosetl.py export_blocks_and_transactions --start-block 0 --end-block 500000 \
  --provider-uri http://user:pass@localhost:8332 \
  --blocks-output blocks.json --transactions-output transactions.json
```

Omit `--blocks-output` or `--transactions-output` or `--actions-output` options if you want to export only transactions/blocks/actions.

You can tune `--max-workers` for performance.

#### get_block_range_for_date

```bash
> python eosetl.py get_block_range_for_date --provider-uri http://user:pass@localhost:8332 --date=2017-03-01
```

#### export_all

```bash
> python eosetl.py export_all --provider-uri http://user:pass@localhost:8332 --start 2018-01-01 --end 2018-01-02
```

You can tune `--export-batch-size`, `--max-workers` for performance.

#### stream

```bash
> python eosetl.py stream --provider-uri http://user:pass@localhost:8332 --start-block 500000
```

- This command outputs blocks and transactions to the console by default.
- Use `--output` option to specify the Google Pub/Sub topic where to publish blockchain data, 
e.g. `projects/your-project/topics/eos_blockchain`.
- The command saves its state to `last_synced_block.txt` file where the last synced block number is saved periodically.
- Specify either `--start-block` or `--last-synced-block-file` option. `--last-synced-block-file` should point to the 
file where the block number, from which to start streaming the blockchain data, is saved.
- Use the `--lag` option to specify how many blocks to lag behind the head of the blockchain. It's the simplest way to 
handle chain reorganizations - they are less likely the further a block from the head.
- You can tune `--period-seconds`, `--batch-size`, `--max-workers` for performance.
 

### Running Tests

```bash
> pip install -e .[dev]
> echo "The below variables are optional"
> export EOSETL_PROVIDER_URI=http://api.main.alohaeos.com:80
> pytest -vv
```

### Running Tox Tests

```bash
> pip install tox
> tox
```

### Public Datasets in BigQuery

TODO: https://cloud.google.com/blog/products/data-analytics/introducing-six-new-cryptocurrencies-in-bigquery-public-datasets-and-how-to-analyze-them
