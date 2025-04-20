# PyCatSearch

Yet another implementation of [JPL](https://spec.jpl.nasa.gov/) and [CDMS](https://cdms.astro.uni-koeln.de/)
spectroscopy catalogs offline search.

## Installation

The package is available from the PyPI repo:

```commandline
python3 -m pip install pycatsearch
```

One may provide a Qt binding beforehand manually installing
- `PySide6-Essentials`,
- `PyQt6`,
- `PyQt5`, or
- `PySide2`.

Otherwise, one of them will be installed automatically.
Currently, it is unavoidable.
If you need the non-GUI parts only, get the files from the GitHub repo manually.

For a bit faster downloading the catalog data, install `aiohttp`.

## Usage

### `catalog`

###### Sample usage:

In a command line:

```commandline
pycatsearch-cli --min-frequency 118749 --max-frequency 118751 catalog.json.gz -n oxygen
```
or
```commandline
python3 -m pycatsearch --min-frequency 118749 --max-frequency 118751 catalog.json.gz -n oxygen
```

In a code:

```python
from pycatsearch.catalog import Catalog

c = Catalog('catalog.json.gz')
c.print(min_frequency=140141, max_frequency=140142)
```

###### Properties:

- `catalog` is a list of the catalog entries loaded by `__init__`.
- `frequency_limits` is a tuple of the minimal and the maximal frequencies of the lines
  the loaded catalogs contain.
- `is_empty` indicates whether nothing has been loaded by `__init__`.
- `entries_count` is the number of the substances loaded by `__init__`.
- `sources` contains a list of files that have been loaded successfully by `__init__`.
- `sources_info` returns a list of the files and the timestamps recorded there (if any).
- `min_frequency` and `max_frequency` are the extreme values of `frequency_limits`.

###### Functions:

- `__init__(self, *catalog_file_names: str)` accepts names of JSON or GZip/BZip2/LZMA-compressed JSON files.
  It loads them into memory joined.
- `filter(self, *,
  min_frequency: float = 0.0,
  max_frequency: float = math.inf,
  min_intensity: float = -math.inf,
  max_intensity: float = math.inf,
  temperature: float = -math.inf,
  any_name: str = '',
  any_formula: str = '',
  any_name_or_formula: str = '',
  anything: str = '',
  species_tag: int = 0,
  inchi: str = '',
  trivial_name: str = '',
  structural_formula: str = '',
  name: str = '',
  stoichiometric_formula: str = '',
  isotopolog: str = '',
  state: str = '',
  degrees_of_freedom: int | None = None) -> dict[int, dict[str, int | str | list[dict[str, float]]]]`
  returns only the catalog entries that meet the criteria specified. The arguments are the following:
    - `float min_frequency`: the lower frequency \[MHz\] to take.
    - `float max_frequency`: the upper frequency \[MHz\] to take.
    - `float min_intensity`: the minimal intensity \[log10(nm²×MHz)\] to take.
    - `float max_intensity`: the maximal intensity \[log10(nm²×MHz)\] to take, use to avoid meta-stable substances.
    - `float temperature`: the temperature to calculate the line intensity at,
      use the catalog intensity if not set.
    - `str any_name`: a string to match the “trivialname” or the “name” field.
    - `str any_formula`: a string to match the “structuralformula,” “moleculesymbol,”
      “stoichiometricformula,” or “isotopolog” field.
    - `str any_name_or_formula`: a string to match any field used by `any_name` and `any_formula`.
    - `str anything`: a string to match any field.
    - `int species_tag`: a number to match the “speciestag” field.
    - `str inchi`: a string to match the “inchikey” field.
      See https://iupac.org/who-we-are/divisions/division-details/inchi/ for more.
    - `str trivial_name`: a string to match the “trivialname” field.
    - `str structural_formula`: a string to match the “structuralformula” field.
    - `str name`: a string to match the “name” field.
    - `str stoichiometric_formula`: a string to match the “stoichiometricformula” field.
    - `str isotopolog`: a string to match the “isotopolog” field.
    - `str state`: a string to match the “state” or the “state_html” field.
    - `int degrees_of_freedom`: 0 for atoms, 2 for linear molecules, and 3 for nonlinear molecules.
- `filter_by_species_tags(self, *,
  species_tags: Iterable[int] | None = None,
  min_frequency: float = 0.0,
  max_frequency: float = math.inf,
  min_intensity: float = -math.inf,
  max_intensity: float = math.inf,
  temperature: float = -math.inf,
  ) -> dict[int, dict[str, int | str | list[dict[str, float]]]]`
  returns only the catalog entries that meet the criteria specified.
  It is a faster version of the `filter` function, for it makes fewer comparisons.
  The arguments are the following:
    - `Iterable[int] | None species_tags`: numbers to match the “speciestag” field,
      use all items listed in the catalog if not set or set to `None`.
    - `float min_frequency`: the lower frequency \[MHz\] to take.
    - `float max_frequency`: the upper frequency \[MHz\] to take.
    - `float min_intensity`: the minimal intensity \[log10(nm²×MHz)\] to take.
    - `float max_intensity`: the maximal intensity \[log10(nm²×MHz)\] to take, use to avoid meta-stable substances.
    - `float temperature`: the temperature to calculate the line intensity at,
      use the catalog intensity if not set.
- `print(**kwargs)` prints a table of the filtered catalog entries.
  It accepts all the arguments valid for the `filter` function.

### `downloader`

###### Sample usage:

In a command line:

```commandline
pycatsearch-downloader --min-frequency 115000 --max-frequency 178000 catalog.json.gz
```

In a code:

```python
from pycatsearch import downloader

downloader.save_catalog('catalog.json.gz', (115000, 178000))
```

###### Functions:

- `get_catalog(frequency_limits: tuple[float, float] = (0.0, math.inf)) ->
  dict[int, dict[str, int | str | list[dict[str, float]]]]` downloads the spectral lines catalog data.
  It returns a list of the spectral lines catalog entries.
  The parameter `frequency_limits` is the frequency range of the catalog entries to keep.
  By default, there are no limits.
- `save_catalog(filename: str, frequency_limits: tuple[float, float] = (0.0, math.inf)) -> bool`
  downloads and saves the spectral lines catalog data.
  Inside, `get_catalog` function is called.
  The function returns `True` if something got downloaded, `False` otherwise.
  The function fails with an error if `get_catalog` raises an error,
  or if the result cannot be stored in the specified file.
  The parameters of `save_catalog` are the following:
    - `str filename`: the name of the file to save the downloaded catalog to.
      If it ends with an unknown suffix, `'.json.gz'` is appended to it.
    - `tuple frequency_limits`: the tuple of the maximal and the minimal frequencies of the lines being stored.
      All the lines outside the specified frequency range are omitted. By default, there are no limits.

### `async_downloader`

This is like `downloader`, but much, much faster.
The download speed is limited by the remote servers.
Most of the time, it takes no more than 90 seconds to load all the data.

Requires `aiohttp`.

###### Sample usage:

In a command line:

```commandline
pycatsearch-async-downloader --min-frequency 115000 --max-frequency 178000 catalog.json.gz
```

In a code:

```python
from pycatsearch import async_downloader

async_downloader.save_catalog('catalog.json.gz', (115000, 178000))
```

###### Functions:

- `get_catalog(frequency_limits: tuple[float, float] = (0.0, math.inf)) ->
  dict[int, dict[str, int | str | list[dict[str, float]]]]`
- `save_catalog(filename: str, frequency_limits: tuple[float, float] = (0.0, math.inf)) -> bool`

The functions behave _almost_ exactly like their namesakes from `downloader`.
`get_catalog` prints out the progress described in two numbers:

- the number of species, for which the data has already been downloaded
  and contains spectral lines within the specified frequency range, and
- the number of species yet to be downloaded and processed.

###### `Downloader` class

An instance of `Downloader` class is created in `get_catalog` function.
Then, a separate thread takes care of the downloading.
If the thread fails, `get_catalog` returns an empty list, almost never raising an exception.

The class constructor accepts the frequency limits, like `get_catalog` function.

One also may provide the constructor with a `multiprocessing.Queue[tuple[int, int]]`
to see the downloading progress.
The first number of the tuple is the number of the species,
for which the data has already been downloaded
and contains spectral lines within the specified frequency range.
The second one is the number of species yet to be downloaded and processed.
The numbers are the same as what `get_catalog` function types.

### `gui`

This is the graphical interface built with Python bindings for Qt (`PyQt5`, `PySide6`, `PyQt6`, or `PySide2`).
Run `pycatsearch` and see for yourself.

### Requirements

The code is developed under `python 3.11`. It should work under `python 3.8` but merely tested.

The non-GUI parts require an absolute minimum of non-standard modules.
If you want to download the catalog data faster, consider `async_downloader` module;
it requires `aiohttp`.
Otherwise, only the built-ins are used.

The GUI requires Python bindings for Qt (`PyQt5`, `PySide6`, `PyQt6`, or `PySide2`), picked by `QtPy`.

## File Format

The JSON file contains a dictionary of substances called `catalog`.
The keys of the dictionary are the species tags.
Each substance is described like the following:

```json
{
  "id": 4,
  "molecule": 3,
  "structuralformula": "H2",
  "stoichiometricformula": "H2",
  "moleculesymbol": "H<sub>2</sub>",
  "speciestag": 3501,
  "name": "HD,v=0,1",
  "trivialname": "Hydrogen molecule",
  "isotopolog": "HD",
  "state": "$v=0,1$",
  "state_html": "v=0,1",
  "inchikey": "UFHFLCQGNIYNRP-OUBTZVSYSA-N",
  "contributor": "H. S. P. M\u00fcller",
  "version": "2*",
  "dateofentry": "2011-12-01",
  "degreesoffreedom": 2,
  "lines": []
}
```

`lines` is an array of the substance absorption lines records.
For now, it includes only the _frequency_ \[MHz\], the _intensity_ \[log10(nm²×MHz)\],
and the _lower state energy_ relative to the ground state \[1/cm\] of a line:

```json
{
  "frequency": 143285.9808,
  "intensity": -6.4978,
  "lowerstateenergy": 581.4862
}
```

Besides `catalog`, the JSON file contains `frequency` array that holds the frequency limits of the catalog
and the catalog build time in ISO format.
Just in case.

For physical meaning of the values, check out [catdoc.pdf](https://spec.jpl.nasa.gov//ftp//pub/catalog/doc/catdoc.pdf).
