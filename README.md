# IHS Practice Files

https://in-housesystems.com/practice-files/

IHS Practice Files is a static folder tool that organizes selected files beneath a practice-owned folder on the local computer.

This repository and its GitHub Pages site are public. Only the static application shell belongs in git. Never commit patient names, initials, DOB, identifying chart numbers, photos, intraoral scans, STLs, visit notes, real case lists, or other PHI.

Files remain on the practice computer's disk. The only browser-persisted value is the selected directory handle in IndexedDB; filenames, paths, Case IDs, dates, and queue data are not persisted in browser storage. Files never upload, and this site is not a backup. Case ID means the practice work-order number, not a patient identifier.

The app requires current desktop Chrome or compatible Chromium on HTTPS or localhost. To deploy, place the repository on GitHub and publish Pages from the `master` branch and repository root. The app uses `<base href="/practice-files/">`; keep `.nojekyll` at the root. For local preview, serve it at `/practice-files/` on localhost rather than opening it with `file://`.

This app is a tool only, not a patient chart. This app is not HIPAA certified and does not claim HIPAA compliance.
