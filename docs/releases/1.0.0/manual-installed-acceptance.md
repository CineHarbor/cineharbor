# CineHarbor 1.0.0 — manual installed-client acceptance (unsigned test builds)

This is the next **human-operated** gate after immutable Web/Core/SDK/Desktop CI and three native installation suites are green. It is NOT a public release. Signatures/notarization and signed updater remain deferred until separately approved publication. Never repackage or distribute an unsigned CI installer as the public 1.0.0 release.

## Obtain the exact candidate

1. Open the **successful** final `CineHarbor/cineharbor-desktop` main workflow on GitHub Actions: https://github.com/CineHarbor/cineharbor-desktop/actions/workflows/ci.yml . Confirm its exact main commit SHA matches the latest immutable seven-repository acceptance matrix. It must have two successful runs for that SHA, including the three `Real unsigned install and startup` jobs. If a later change exists, the old artifacts are not the final candidate.
2. In the workflow run's **Artifacts** section, download the `desktop-native-<target>-<SHA>-<run_id>` archive for your actual machine: Windows x64 `x86_64-pc-windows-msvc` (NSIS setup.exe), Intel macOS `x86_64-apple-darwin` (.dmg), or Apple Silicon macOS `aarch64-apple-darwin` (.dmg). Never download another architecture just to satisfy this checklist. Record the artifact name, commit SHA and OS/build. GitHub may require sign-in to access Actions artifacts.
3. Perform the installation **only on an isolated test computer or expendable test profile**, because these are unsigned verification packages rather than a publicly trusted release. Do not disable machine-wide security protections or replace an existing productive installation. If OS trust policy blocks the installer, record the exact error and stop instead of disabling protections.

## Interactive acceptance matrix

Mark each as PASS / FAIL / BLOCKED, attach a screenshot, timestamp and redacted application/sidecar logs for failures. Never send passwords, tokens, cookie values, or private database content.

- **Install / visible startup:** installer opens, app launches, the main UI renders without blank page or crashes; close app and relaunch; verify local-service starts and stops normally.
- **Account and state:** sign in with an expendable test account if supported; change one harmless setting, add a disposable favorite/history item, quit app fully, reopen and confirm the setting/favorite/history remain. Verify profile selection without leaking data across accounts.
- **VOD:** search a movie and a series, open details, display stream sources, play an authorized real source, seek at least once, switch episode/source, and verify recovery/error messages for an unavailable source.
- **Live:** select a live channel, play and switch channel/source; verify UI remains responsive and does not reuse a prior signed media URL. Do not deliberately make requests to untrusted/private-network media URLs.
- **Downloads:** start one small permitted download, observe progress and completion, play or open it offline if supported, restart the app and check the download metadata is retained; test cancellation/retry only on nonessential media.
- **Time/expiry and connectivity:** with a supported test source, use the app longer than one media capability renewal period; verify playback can continue after metadata refresh. Toggle offline only after content is safely saved, then restore connectivity and check recoverable errors.
- **Update/retention:** do **not** run the public updater, force a signature mismatch, or create a public release. A signed old-to-new production upgrade is deferred to publication. Optional isolated data-copy rehearsal must be recorded as unsigned/manual only.

## Evidence and decision

Record `platform`, `os_version`, `architecture`, `desktop_main_sha`, `artifact_name`, `sha256`, `date`, `installer_startup`, `sidecar_health`, `settings_persistence`, `vod_playback`, `live_playback`, `downloads`, `error_recovery`, `notes`. A missing item is **UNVERIFIED**, not passing. Report reproducible failures with source identifier and safe diagnostic excerpts. Do not mark `RELEASE_READY=true` because of this one run; dependency audit, production/architecture, license/brand, and public-stage signing remain separate.
