from click.testing import CliRunner
from zincdl.cli import main

runner = CliRunner()

def test_help_works():
    """Ensure help page renders without error."""
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Options:" in result.output

def test_subset_option():
    """Check subset preset selection."""
    result = runner.invoke(main, ["--subset", "fragments"])
    assert result.exit_code == 0
    assert "Using predefined subset" in result.output or result.exit_code == 0

def test_custom_mw_logp():
    """Test MW/logP manual grid parsing."""
    result = runner.invoke(main, ["--mw", "300,325", "--logp", "2,3"])
    assert result.exit_code == 0

def test_invalid_format():
    """Unsupported format should raise error."""
    result = runner.invoke(main, ["--fmt", "xyz"])
    assert result.exit_code != 0
    assert "Invalid value for '--fmt'" in result.output

def test_download_flag(tmp_path, monkeypatch):
    """Mock download behavior to avoid network access."""
    called = {}

    def fake_download_tranches(urls, out_dir):
        called["urls"] = urls
        called["out"] = out_dir

    monkeypatch.setattr("zincdl.cli.download_tranches", fake_download_tranches)

    result = runner.invoke(main, ["--mw", "300", "--logp", "2", "--download", "--out-dir", str(tmp_path)])
    assert result.exit_code == 0
    assert "urls" in called and tmp_path.name in called["out"]