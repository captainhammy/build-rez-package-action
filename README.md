[![Tests](https://github.com/captainhammy/build-rez-package-action/actions/workflows/tests.yml/badge.svg)](https://github.com/captainhammy/build-rez-package-action/actions/workflows/tests.yml)

# Build Rez Packages

This GitHub Action will build and install a [rez](https://github.com/AcademySoftwareFoundation/rez) package via the `rez build` command.

# Usage

```yaml
  - name: Build Package
    uses: captainhammy/build-rez-package-action@v1
```

## Inputs

The following optional input values can be used:

### variant

The `variant` input can be used to build a specific variant, otherwise all will be built.

```yaml
  - name: Build Package
    uses: captainhammy/build-rez-package-action@v1
    with:
      variant: 1

  # Would execute the following command
  # rez build --install --variant 1
```

### extra

The `extra` input value will be appended to the end of the [build command](https://rez.readthedocs.io/en/stable/commands/rez-build.html)

For example, to enable debug output on the underlying cmake call you could do the following:

```yaml
  - name: Build Package
    uses: captainhammy/build-rez-package-action@v1
    with:
      extra: -- --debug-output

  # Would execute the following command
  # rez build --install -- --debug-output
```

### package_root

The `package_root` input is used to define where to build from. By default, this is the current directory (.).

This input is a hack around the fact you **cannot** specify a `working-directory` on **uses** steps in GitHub Actions. 

```yaml
  - name: Build Package
    uses: captainhammy/build-rez-package-action@v1
    with:
      package_root: ./tests/test_package

  # Would execute the following command
  # cd ./tests/test_package
  # rez build --install
```

# Dependencies

While this package has no direct dependencies, it must be run in an environment where the `rez` command is available. 
