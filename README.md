# IHS Practice Files

[https://in-housesystems.com/practice-files/](https://in-housesystems.com/practice-files/)

IHS Practice Files is a static folder tool for desktop Chrome. Connect a practice-owned folder on this computer. Selected files are copied into `CaseID/VisitDate/{scans,notes,design,print}` on disk. Phone camera JPEGs save into `CaseID/VisitDate/notes/photos/`.

This repository and its GitHub Pages site are public. Only the static application shell belongs in git. Never commit patient names, initials, DOB, identifying chart numbers, photos, intraoral scans, STLs, visit notes, real case lists, or other PHI.

Files never leave the practice computer. Nothing is uploaded to GitHub, IHS Drive, or any server. The only browser-persisted value is the selected directory handle in IndexedDB. Filenames, paths, Case IDs, dates, queue data, and photos are not stored in the browser. Photo blobs stay in memory only, with no service worker and no IndexedDB of images. Forgetting the folder removes this browser's connection and does not delete files.

Case ID means the practice work-order number, not a patient identifier. Until a folder is connected, the page shows DEMO-only fake Case IDs.

This app is a tool only, not a patient chart. This app is not HIPAA certified and does not claim HIPAA compliance. File and folder names can contain patient information; they stay on disk and are never logged, synced, or analyzed.

The app requires current desktop Chrome or compatible Chromium on HTTPS or localhost. To deploy, publish GitHub Pages from the `master` branch and repository root. The app uses `<base href="/practice-files/">`; keep `.nojekyll` at the root. For local preview, serve it at `/practice-files/` on localhost rather than opening it with `file://`.

## Local practice folder

Connect a dedicated local-only folder that the practice owns. Do not use this git checkout. Do not use OneDrive, Dropbox, or iCloud Drive. File System Access often cannot show the full path, so confirm in Explorer that the folder is on this PC and not cloud-synced.

## Phone camera

Desktop Intake, after the folder is connected and granted and a Case ID plus visit date are set:

1. PC on, desktop Chrome open at [https://in-housesystems.com/practice-files/](https://in-housesystems.com/practice-files/).
2. Practice folder connected and access granted.
3. Phone and PC on the same Wi‑Fi.
4. From this folder run `python photo-bridge.py` and leave it running. The desktop page fetches `http://127.0.0.1:17831` only. The bridge is signaling; it never writes photos and never logs SDP to disk.
5. Scan the Intake QR. The phone opens `#/capture` on the live HTTPS origin, uses the live camera (not Camera Roll), sends a JPEG over a same-LAN WebRTC datachannel, waits for the PC to acknowledge a finished write, then discards the photo. If the link fails, the phone still discards it.
6. Files land in `CaseID/VisitDate/notes/photos/` as `YYYY-MM-DD_HHMMSS_xxxx.jpg` (timestamp plus short random; no patient name; no colons). Incomplete writes use a `.part` temp and are not treated as saved.

Do not email photos. Photos must not remain on the phone. There is no download, share sheet, or file picker on the capture page.

A later local-only transcription path may be added on this PC. It will not send audio or notes to a cloud inbox.

## Git

Image and `.part` files are gitignored. Optional: copy `hooks/pre-commit` to `.git/hooks/pre-commit` if you want this clone to block image commits. Do not change git config.
