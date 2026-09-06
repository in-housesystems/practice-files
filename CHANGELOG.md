# IHS Practice Files changelog

Newest first. This is the human list of what went live. GitHub still has the technical commits.

## Sep 5, 2026 — Faster keyboard navigation

- Added a keyboard-visible skip link to jump directly past the sticky navigation.
- Labeled the primary navigation for screen readers.
- Folder handling, photo transfer, storage boundaries, and the live URL did not change.
- Local scratch output under `__grok/` is now ignored.

## Sep 5, 2026 — Queue continue into Intake

- Real Queue case cards now have **Continue in Intake** next to **Open case in app**.
- Continue fills Case ID, the latest visit date, and the next empty lab stage (scans → design → print, else notes), then opens Intake so the next-stage files can be dropped without retyping.
- Open case in app is still the on-page file list. DEMO cards are unchanged.

## Sep 4, 2026 — Architecture pass (no change)

- Looked at the live app and this repo. No structure change was needed.
- Already a one-file GitHub Pages shell, local folder writes on this PC, and a signaling-only photo-bridge. The bridge never writes photos.
- Pages never sees the files. The bridge never sees JPEG bytes. The phone never keeps them. Chrome writes to disk.
- Live URL, `CaseID/VisitDate/{scans,notes,design,print}` plus `notes/photos`, and this-PC-only storage stay as they are.

## Sep 2, 2026 — Phone camera WebRTC JPEG path

- Optional phone camera from Intake, after a folder is connected and a Case ID plus visit date are set
- Same Wi‑Fi. Run `python photo-bridge.py`. Scan the QR. Live camera JPEG over a local WebRTC datachannel into `CaseID/VisitDate/notes/photos/`
- The bridge is signaling only. It never writes photos. Photo blobs stay in memory. The phone discards the photo after the PC finishes the write
- Do not email photos. Photos must not remain on the phone

## Sep 2, 2026 — v1 goes live

- Live at https://in-housesystems.com/practice-files/
- Desktop Chrome folder tool. Connect a practice-owned folder on this PC
- Selected files copy into `CaseID/VisitDate/{scans,notes,design,print}`
- Files stay on disk. Nothing is uploaded. Not a patient chart. Not HIPAA certified
