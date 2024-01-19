---
sidebar_position: 2
---

# Installing dōteki

If you are using the [GitHub Action](https://github.com/welpo/doteki-action), you don't need to install anything. The action will take care of everything.

Keep reading if you want to run **dōteki** locally.

## From PyPI

To get the latest stable release with only the core dependencies, run:

```bash
pip install doteki
```

If you want all plugin dependencies, run this instead:

```bash
pip install doteki[all]
```

You can select specific plugins to install by replacing `all` with a space-separated list of plugin names. For example, to install the dependencies for the `lastfm` and `feed` plugins, run:

```bash
pip install doteki[lastfm,feed]
```

## From Source

You can use `pip` to install the development version from GitHub:

```bash
pip install git+https://github.com/welpo/doteki.git
```

You can also install a specific version by appending `@<version>` to the URL. For example, to install version `0.0.1`, run:

```bash
pip install git+https://github.com/welpo/doteki.git@v0.1.0
```
