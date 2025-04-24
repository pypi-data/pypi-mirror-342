# bulkdownload

Utility script to retrieve bulk downloads

## Environment Variables

Env Var | Description | Required
-- | -- | --
NDL_APIKEY | Data Link api key.  Used for all requests to perform bulk download. | Yes
NDL_HOSTNAME | Alternative hostname to retrieve files. | No

## Install

[Create a venv](https://docs.python.org/3/library/venv.html) or pyenv if you
like and activate.

```shell
pip install ndlbulkdownload
```

## Usage

The '--param' accepts key/value pairs as you would define query parameters.
For any given product documentation, define the key as necessary.

Note, for collections, you can specify multiple of the same key. Use RFC
brackets [] for lists of a given key.  See examples below.

```shell
usage: bulkdownload [-h] --code VC/TC
                    [--param [key value [value ...]]]
                    [--output-directory /tmp/ndl]
                    [--debug]
                    [--verbose]
                    [--skip-proxy] [--skip-ssl-verify]
                    [--redirect | --no-redirect]
                    [--workers W]
                    [--host hostname]
                    [--version]

Bulk Download from Data Link.

options:
  -h, --help            show this help message and exit
  --code VC/TC          The vendor_code/table_code you are trying to download.
                        Example: FOO/BAR
  --param key value [value ...]
                        Add query param key/value pair
  -O O, --output-directory O
                        Directory to output files. Example: /tmp/ndl (default: current directory)
  --debug               Increase log level to DEBUG
  --verbose             Show logging output
  --skip-proxy          Ignore proxy environment variables
  --skip-ssl-verify     Do not verify SSL (not recommended in most situations)
  --redirect, --no-redirect
                        Request redirect to files (default: true)
  --workers W           Total parallel workers (default: min(32, os.cpu_count()))
  --host hostname       Define an alternative hostname
  --version             show program's version number and exit
```

## Examples

```shell
# download data on a particular date:
bulkdownload --code FOO/BAR --param date.eq 2024-09-01

# download multiple tickers between a given date [start, end)
bulkdownload --code FOO/BAR --param 'symbols.in[]' MSFT AAPL --param date.gte 2024-01-01 --param date.lt 2024-04-01

# download multiple tickers between a given date [start, end) and with output directory
bulkdownload --code FOO/BAR --param 'symbols.in[]' MSFT --param 'symbols.in[]' AAPL --param date.gte 2024-01-01 --param date.lt 2024-04-01 -O /tmp/ndl
```

## External Documentation

Please read more about possible arguments for a given table.  You can read
more about the [api parameter specification here](https://docs.data.nasdaq.com/docs/large-table-download).

## Development

Be sure to install optional dependencies. You can run the following to install
development related tools:

```shell
make install-devtools
```

To try your changes with a localized shim:

```shell
make install-dev
