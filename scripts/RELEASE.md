# Release Checklist

Use this guide for an OCELOT release.

## 1. Decide the version

OCELOT uses versions based on the release year and month like `26.06.0`. The last digit is incremented in case of bugfix releases, e.g. `26.06.0` --> `26.06.1`.

## 2. Update the changelog

Update `CHANGELOG.md` before running the release scripts. The scripts update version metadata, but they do not write release notes.

## 3. Prepare from a clean `dev` branch

```bash
git checkout dev
git pull
git status
python scripts/prepare_release.py <version> --full --dry-run
python scripts/prepare_release.py <version> --full
```

`prepare_release.py` updates version metadata, runs tests and demos,
builds package artifacts, commits the release metadata, merges `dev` into `master`, and creates a new version tag. It does not push or publish unless explicit flags are passed.

After checking the result:

```bash
git push origin dev master --tags
```

## 4. Publish artifacts explicitly

Run this first to rebuild and check artifacts without uploading:

```bash
python scripts/publish_release.py <version>
```

After credentials are configured and the artifacts look correct:

```bash
python scripts/publish_release.py <version> --upload-pypi --upload-conda
```

PyPI upload uses Twine credentials. Anaconda upload uses `anaconda-client`. Run `anaconda login` first if needed.

## 5. Optional GitHub release

If a GitHub release is needed, either create it manually from tag `v<version>` or run `prepare_release.py` with `--github-release` during the preparation step.

## Notes

- Start from a clean worktree. Avoid `--allow-dirty` for normal releases.
- Use `--skip-tests`, `--skip-demos`, or `--skip-build` only for an intentional emergency workflow.
- Use `--critical-demos-only` if needed to skip non-critical demos. This speeds up the release process but can lower the quality of the release.
- `publish_release.py` expects `HEAD` to be tagged as `v<version>` unless `--allow-tag-mismatch` is passed.
