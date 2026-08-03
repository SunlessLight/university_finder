/**
 * Code.gs — pending-response feed for the university-finder Stage 1 intake.
 *
 * This file is the SOURCE OF TRUTH for the script that lives inside the Google
 * Form's responses spreadsheet. Edit it here, commit it, then paste it into the
 * bound Apps Script project (Extensions -> Apps Script) and redeploy.
 *
 * WHAT IT DOES
 *   Exposes the responses sheet as two HTTP actions so
 *   tools/fetch_form_responses.py can pull only rows that have not been ingested
 *   yet, and stamp them as done afterwards:
 *
 *     ?action=pending&token=...              -> {headers, rows, row_numbers}
 *     ?action=confirm&token=...&rows=12,13   -> {stamped:[12,13]}
 *
 *   "Not ingested yet" is recorded IN THE SHEET, in a column called
 *   `Ingested at` (see INGESTED_HEADER). Blank cell = pending. A timestamp =
 *   already turned into a data/students/<slug>/ folder. Keeping the marker in
 *   the sheet rather than on disk means it survives a wiped `data/` folder and a
 *   different machine.
 *
 * ---------------------------------------------------------------------------
 * TWO CONSTRAINTS THIS FILE IS BUILT AROUND — do not "clean these up":
 *
 * 1. ROW IDENTITY IS THE SHEET ROW NUMBER.
 *    Safe only because Google Forms APPENDS responses and never reorders them.
 *    SORTING THE RESPONSES SHEET BY HAND WILL BREAK THE MAPPING between a
 *    fetched CSV and the rows `--confirm` stamps. Filter views are fine (they
 *    do not move the underlying rows); an actual Data -> Sort range is not.
 *
 * 2. EVERYTHING IS GET. THERE IS DELIBERATELY NO doPost().
 *    A web app deployed with access "Anyone" answers with a 302 redirect to
 *    googleusercontent.com. Python's urllib silently downgrades a redirected
 *    POST to a GET, which DROPS THE REQUEST BODY — a confirm would look like it
 *    succeeded and stamp nothing. Routing both actions through GET avoids the
 *    trap entirely. Mutating on GET is impure, but this is a private,
 *    single-user endpoint and correctness beats purity here.
 * ---------------------------------------------------------------------------
 *
 * SECURITY
 *   The deployed URL is public, so every request must carry a shared token.
 *   The expected value lives in Script Properties under FORM_TOKEN
 *   (Project Settings -> Script Properties) and is NEVER inlined here — this
 *   file is committed to git. The token is checked BEFORE the sheet is touched.
 *   To revoke access: change FORM_TOKEN and redeploy.
 */

/** Header of the bookkeeping column. Must match INGESTED_HEADER in fetch_form_responses.py. */
var INGESTED_HEADER = 'Ingested at';

/** Script Property holding the shared secret. Set it in Project Settings, not here. */
var TOKEN_PROPERTY = 'FORM_TOKEN';


/**
 * Single entry point. Routes on ?action= and always returns JSON.
 */
function doGet(e) {
  var params = (e && e.parameter) || {};

  // --- Token gate. Runs before anything reads or writes the sheet. ---
  var expected = PropertiesService.getScriptProperties().getProperty(TOKEN_PROPERTY);
  if (!expected) {
    return jsonOut({ error: 'server_misconfigured', detail: TOKEN_PROPERTY + ' script property is not set' });
  }
  if (params.token !== expected) {
    return jsonOut({ error: 'unauthorized' });
  }

  var action = params.action || 'pending';

  try {
    if (action === 'pending') {
      return jsonOut(getPending());
    }
    if (action === 'confirm') {
      return jsonOut(confirmRows(params.rows || ''));
    }
    return jsonOut({ error: 'unknown_action', detail: action });
  } catch (err) {
    return jsonOut({ error: 'script_error', detail: String(err) });
  }
}


/**
 * Return every row whose `Ingested at` cell is blank.
 *
 * Returns JSON rather than CSV on purpose: form answers contain commas, quotes
 * and newlines, and Google's exact header strings must survive verbatim because
 * QUESTION_MAP in ingest_form_csv.py matches on them. Python's stdlib csv module
 * does the quoting on the other end.
 *
 * The `Ingested at` column itself is stripped from the payload — it is
 * bookkeeping, not a form answer, and there is no reason to ship it downstream.
 */
function getPending() {
  var sheet = getSheet();
  var lastRow = sheet.getLastRow();
  var lastCol = sheet.getLastColumn();

  var headers = sheet.getRange(1, 1, 1, lastCol).getValues()[0];
  var markerCol = ensureIngestedColumn(sheet, headers); // 1-based; may extend headers

  // Header row only (or a totally empty sheet) => nothing to hand back.
  if (lastRow < 2) {
    return { headers: stripMarker(headers, markerCol), rows: [], row_numbers: [] };
  }

  // Re-read width: ensureIngestedColumn() may have just appended the marker.
  lastCol = sheet.getLastColumn();
  headers = sheet.getRange(1, 1, 1, lastCol).getValues()[0];

  var values = sheet.getRange(2, 1, lastRow - 1, lastCol).getValues();

  var rows = [];
  var rowNumbers = [];

  for (var i = 0; i < values.length; i++) {
    var row = values[i];
    var marker = row[markerCol - 1];

    // Blank marker = pending. A Forms row can never be blank across the board
    // (Timestamp is always written), so a fully empty row is spreadsheet cruft
    // — skip it rather than handing back a phantom respondent.
    if (marker !== '' && marker !== null) continue;
    if (isBlankRow(row)) continue;

    rows.push(stripMarker(row, markerCol).map(normalizeCell));
    rowNumbers.push(i + 2); // +2: values[] starts at sheet row 2
  }

  return {
    headers: stripMarker(headers, markerCol),
    rows: rows,
    row_numbers: rowNumbers
  };
}


/**
 * Stamp `Ingested at` for each named sheet row.
 *
 * `rows` is the comma-separated list fetch_form_responses.py read back out of
 * the `_row` column of data/form/responses.csv. Anything out of range is
 * reported in `skipped` rather than silently ignored, so a mismatch between the
 * CSV on disk and the sheet is visible instead of quiet.
 */
function confirmRows(rowsParam) {
  var sheet = getSheet();
  var lastRow = sheet.getLastRow();
  var lastCol = sheet.getLastColumn();

  var headers = sheet.getRange(1, 1, 1, lastCol).getValues()[0];
  var markerCol = ensureIngestedColumn(sheet, headers);

  var wanted = String(rowsParam)
    .split(',')
    .map(function (s) { return parseInt(s.trim(), 10); })
    .filter(function (n) { return !isNaN(n); });

  if (!wanted.length) {
    return { error: 'no_rows', detail: 'confirm called without a usable rows= list' };
  }

  var stamp = new Date();
  var stamped = [];
  var skipped = [];

  for (var i = 0; i < wanted.length; i++) {
    var rowNum = wanted[i];
    if (rowNum < 2 || rowNum > lastRow) {
      skipped.push(rowNum);
      continue;
    }
    sheet.getRange(rowNum, markerCol).setValue(stamp);
    stamped.push(rowNum);
  }

  // Force the writes out before the response returns, so a caller that
  // immediately re-fetches sees the stamps.
  SpreadsheetApp.flush();

  return { stamped: stamped, skipped: skipped };
}


/* ------------------------------------------------------------------ helpers */


/**
 * The sheet the form writes into. Uses the ACTIVE sheet of the bound
 * spreadsheet — correct for the standard one-form-one-sheet setup.
 */
function getSheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  if (!ss) throw new Error('No bound spreadsheet — this script must be created from Extensions -> Apps Script inside the responses sheet.');
  var sheet = ss.getSheets()[0];
  if (!sheet) throw new Error('Bound spreadsheet has no sheets.');
  return sheet;
}


/**
 * Find the `Ingested at` column, creating it as the LAST column if absent.
 *
 * Located by HEADER NAME on every call, never by a cached index: Forms appends a
 * new column whenever a question is added to the form, which shifts this one
 * right. Appending at the end (rather than inserting at the front) is what keeps
 * the form-owned block of columns undisturbed.
 *
 * @return {number} 1-based column index of the marker column.
 */
function ensureIngestedColumn(sheet, headers) {
  for (var i = 0; i < headers.length; i++) {
    if (String(headers[i]).trim() === INGESTED_HEADER) return i + 1;
  }
  var col = sheet.getLastColumn() + 1;
  sheet.getRange(1, col).setValue(INGESTED_HEADER);
  SpreadsheetApp.flush();
  headers.push(INGESTED_HEADER);
  return col;
}


/** Copy of `arr` without the marker column. */
function stripMarker(arr, markerCol) {
  var out = [];
  for (var i = 0; i < arr.length; i++) {
    if (i === markerCol - 1) continue;
    out.push(arr[i]);
  }
  return out;
}


/**
 * Make a cell safe to JSON-encode and stable across fetches.
 *
 * Dates (the Timestamp column) are serialised in the SHEET'S OWN TIMEZONE, not as
 * the ISO UTC string JSON.stringify would emit — otherwise every timestamp would
 * silently shift by the UTC offset (8 hours, for a Malaysian form).
 *
 * NOTE: this deliberately does NOT reproduce Google's manual-export format.
 * "Download responses (.csv)" writes M/d/yyyy H:mm:ss ('7/26/2026 21:46:16');
 * this writes yyyy-MM-dd HH:mm:ss ('2026-07-30 10:05:54'). Verified 2026-08-03.
 * ISO is kept on purpose: it sorts correctly and can't be misread as d/M. Safe
 * because ingest_form_csv.py never reads the Timestamp column (no QUESTION_MAP
 * entry, zero references). If anything downstream ever starts parsing it, decide
 * the format THERE rather than reverting this to Google's ambiguous one.
 */
function normalizeCell(v) {
  if (v === null || v === undefined) return '';
  if (Object.prototype.toString.call(v) === '[object Date]') {
    return Utilities.formatDate(v, SpreadsheetApp.getActiveSpreadsheet().getSpreadsheetTimeZone(), 'yyyy-MM-dd HH:mm:ss');
  }
  return String(v);
}


/** True if every cell in the row is empty. */
function isBlankRow(row) {
  for (var i = 0; i < row.length; i++) {
    if (row[i] !== '' && row[i] !== null && row[i] !== undefined) return false;
  }
  return true;
}


/** Serialise a value as a JSON HTTP response. */
function jsonOut(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
