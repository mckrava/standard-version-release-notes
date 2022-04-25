# standard-version-release-notes

Read changelog entries for a specific version in changelog files created
by [standard-version](https://github.com/conventional-changelog/standard-version).

## Description

An indicative changelog created by the action is the following:

```txt
## [0.2.0] (2021-12-12)

### 0.1.8 (2021-12-12)

### Feat

- **users**: support deletion of users using the DELETE api/users endpoint

### Fix

- **users**: fix nickname field in GET api/users endpoint returning the nickname without an empty character.

## 0.1.7 (2021-11-05)


### Fix

- **about**: fix error message not properly showing up its minor component.

## 0.1.6 (2021-08-12)

### Feat

- **about**: add about endpoint with proper version

### Fix

- **messages**: fix error messages in GET api/users/endpoint 
```

## Usage

An example usage of the action is the following:

## Sample Workflow

```yaml
name: Bump version

on:
  push:
    branches:
      - master

jobs:
  release:
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@main
        with:
          token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
          fetch-depth: 0
      - name: Setup Python
        uses: actions/setup-python@v2.1.4
        with:
          python-version: 3.8.6
          architecture: x64
      - name: Get version from tag
        id: tag_name
        run: |
          echo ::set-output name=current_version::${GITHUB_REF#refs/tags/v}
        shell: bash
      - name: Get notes
        id: generate_notes
        uses: mckrava/standard-version-release-notes@v1.1.0
        with:
          tag_name: ${{ github.ref }}
          tag_name_ref_view: true
          changelog: CHANGELOG.md
      - name: Create Release
        id: create_release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          prerelease: false
          draft: false
          body: ${{join(fromJson(steps.generate_notes.outputs.notes).notes, '')}}
```

## Input Variables

| Name                | Description                                            | Default |
| ------------------- | ------------------------------------------------------ | ------- |
| `tag_name`          | Name of the tag whose release notes we are looking for | -       |
| `changelog`         | Path to changelog file                                 | -       |
| `tag_name_prefix`   | Tag name prefix                                        | "v"     |
| `tag_name_ref_view` | Does tag name have such view as `refs/tags/{tag_name}` | false   |

## Output Variables

| Name    | Description                                                                                                                        | Default |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------- | ------- |
| `notes` | Serialized dictionary as string containing the `notes` key which hosts the list of lines that hold data for the aforementioned tag | -       |
