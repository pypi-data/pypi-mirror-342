# dataflows-elasticsearch

[![Travis](https://travis-ci.org/dataspot/dataflows-elasticsearch.svg?branch=master)](https://travis-ci.org/dataspot/dataflows-elasticsearch)
[![Coveralls](http://img.shields.io/coveralls/dataspot/dataflows-elasticsearch.svg?branch=master)](https://coveralls.io/r/dataspot/dataflows-elasticsearch?branch=master)

Dataflows's processors to work with ElasticSearch

## Features

- `dump_to_elasticsearch` processor

## Contents

<!--TOC-->

  - [Getting Started](#getting-started)
    - [Installation](#installation)
    - [Examples](#examples)
  - [Documentation](#documentation)
    - [dump_to_es](#dump_to_es)
  - [Contributing](#contributing)
  - [Changelog](#changelog)

<!--TOC-->

## Getting Started

### Installation

The package use semantic versioning. It means that major versions  could include breaking changes. It's recommended to specify `package` version range in your `setup/requirements` file e.g. `package>=1.0,<2.0`.

```bash
$ pip install dataflows-elasticsearch
```

### Examples

These processors have to be used as a part of a dataflows `Flow`. For example:

```python
flow = Flow(
    load('data/data.csv'),
    dump_to_es(
        engine='localhost:9200',
    ),
)
flow.process()
```

## Documentation

### dump_to_es

Saves the Flow to an ElasticSearch Index.

#### Parameters
- `indexes` - Mapping of indexe names to resource names, e.g.
```
{
  'index-name-1': {
    'resource-name': 'resource-name-1',
  },
  'index-name-2': {
    'resource-name': 'resource-name-2',
  },
  # ...
}
```
- `mapper_cls` - Class to be used to map json table schema types into ElasticSearch types
- `index_settings` - Options to be used when creating the ElasticSearch index
- `engine` - Connection string for connecting the ElasticSearch instance, or an `Elasticsearch` object.
             Can also be of the form `env://ENV_VAR`, in which case the connection string will be fetched from the environment variable `ENV_VAR`.
- `elasticsearch_options` - Options to be used when creating the `Elasticsearch` object (in case it wasn't provided)

## Contributing

The project follows the [Open Knowledge International coding standards](https://github.com/okfn/coding-standards).

The recommended way to get started is to create and activate a project virtual environment.
To install package and development dependencies into your active environment:

```
$ make install
```

To run tests with linting and coverage:

```bash
$ make test
```

For linting, `pylama` (configured in `pylama.ini`) is used. At this stage it's already
installed into your environment and could be used separately with more fine-grained control
as described in documentation - https://pylama.readthedocs.io/en/latest/.

For example to sort results by error type:

```bash
$ pylama --sort <path>
```

For testing, `tox` (configured in `tox.ini`) is used.
It's already installed into your environment and could be used separately with more fine-grained control as described in documentation - https://testrun.org/tox/latest/.

For example to check subset of tests against Python 2 environment with increased verbosity.
All positional arguments and options after `--` will be passed to `py.test`:

```bash
tox -e py37 -- -v tests/<path>
```

Under the hood `tox` uses `pytest` (configured in `pytest.ini`), `coverage`
and `mock` packages. These packages are available only in tox envionments.

## Changelog

The full changelog and documentation for all released versions can be found in the nicely formatted [commit history](https://github.com/dataspot/dataflows-elasticsearch/commits/master).
