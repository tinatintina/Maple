# Maple Freight — Dispatch Action Report
**As of:** 2026-09-21 06:47:27 PM EDT (backfill update; original 6 p.m. snapshot preserved)
**Source:** supplied CSV exports only. **Action capacity:** up to 10/day, not a quota.

## Three evidence-backed actions
These are selected high-confidence cases, not a proof that all other fleet issues are resolved.

### 1. V-108 — P1 / immediate
**Depot:** Hamilton Depot. **Reason:** Two newly delivered critical faults: P0217 overheating and P0524 low oil pressure; earlier WO-5512 repaired a different P0171 condition.
**Next action:** Maintenance lead and dispatch: urgently locate and hold V-108 pending mechanical assessment; confirm whether it is currently assigned.
**Supporting alerts:**
- A-790647: DTC P0171 (System too lean (bank 1); reference: Medium - inspect at next service); vendor MEDIUM; event 2026-09-08 11:31:27 AM EDT; received 2026-09-08 11:31:43 AM EDT; delay 0.3 min.
- A-894448: DTC P0420 (Catalyst system efficiency below threshold; reference: Low - emissions, schedule repair); vendor LOW; event 2026-09-09 06:20:15 PM EDT; received 2026-09-09 06:21:30 PM EDT; delay 1.2 min.
- A-120811: DTC P0217 (Engine coolant over-temperature condition; reference: Critical - stop vehicle, risk of engine damage); value 107 C; vendor MEDIUM; event 2026-09-21 12:05:00 PM EDT; received 2026-09-21 06:47:00 PM EDT; delay 402.0 min.
- A-707191: DTC P0524 (Engine oil pressure too low; reference: Critical - stop vehicle immediately); value 88 kPa; vendor MEDIUM; event 2026-09-21 03:41:00 PM EDT; received 2026-09-21 06:47:15 PM EDT; delay 186.2 min.
**Shop record:** WO-5512 (Closed; opened 2026-09-08 15:20 local; closed 2026-09-09 11:05; Replaced intake manifold gasket; note: P0171 lean condition resolved. Test drive OK.)


### 2. V-137 — P1 / immediate
**Depot:** North Yard. **Reason:** Critical P0524 after an earlier sensor-related P0217 repair.
**Next action:** Maintenance lead: hold from dispatch pending an immediate oil-pressure assessment; do not assume the earlier repair cleared this new fault.
**Supporting alerts:**
- A-815916: DTC P0217 (Engine coolant over-temperature condition; reference: Critical - stop vehicle, risk of engine damage); value 104 C; vendor MEDIUM; event 2026-09-17 02:57:00 PM EDT; received 2026-09-17 02:58:11 PM EDT; delay 1.2 min.
- A-458608: DTC P0217 (Engine coolant over-temperature condition; reference: Critical - stop vehicle, risk of engine damage); value 109 C; vendor MEDIUM; event 2026-09-18 12:46:00 PM EDT; received 2026-09-18 12:47:27 PM EDT; delay 1.4 min.
- A-149353: DTC P0217 (Engine coolant over-temperature condition; reference: Critical - stop vehicle, risk of engine damage); value 113 C; vendor MEDIUM; event 2026-09-19 02:27:00 PM EDT; received 2026-09-19 02:27:15 PM EDT; delay 0.2 min.
- A-856950: DTC P0217 (Engine coolant over-temperature condition; reference: Critical - stop vehicle, risk of engine damage); value 118 C; vendor MEDIUM; event 2026-09-20 11:30:00 AM EDT; received 2026-09-20 11:30:19 AM EDT; delay 0.3 min.
- A-784686: DTC P0524 (Engine oil pressure too low; reference: Critical - stop vehicle immediately); value 96 kPa; vendor MEDIUM; event 2026-09-21 02:32:00 PM EDT; received 2026-09-21 02:32:06 PM EDT; delay 0.1 min.
**Shop record:** WO-5540 (Closed; opened 2026-09-20 16:00 local; closed 2026-09-21 07:40; Replaced coolant temperature sensor; note: P0217 readings traced to a faulty sensor. Codes cleared. OK to dispatch.)


### 3. V-158 — P2 / before dispatch
**Depot:** North Yard. **Reason:** P0300 misfire with open inspection work order.
**Next action:** Maintenance lead and dispatch: confirm inspection and assignment status before the next dispatch.
**Supporting alerts:**
- A-892055: DTC P0171 (System too lean (bank 1); reference: Medium - inspect at next service); vendor MEDIUM; event 2026-09-08 10:33:45 AM EDT; received 2026-09-08 10:34:15 AM EDT; delay 0.5 min.
- A-828307: DTC P0420 (Catalyst system efficiency below threshold; reference: Low - emissions, schedule repair); vendor LOW; event 2026-09-15 12:11:38 PM EDT; received 2026-09-15 12:12:56 PM EDT; delay 1.3 min.
- A-223397: maintenance_due; value 43 km_overdue; vendor MEDIUM; event 2026-09-20 06:00:00 AM EDT; received 2026-09-20 06:00:57 AM EDT; delay 0.9 min.
- A-925652: maintenance_due; value 43 km_overdue; vendor MEDIUM; event 2026-09-20 06:00:00 AM EDT; received 2026-09-20 06:01:00 AM EDT; delay 1.0 min.
- A-967332: DTC P0128 (Coolant thermostat below regulating temperature; reference: Low - monitor); value 61 C; vendor LOW; event 2026-09-20 01:27:39 PM EDT; received 2026-09-20 01:29:03 PM EDT; delay 1.4 min.
- A-468820: DTC P0300 (Random/multiple cylinder misfire detected; reference: High - inspect within 24 h); vendor HIGH; event 2026-09-21 05:09:01 PM EDT; received 2026-09-21 05:10:23 PM EDT; delay 1.4 min.
**Shop record:** WO-5543 (Open; opened 2026-09-21 17:30 local; closed not recorded; Misfire inspection; note: Booked first thing 2026-09-22.)

## Export checks
- 2380 raw alerts (2370 original + 10 backfill); 2380 at or before the selected event/receipt cutoff; 60 vehicles; 9 work orders.
- Unique alert IDs: 2380; repeated IDs: 0. This does not rule out repeated underlying events.
- Engine-fault alerts: 139; speeding alerts: 414; speeding alerts without posted limit: 86.
- Alerts received >24 hours after event: 21; negative delivery delays: 0.
- Event time and received time are separate; displayed in Toronto local time. Work-order times are already local.
- Hamilton gateway outage contradicts vendor connectivity notes; late receipt does not make the underlying event new.

## Ranking and limitations
- P1: critical reference DTC with no documented resolution after its latest event; P2: high-reference fault requiring prompt inspection or a combined unresolved concern.
- This intentionally outputs three selected cases, not ten manufactured tasks. It is not a complete fleet-wide triage engine.
- Repeated alerts are grouped by vehicle in this report; distinct fault codes and their timestamps remain visible.
- Vendor severity is retained as evidence, not treated as authoritative for DTC urgency.
- A work order closing does not prove a different subsequent fault is resolved.
- Missing speed limits, firmware-dependent harsh-event sensitivity and delayed receipt make naive driver ranking unreliable.
- Nightly device interruptions may be expected according to vendor notes; they are not investigated in this minimal report.
- This report recommends human review; it does not certify mechanical safety or dispatch clearance.


## What changed after the new information
- Hamilton Depot gateway reconnected at 6:47 p.m. EDT and delivered 10 alerts; these were not visible at the original 6:00 p.m. cutoff.
- V-108 becomes first priority: A-120811 P0217 at 12:05 p.m. EDT (received 6:47 p.m.), and A-707191 P0524 at 3:41 p.m. EDT (received 6:47 p.m.). Both are critical despite vendor MEDIUM.
- WO-5512 closed September 9 for P0171; it does not resolve the new P0217/P0524 faults.
- V-151 remains a known follow-up (A-668410 misfire and A-927832 2,350 km overdue), but moves below the top three, not cleared.
- The remaining eight backfill records are retained and inspectable in the source explorer; this minimal report does not certify them as harmless.
