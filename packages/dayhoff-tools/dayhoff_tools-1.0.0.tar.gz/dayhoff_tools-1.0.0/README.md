# dayhoff-tools

A set of small, sharp tools for everyone at Dayhoff.

## Hosting and Auth

This repo uses Poetry to build and publish a package to GCP Artifact Registry, at `https://us-central1-python.pkg.dev/enzyme-discovery/pypirate/`.  This depends on a Poetry plugin that's now in the standard chassis setup (`keyrings.google-artifactregistry-auth`), and also on the active service account having read access to Artifact Registry. That much is set up for the standard dev container service account, but may not be available to other intended users.

## CLI commands

Unlike all the repos that use dayhoff-tools, here you have to install the package explicitly before using the CLI:

```sh
poetry install
```

## Publish a new version

1. Update version number in `pyproject.toml`
2. Run `dh wheel`
3. In other repos, run `poetry update dayhoff-tools`

If you want to overwrite an existing wheel, you'll have to manually delete it from the `dist` folder and also the [Artifact Registry repo](https://console.cloud.google.com/artifacts/python/enzyme-discovery/us-central1/pypirate/dayhoff-tools).

## Install in other repos

Installing this library is tricky because we need GCS authentication and also a couple of plugins to install this with either Pip or Poetry.  These have been incorporated into `chassis`, but it's worth noting here what the various parts are.  All this info came from this [Medium post](https://medium.com/google-cloud/python-packages-via-gcps-artifact-registry-ce1714f8e7c1).

1. Get a Service Account with read access to Artifact Registry (such as `github-actions`, which I made for this purpose).
2. Export the SA key file, copy it to your repo, and make it available through this envvar: `export GOOGLE_APPLICATION_CREDENTIALS=github_actions_key.json`

### ... with Pip

1. `pip install keyring`
2. `pip install keyrings.google-artifactregistry-auth`
3. `pip install --upgrade dayhoff-tools --index-url https://us-central1-python.pkg.dev/enzyme-discovery/pypirate/simple/`

### ... with Poetry

1. Add this plugin: `poetry self add keyrings.google-artifactregistry-auth`
2. Add these sections to `pyproject.toml`.  Note that dayhoff-tools is in a separate group `pypirate` that installs separately from the others.

   ```toml
   [tool.poetry.group.pypirate.dependencies]
   dayhoff-tools = {version = "*", source = "pypirate"}

   [[tool.poetry.source]]
    name = "pypirate"
    url = "https://us-central1-python.pkg.dev/enzyme-discovery/pypirate/simple/"
    priority = "supplemental"
   ```

3. When building a dev container, or in other circumstances when you can't easily authenticate as above, run `poetry install --without pypirate`.  
4. Otherwise, just `poetry install`.
5. To ensure you have the latest version, run `poetry update dayhoff-tools`.
