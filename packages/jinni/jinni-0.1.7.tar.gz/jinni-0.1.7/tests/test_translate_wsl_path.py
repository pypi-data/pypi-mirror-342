import pytest
import platform
import subprocess
import shutil
from urllib.parse import urlparse, ParseResult
from jinni.utils import _translate_wsl_path, _WSLPATH_PATH

# --- Test Cases for _translate_wsl_path ---

# Helper to mock platform.system
def mock_platform_system(system_name="Windows"):
    def func():
        return system_name
    return func

# Helper to mock shutil.which
def mock_shutil_which(wslpath_exists=True):
    def func(cmd):
        if cmd == "wslpath" and wslpath_exists:
            return "/path/to/wslpath" # Return a dummy path
        return None
    return func

# Helper to mock subprocess.check_output for wslpath
def mock_subprocess_check_output(win_path="\\\\wsl$\\Ubuntu\\home\\user\\project", fail=False, fail_msg="Error", raise_other_exception=False):
    def func(cmd_args, text=True, stderr=None):
        if raise_other_exception:
             raise Exception("Some other error")
        if cmd_args == ["wslpath", "-w", "/home/user/project"]:
            if fail:
                raise subprocess.CalledProcessError(1, cmd_args, stderr=fail_msg)
            return win_path + "\n" # wslpath adds newline
        raise ValueError(f"Unexpected command for mock_subprocess_check_output: {cmd_args}")
    return func

# Helper to mock urlparse
def mock_urlparse(scheme="vscode-remote", netloc="wsl+Ubuntu", path="/home/user/project"):
    # Return a simple object that mimics ParseResult enough for the function
    class MockParseResult:
        def __init__(self, scheme, netloc, path):
            self.scheme = scheme
            self.netloc = netloc
            self.path = path
    return lambda url_str: MockParseResult(scheme, netloc, path)

# --- Tests ---

def test_translate_windows_path_no_change(monkeypatch):
    """Test a Windows path is not translated on Windows."""
    monkeypatch.setattr(platform, "system", mock_platform_system("Windows"))
    win_path = "C:\\Users\\User\\Project"
    assert _translate_wsl_path(win_path) == win_path

def test_translate_non_wsl_posix_path_no_change(monkeypatch):
    """Test a path that looks POSIX but isn't WSL (e.g., macOS path on Windows) is not translated."""
    monkeypatch.setattr(platform, "system", mock_platform_system("Windows"))
    # Mock wslpath failing because the path isn't inside WSL
    monkeypatch.setattr(shutil, "which", mock_shutil_which(True))
    monkeypatch.setattr(subprocess, "check_output", mock_subprocess_check_output(fail=True, fail_msg="Path does not exist"))
    assert _translate_wsl_path("/Users/me/project") == "/Users/me/project"

def test_translate_posix_path_wslpath_not_found(monkeypatch):
    """Test POSIX path translation when wslpath is not installed/found."""
    monkeypatch.setattr(platform, "system", mock_platform_system("Windows"))
    monkeypatch.setattr(shutil, "which", mock_shutil_which(False)) # wslpath not found
    assert _translate_wsl_path("/home/user/project") == "/home/user/project"

def test_translate_posix_path_wslpath_error(monkeypatch):
    """Test POSIX path translation when wslpath command fails unexpectedly."""
    monkeypatch.setattr(platform, "system", mock_platform_system("Windows"))
    monkeypatch.setattr(shutil, "which", mock_shutil_which(True))
    monkeypatch.setattr(subprocess, "check_output", mock_subprocess_check_output(raise_other_exception=True))
    assert _translate_wsl_path("/home/user/project") == "/home/user/project"

def test_translate_vscode_non_wsl_uri_no_change(monkeypatch):
    """Test a non-WSL vscode-remote URI is not translated."""
    monkeypatch.setattr(platform, "system", mock_platform_system("Windows"))
    monkeypatch.setattr("urllib.parse.urlparse", mock_urlparse(scheme="vscode-remote", netloc="ssh+server", path="/path/on/remote"))
    uri = "vscode-remote://ssh+server/path/on/remote"
    assert _translate_wsl_path(uri) == uri

def test_translate_posix_path_on_linux_no_change(monkeypatch):
    """Test POSIX path is not translated when running on Linux."""
    monkeypatch.setattr(platform, "system", mock_platform_system("Linux"))
    path = "/home/user/project"
    assert _translate_wsl_path(path) == path

def test_translate_vscode_wsl_uri_on_linux_no_change(monkeypatch):
    """Test vscode-remote WSL URI is not translated when running on Linux."""
    monkeypatch.setattr(platform, "system", mock_platform_system("Linux"))
    uri = "vscode-remote://wsl+Ubuntu/home/user/project"
    assert _translate_wsl_path(uri) == uri

def test_translate_unc_path_no_change(monkeypatch):
    """Test a UNC path (potentially already translated) is not re-translated."""
    monkeypatch.setattr(platform, "system", mock_platform_system("Windows"))
    unc_path = "\\\\server\\share\\path"
    assert _translate_wsl_path(unc_path) == unc_path

def test_translate_empty_string_no_change(monkeypatch):
    """Test an empty string is handled gracefully."""
    monkeypatch.setattr(platform, "system", mock_platform_system("Windows"))
    assert _translate_wsl_path("") == ""


# --- Parametrized Tests ---

@pytest.mark.parametrize(
    ("input_path", "mock_system", "wslpath_exists", "wslpath_output", "urlparse_mock_config", "expected_output"),
    [
        # --- Standard WSL Translations ---
        # POSIX Path
        ("/home/alice/app", "Windows", True, r"\\wsl$\Ubuntu\home\alice\app", None, r"\\wsl$\Ubuntu\home\alice\app"),
        # VSCode Remote URI
        ("vscode-remote://wsl+Ubuntu/home/alice/app", "Windows", True, None, {"scheme": "vscode-remote", "netloc": "wsl+Ubuntu", "path": "/home/alice/app"}, r"\\wsl$\Ubuntu\home\alice\app"),
        # Alternate VSCode URI
        ("vscode://vscode-remote/wsl+Ubuntu/home/alice/app", "Windows", True, None, {"scheme": "vscode", "netloc": "vscode-remote", "path": "/wsl+Ubuntu/home/alice/app"}, r"\\wsl$\Ubuntu\home\alice\app"),

        # --- Edge Cases ---
        # Alternate VSCode URI - No Path
        ("vscode://vscode-remote/wsl+Ubuntu", "Windows", True, None, {"scheme": "vscode", "netloc": "vscode-remote", "path": "/wsl+Ubuntu"}, "\\\\wsl$\\Ubuntu\\"),
        # Malformed URI (empty distro)
        ("vscode-remote://wsl+/home/user/project", "Windows", True, None, {"scheme": "vscode-remote", "netloc": "wsl+", "path": "/home/user/project"}, "vscode-remote://wsl+/home/user/project"),
        # SSH Remote URI (Should Not Translate)
        ("vscode-remote://ssh-remote+myhost/path/to/proj", "Windows", True, None, {"scheme": "vscode-remote", "netloc": "ssh-remote+myhost", "path": "/path/to/proj"}, "vscode-remote://ssh-remote+myhost/path/to/proj"),
        # UNC Path with Spaces (Should Not Translate)
        (r"\\wsl$\Ubuntu\home\My Project\file.txt", "Windows", True, None, None, r"\\wsl$\Ubuntu\home\My Project\file.txt"),
        # Regular Windows Path (Should Not Translate)
        (r"C:\Users\Test\Project", "Windows", True, None, None, r"C:\Users\Test\Project"),

        # --- Non-Windows Platform (Should Not Translate) ---
        ("/home/alice/app", "Linux", True, None, None, "/home/alice/app"),
        ("vscode-remote://wsl+Ubuntu/home/alice/app", "Linux", True, None, {"scheme": "vscode-remote", "netloc": "wsl+Ubuntu", "path": "/home/alice/app"}, "vscode-remote://wsl+Ubuntu/home/alice/app"),

        # --- wslpath unavailable/error (Should Not Translate POSIX) ---
        ("/home/alice/app", "Windows", False, None, None, "/home/alice/app"), # wslpath not found
        ("/home/alice/app", "Windows", True, None, None, "/home/alice/app"), # wslpath call fails
        # Malformed URI (empty distro) - Added Test Case
        ("vscode-remote://wsl+/home/user/project", "Windows", True, None, {"scheme": "vscode-remote", "netloc": "wsl+", "path": "/home/user/project"}, "vscode-remote://wsl+/home/user/project"),
    ],
    ids=[
        "posix_to_unc",
        "vscode_remote_uri_to_unc",
        "vscode_alt_uri_to_unc",
        "vscode_alt_uri_no_path_to_unc_root",
        "malformed_uri_empty_distro_no_change",
        "ssh_remote_uri_no_change",
        "unc_with_spaces_no_change",
        "windows_path_no_change",
        "posix_on_linux_no_change",
        "vscode_remote_uri_on_linux_no_change",
        "posix_wslpath_not_found_no_change",
        "posix_wslpath_fails_no_change",
        "malformed_uri_empty_distro_duplicate_no_change",
    ]
)
def test_translate_wsl_path_parametrized(monkeypatch, input_path, mock_system, wslpath_exists, wslpath_output, urlparse_mock_config, expected_output):
    monkeypatch.setattr(platform, "system", mock_platform_system(mock_system))
    # Ensure _WSLPATH_PATH is mocked based on wslpath_exists for this test run
    monkeypatch.setattr("jinni.utils._WSLPATH_PATH", "/fake/wslpath" if wslpath_exists else None)
    monkeypatch.setattr(shutil, "which", mock_shutil_which(wslpath_exists))

    # Mock subprocess.check_output if wslpath is expected to be called and exist
    if input_path.startswith("/") and not urlparse(input_path).scheme and wslpath_exists:
        def mock_subprocess_check_output_param(cmd_args, text=True, stderr=None):
            expected_cmd_base = ["/fake/wslpath", "-w"]
            expected_cmd = expected_cmd_base + [input_path]

            if cmd_args == expected_cmd:
                if wslpath_output is not None:
                    return wslpath_output + "\n"
                else:
                    raise subprocess.CalledProcessError(1, cmd_args, stderr="Mock wslpath failure for parametrized test")
            raise ValueError(f"Unexpected command for mock_subprocess_check_output_param: {cmd_args} (expected {expected_cmd}) for input {input_path}")
        monkeypatch.setattr(subprocess, "check_output", mock_subprocess_check_output_param)

    if urlparse_mock_config:
        monkeypatch.setattr("urllib.parse.urlparse", mock_urlparse(**urlparse_mock_config))

    assert _translate_wsl_path(input_path) == expected_output 