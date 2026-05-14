# drugscreenpy

[![Tests][badge-tests]][tests]
[![Documentation][badge-docs]][documentation]

[badge-tests]: https://img.shields.io/github/actions/workflow/status/xushenbo/drugscreenpy/test.yaml?branch=main
[badge-docs]: https://img.shields.io/readthedocs/drugscreenpy

Self-controlled cohort drug-screening workflows for electronic health record data.

## Getting started

Please refer to the [documentation][],
in particular, the [drug-screening tutorial][] and the [API documentation][].

## Installation

You need to have Python 3.11 or newer installed on your system.
If you don't have Python installed, we recommend installing [uv][].

There are several alternative options to install drugscreenpy:

<!--
1) Install the latest release of `drugscreenpy` from [PyPI][]:

```bash
pip install drugscreenpy
```
-->

1. Install the latest development version:

```bash
pip install git+https://github.com/xushenbo/drugscreenpy.git@main
```

## Release notes

See the [changelog][].

## Contact

For questions and help requests, you can reach out in the [scverse discourse][].
If you found a bug, please use the [issue tracker][].

## Citation

If you use `drugscreenpy`, please cite the drug-screening workflow:

```bibtex
@inproceedings{xu2024foundational,
  title={Foundational Model-aided Automatic High-throughput Drug Screening Using Self-controlled Cohort Study},
  author={Shenbo Xu and Raluca Cobzaru and Stan Finkelstein and Roy Welsch and Kenney Ng},
  booktitle={NeurIPS 2024 Workshop on AI for New Drug Modalities},
  year={2024},
  url={https://openreview.net/forum?id=30EakJqzF0}
}
```

[uv]: https://github.com/astral-sh/uv
[scverse discourse]: https://discourse.scverse.org/
[issue tracker]: https://github.com/xushenbo/drugscreenpy/issues
[tests]: https://github.com/xushenbo/drugscreenpy/actions/workflows/test.yaml
[documentation]: https://drugscreenpy.readthedocs.io
[drug-screening tutorial]: https://drugscreenpy.readthedocs.io/en/latest/drug_screening.html
[changelog]: https://drugscreenpy.readthedocs.io/en/latest/changelog.html
[api documentation]: https://drugscreenpy.readthedocs.io/en/latest/api.html
[pypi]: https://pypi.org/project/drugscreenpy
