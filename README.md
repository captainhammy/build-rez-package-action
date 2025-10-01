[![Tests](https://github.com/captainhammy/build-rez-package-action/actions/workflows/tests.yml/badge.svg)](https://github.com/captainhammy/build-rez-package-action/actions/workflows/tests.yml)

# Build Rez Package

This GitHub Action will build and install a [rez](https://github.com/AcademySoftwareFoundation/rez) package via the `rez build` command.

The package source can exist locally, or be pulled from a git repository.

# Usage

```yaml
  - name: Build Package
    uses: captainhammy/build-rez-package-action@v1
```
The above would execute the following command when running:
```
rez build --install
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
```
The above would execute the following command:
```
rez build --install --variant 1
```

### variant_from_request

The `variant_from_request` input can be used to have the action determine which variant to build based on a package request.

```yaml
  - name: Build Package
    uses: captainhammy/build-rez-package-action@v1
    with:
      variant_from_request: houdini-20.5
```

In this example we will say a package has the following variants: `["houdini-19.5"], ["houdini-20.0"], ["houdini-20.5"]`.
The above would find index '2' and execute the following command:
```
rez build --install --variant 2
```
If no matching variant is found, or too many variants match the requests, the workflow action will fail.

### extra

The `extra` input value will be appended to the end of the [build command](https://rez.readthedocs.io/en/stable/commands/rez-build.html)

For example, to enable debug output on the underlying cmake call you could do the following:

```yaml
  - name: Build Package
    uses: captainhammy/build-rez-package-action@v1
    with:
      extra: -- --debug-output
```
The above would execute the following command:
```
  rez build --install -- --debug-output
```

### package_root

The `package_root` input is used to define where to build from. By default, this is the current directory (.).

This input is a hack around the fact you **cannot** specify a `working-directory` on **uses** steps in GitHub Actions. 

```yaml
  - name: Build Package
    uses: captainhammy/build-rez-package-action@v1
    with:
      package_root: ./tests/test_package
```
The above would execute the following command:
```
cd ./tests/test_package
rez build --install
```

### from_git / git_tag

The `from_git` input will build the package from a git repository rather than the package root.

```yaml
  - name: Build Package
    uses: captainhammy/build-rez-package-action@v1
    with:
      from_git: https://github.com/captainhammy/dummy-rez-package.git
```

The `git_tag` input can be used to build a specific tag from that repo.
```yaml
  - name: Build Package
    uses: captainhammy/build-rez-package-action@v1
    with:
      from_git: https://github.com/captainhammy/dummy-rez-package.git
      git_tag: 0.0.2
```


# Dependencies

Dependencies are listed in `requirements.txt`, and the action must be run in an environment where the `rez` command is
available. 
