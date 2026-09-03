# IHS Practice Files

[https://in-housesystems.com/practice-files/](https://in-housesystems.com/practice-files/)

IHS Practice Files is a static folder tool for desktop Chrome. Connect a practice-owned folder on this computer. Selected files are copied into `CaseID/VisitDate/{scans,notes,design,print}` on disk.

This repository and its GitHub Pages site are public. Only the static application shell belongs in git. Never commit patient names, initials, DOB, identifying chart numbers, photos, intraoral scans, STLs, visit notes, real case lists, or other PHI.

Files never leave the practice computer. Nothing is uploaded to GitHub, IHS Drive, or any server. The only browser-persisted value is the selected directory handle in IndexedDB. Filenames, paths, Case IDs, dates, and queue data are not stored in the browser. Forgetting the folder removes this browser's connection and does not delete files.

Case ID means the practice work-order number, not a patient identifier. Until a folder is connected, the page shows DEMO-only fake Case IDs.

This app is a tool only, not a patient chart. This app is not HIPAA certified and does not claim HIPAA compliance. File and folder names can contain patient information; they stay on disk and are never logged, synced, or analyzed.

The app requires current desktop Chrome or compatible Chromium on HTTPS or localhost. To deploy, publish GitHub Pages from the `master` branch and repository root. The app uses `<base href="/practice-files/">`; keep `.nojekyll` at the root. For local preview, serve it at `/practice-files/` on localhost rather than opening it with `file://`.
