# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.7] - YYYY-MM-DD
### Added
- Windows + WSL & VS Code-Remote path support: Jinni now auto-converts WSL paths (`/home/user/project`) and `vscode-remote://wsl+Distro/...` URIs to the correct `\\wsl$\Distro\...` UNC form when running on Windows. This applies to paths provided via CLI arguments (`paths`, `--root`, `--overrides`) and the MCP `read_context` tool arguments (`project_root`, `targets`).

[Unreleased]: https://github.com/smat-dev/jinni/compare/v0.1.7...HEAD
[0.1.7]: https://github.com/smat-dev/jinni/releases/tag/v0.1.7 