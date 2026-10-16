# Maple Freight: Dispatch Action Report

A small, auditable report for the operations manager at **September 21, 2026, 6:00 p.m. America/Toronto**. It uses only the supplied synthetic exports and Python's standard library.

## How to run it

On macOS, with Python 3.9+ installed:

```bash
python3 report.py
python3 -m unittest -v
```

Open `DISPATCH_REPORT.md` in VS Code (Markdown Preview: Cmd+Shift+V). No `pip install`, API key, or hosting required. Keep the five supplied files in `data/` with the exact filenames shown. Running the script overwrites `DISPATCH_REPORT.md` deterministically.

## Tonight's top 3 for Maple Freight

1. **Item:** V-137 — critical oil-pressure alert after a different repair. **Why it matters:** P0524 is critical in the supplied DTC reference, although the vendor called it MEDIUM. **Evidence:** `A-784686`, P0524, 96 kPa, Sep 21 2:32 p.m. EDT; `WO-5540` closed Sep 21 7:40 a.m. after replacing a coolant sensor for earlier P0217 readings. **Next action (who, by when):** Maintenance lead: urgently check oil pressure and coordinate holding V-137 from dispatch until assessed, tonight.
2. **Item:** V-158 — misfire inspection pending. **Why it matters:** P0300 requires inspection within 24 hours per the supplied reference. **Evidence:** `A-468820`, P0300, Sep 21 5:09:01 p.m. EDT; open `WO-5543` booked for Sep 22. **Next action (who, by when):** Maintenance and dispatch: confirm inspection and assignment plan before the 6 a.m. dispatch.
3. **Item:** V-151 — misfire plus overdue maintenance. **Why it matters:** A P0300 fault and 2,350 km overdue service combine into one vehicle-readiness decision. **Evidence:** `A-668410`, P0300, Sep 20 3:09:50 p.m. EDT; `A-927832`, 2,350 km overdue, Sep 21 6 a.m.; `WO-5541` scheduled for Oct 5. **Next action (who, by when):** Maintenance lead: review misfire and service scheduling together before dispatch.

These are selected evidence-backed cases, **not** a claim that all other vehicles are cleared or that the top three are an exhaustive fleet-wide ranking.

## What I built, and for whom

`report.py` reads the actual provided CSVs and writes `DISPATCH_REPORT.md`, a static report for an operations manager to review tonight and before tomorrow's dispatch. It shows three grouped vehicle issues, every source alert of relevant types for each selected vehicle, vendor severity, DTC meaning/reference urgency, local event and receipt timestamps, delays, and associated work orders. It also shows dataset checks and caveats.

## Assumptions I made

- Both event and received timestamps must be at or before the fixed assessment cutoff; a later-received event is not yet known to operations at that time.
- `event_time_utc` is occurrence time, not receipt time; work-order times are local Toronto times as described in the brief.
- Vehicle-level grouping is suitable for an operations manager, but different DTCs are kept visible separately; a closed work order for one fault does not automatically clear another.
- The supplied DTC reference is more suitable than vendor severity for mechanical urgency. Fault presence is not itself a mechanical diagnosis.
- A team capacity of ten is an upper bound, not a target; this baseline intentionally selects only three well-supported issues.
- No new post-export work-order updates are available. Human review is required before deciding vehicle readiness.

## What I deliberately did NOT do (and why)

- No paid AI, model-generated risk scores, API calls, hosting, authentication, or live feed: they add dependencies without improving this small, auditable decision.
- No claim of exhaustive fleet-wide triage: this is a **curated three-case baseline**, not a dynamic engine that finds every unresolved issue.
- No driver leaderboard: distance exposure and firmware sensitivity make raw alert counts misleading.
- No automated speed enforcement: 85 speeding alerts lack posted limits, and no road context is supplied.
- No blanket suppression of device alerts: vendor notes describe expected 11 p.m.–midnight interruptions, but not every interruption is necessarily benign.
- No automatic dispatch approval or vehicle safety certification: only authorized staff can make those decisions.

## How I checked it's correct

Run `python3 -m unittest -v`. Tests verify the fixed cutoff, all 2,370 input alerts, V-137's critical-but-MEDIUM alert and work order, V-158's open order, V-151's misfire and maintenance alert, and three displayed action cards. The generated report also reports duplicate alert IDs, counts, missing speeding limits, and delayed deliveries. A unique alert ID does not guarantee a unique underlying event. The vendor's exactly-once delivery and nightly-update claims are treated as vendor statements, not independently verified facts.

## AI use

- **Tools I used:** ChatGPT for reasoning and code assistance; Python standard library for reproducible execution.
- **What AI did for me:** Helped inspect the supplied records, outline the three actions, generate the script and verification tests, and document assumptions.
- **One thing AI got wrong or incomplete, and how I caught it:** An earlier summary described V-151 primarily as overdue for service; checking `A-668410` also showed a P0300 misfire. The report now groups both concerns in one vehicle issue.
- **Link to / export of my AI session:** Add the actual shared conversation link or exported transcript before submission.

## If I had two more days

Build a full fleet-wide issue engine with time-aware fault/work-order matching, explicit status resolution, configurable priority rules, tests for event-level duplicate patterns, and a driver review normalized by kilometres and firmware. Validate ranking with maintenance and operations before use.

## Optional local UI

A read-only Streamlit interface (`app.py`) displays the same verified three cases,
expandable source evidence, data-quality notes, and browsable original CSV records.
It reuses `report.build()`; it does not introduce new prioritization claims.

```bash
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
```

The browser opens on your Mac (typically `http://localhost:8501`). No API key,
account, hosting, or external fleet data is required. To regenerate the standalone
Markdown report, run `python3 report.py`. Verify with `python3 -m unittest -v`.
