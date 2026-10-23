fixture_evidence/ contents (req-20261023-001, A route)
- conmebol_2022_fase12.pdf (194,980 bytes, HTTP 200, sha256 54f9acdc5344759a5d0c1c373f64d7f8fc7d5ec047939c95655ec7d2d595e95c)
- conmebol_2022_fase3.pdf (155,797 bytes, HTTP 200, sha256 83c0f73aa46d1b3030a1f2ed05d294f17e814bef3b33bc755b578c65d03941e2)
- conmebol_2024_qf.pdf (71,765 bytes, HTTP 200, sha256 5569f5b2cf3421e23153582199d716fa5c037c8d4b185da498e51d2d81bc7334)
  All three downloaded by curl on 2026-10-23 (21:23 CST); hashes reproduced identically
  in the probe pass and the download pass. PDFs are 1 page each.
  NOTE: an earlier curl probe of the 2024 QF URL returned CloudFront 403; the
  block is intermittent. The downloaded bytes above were verified as PDF
  (%PDF-1.6 / %PDF-1.7) and parsed with pdftotext -layout, so the 403 was a
  transient access failure, not evidence the file does not exist.
- curl_probe_log.json: one curl attempt per FBref season URL (8) and per CONMEBOL
  PDF URL (3), with HTTP status / curl exit code / body sha256 of whatever was
  returned. WARNING: body sha256 values in the probe log for FBref URLs are
  hashes of Cloudflare challenge pages (403) or empty replies (000), NOT of
  fixture data. They must never be used as source_sha256 for inventory rows.
  FBref rows therefore carry source_sha256=null with retrieval_method
  'browser text layer' (see per-season note files), not curl bytes.
- fbref_YYYY_textlayer_note.txt (per season, written by the FBref season agents):
  browser-text-layer retrieval notes; no FBref page bytes were downloaded.
