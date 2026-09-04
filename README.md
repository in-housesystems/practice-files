# IHS Practice Files

https://in-housesystems.com/practice-files/

Desktop Chrome folder tool for a dental practice. Connect a practice-owned folder on this computer. Selected files are copied into `CaseID/VisitDate/{scans,notes,design,print}` on disk. Optional phone camera JPEGs save into `CaseID/VisitDate/notes/photos/`.

Files never leave this PC. Nothing is uploaded. This is a tool only, not a patient chart.

## Use it

Open the live URL in current desktop Chrome (HTTPS).

1. **Connect folder** — pick a dedicated local-only folder the practice owns. Do not use this git checkout. Do not use OneDrive, Dropbox, or iCloud Drive. File System Access often cannot show the full path, so confirm in Explorer that the folder is on this PC.
2. **Copy files** — Case ID is the practice work-order number. Set the visit date and a bucket (`scans`, `notes`, `design`, or `print`). Selected files are copied on disk.
3. **Phone photos (optional)** — same Wi‑Fi, folder connected, Case ID and visit date set. From this folder run `python photo-bridge.py` and leave it running. Scan the Intake QR. Use the live camera, not Camera Roll. JPEGs land in `notes/photos/` on this PC. The phone discards the photo. Do not email photos; they must not remain on the phone.

Until a folder is connected, the page shows DEMO-only fake Case IDs. Forgetting the folder removes this browser's connection and does not delete files. The only browser-persisted value is the selected directory handle. Filenames, paths, Case IDs, dates, queue data, and photos are not stored in the browser.

## Rules

- This repository and its GitHub Pages site are public. Only the static application shell belongs in git. Never commit patient names, initials, DOB, identifying chart numbers, photos, intraoral scans, STLs, visit notes, real case lists, or other PHI.
- Case ID means the practice work-order number, not a patient identifier.
- This app is not a patient chart. This app is not HIPAA certified and does not claim HIPAA compliance. File and folder names can contain patient information; they stay on disk and are never logged, synced, or analyzed.
- Photo blobs stay in memory only. The photo-bridge is signaling; it never writes photos.
