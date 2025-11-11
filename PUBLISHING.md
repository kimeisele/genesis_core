# Publishing Genesis Core to PyPI

This guide explains how to publish Genesis Core to PyPI (Python Package Index).

## Prerequisites

1. **PyPI Account**
   - Create account at https://pypi.org/account/register/
   - Verify your email

2. **API Token**
   - Go to https://pypi.org/manage/account/token/
   - Create new API token with scope "Entire account"
   - Save the token (starts with `pypi-`)

3. **GitHub Secrets**
   - Go to your GitHub repo → Settings → Secrets and variables → Actions
   - Add secret: `PYPI_TOKEN` with your PyPI API token

## Publishing Methods

### Method 1: Automatic (via GitHub Release)

This is the recommended method. It uses GitHub Actions to automatically publish when you create a release.

```bash
# 1. Update version in setup.py and pyproject.toml
# 2. Commit and push changes
git add setup.py pyproject.toml
git commit -m "Bump version to 1.0.1"
git push

# 3. Create and push a tag
git tag v1.0.1
git push origin v1.0.1

# 4. Create GitHub Release
# Go to GitHub → Releases → Create new release
# - Tag: v1.0.1
# - Title: "Genesis Core v1.0.1"
# - Description: Release notes
# - Click "Publish release"

# 5. GitHub Actions will automatically:
#    - Run tests
#    - Verify frozen core
#    - Build package
#    - Publish to PyPI
```

### Method 2: Manual (Local)

If you need to publish manually:

```bash
# 1. Install build tools
pip install build twine

# 2. Clean old builds
rm -rf dist/ build/ *.egg-info

# 3. Build package
python -m build

# Output:
# dist/
#   ├── genesis_core-1.0.0-py3-none-any.whl
#   └── genesis_core-1.0.0.tar.gz

# 4. Check package
twine check dist/*

# 5. Test upload to TestPyPI (optional)
twine upload --repository testpypi dist/*
# Username: __token__
# Password: your-testpypi-token

# Test install from TestPyPI:
pip install --index-url https://test.pypi.org/simple/ genesis-core

# 6. Upload to PyPI (production)
twine upload dist/*
# Username: __token__
# Password: your-pypi-token
```

## Version Management

### Semantic Versioning

Genesis Core follows [Semantic Versioning](https://semver.org/):

- **1.0.0** - Initial frozen release
- **1.0.1** - Patch (bug fixes in extensions/tooling only, NOT core)
- **1.1.0** - Minor (new features in extensions, core stays frozen)
- **2.0.0** - Major (breaking changes - requires unfreezing core)

### Updating Version

Update version in **3 places**:

1. `setup.py` - line 17
2. `pyproject.toml` - line 6
3. `genesis_core/__init__.py` - line 11

```python
# genesis_core/__init__.py
__version__ = "1.0.1"
__freeze_date__ = "2025-11-11"  # Keep original freeze date
```

## Pre-Release Checklist

Before publishing a new version:

- [ ] All tests pass: `pytest -v`
- [ ] Frozen core verified: `python scripts/verify_frozen.py`
- [ ] README updated (if needed)
- [ ] FROZEN_MANIFEST.md reviewed
- [ ] Version bumped in all 3 files
- [ ] CHANGELOG updated (create if needed)
- [ ] Git tag created with matching version

## Post-Release Checklist

After publishing:

- [ ] Verify package on PyPI: https://pypi.org/project/genesis-core/
- [ ] Test installation: `pip install genesis-core==X.Y.Z`
- [ ] Test imports: `python -c "from genesis_core import entity, schema"`
- [ ] Update documentation if needed
- [ ] Announce release (if major version)

## Testing Before Release

### Test on Test PyPI First

```bash
# 1. Build
python -m build

# 2. Upload to Test PyPI
twine upload --repository testpypi dist/*

# 3. Test install in fresh environment
python -m venv test_env
source test_env/bin/activate
pip install --index-url https://test.pypi.org/simple/ --no-deps genesis-core
python -c "from genesis_core import entity, schema; print('✅ Works')"
deactivate
rm -rf test_env
```

## Troubleshooting

### Issue: "File already exists"

PyPI doesn't allow re-uploading the same version. Solutions:

1. Delete `dist/` and rebuild
2. Bump version number
3. Use Test PyPI for testing

### Issue: "Invalid token"

1. Regenerate PyPI API token
2. Update GitHub secret `PYPI_TOKEN`
3. Make sure token starts with `pypi-`

### Issue: "Package name already taken"

If `genesis-core` is taken:

1. Try variations: `genesis-core-framework`, `genesis-core-system`
2. Or use private PyPI server
3. Or distribute via GitHub only

### Issue: "Build fails"

```bash
# Clean everything
rm -rf dist/ build/ *.egg-info __pycache__
find . -type d -name __pycache__ -exec rm -rf {} +

# Reinstall build tools
pip install --upgrade build twine setuptools wheel

# Try again
python -m build
```

## GitHub Actions Workflow

The `.github/workflows/publish.yml` handles automatic publishing:

```yaml
- Triggered on: GitHub Release
- Steps:
  1. Checkout code
  2. Setup Python
  3. Verify frozen core
  4. Run tests
  5. Build package
  6. Check package
  7. Upload to PyPI
```

## Security Notes

1. **Never commit tokens** to git
2. **Use GitHub Secrets** for tokens
3. **Enable 2FA** on PyPI account
4. **Use scoped tokens** (per-project if possible)
5. **Rotate tokens** regularly

## Versioning Strategy for Frozen Core

Since Genesis Core is **frozen**, version updates should be rare:

- **1.0.x** - Tooling improvements, documentation, examples
- **1.x.0** - New extension examples, improved tests
- **2.0.0** - Core unfreeze (only with team approval)

## Alternative: Private Distribution

If you don't want to publish to public PyPI:

### Option 1: GitHub as Package Source

```bash
pip install git+https://github.com/kimeisele/genesis_core.git
```

### Option 2: Private PyPI Server

Use [pypiserver](https://github.com/pypiserver/pypiserver) or similar.

### Option 3: Vendoring

Include genesis_core directly in your project (not recommended).

## Support

For issues with publishing:
- Check GitHub Actions logs
- Review PyPI upload logs
- Open issue in genesis_core repo

---

**Remember:** Genesis Core is frozen. Most version updates should only affect extensions, documentation, and tooling - NOT the core modules themselves.
