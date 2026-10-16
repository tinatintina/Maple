"""Generate an auditable dispatch report from the supplied Maple Freight exports."""
import csv
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data'
REFERENCE = datetime(2026, 9, 21, 18, tzinfo=ZoneInfo('America/Toronto'))
BACKFILL_RECEIVED = datetime(2026, 9, 21, 18, 47, 27, tzinfo=ZoneInfo('America/Toronto'))


def rows(name):
    with (DATA / name).open(newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def utc_time(s):
    return datetime.fromisoformat(s.replace('Z', '+00:00'))


def local_time(s):
    return datetime.strptime(s, '%Y-%m-%d %H:%M').replace(tzinfo=ZoneInfo('America/Toronto')) if s else None


def fmt(dt):
    return dt.astimezone(ZoneInfo('America/Toronto')).strftime('%Y-%m-%d %I:%M:%S %p %Z')


def build(include_backfill=False):
    raw = rows('alerts.csv')
    added = rows('hamilton_backfill.csv') if include_backfill else []
    all_alerts = raw + added
    cutoff = BACKFILL_RECEIVED if include_backfill else REFERENCE
    vehicles = {v['vehicle_id']: v for v in rows('vehicles.csv')}
    dtcs = {d['dtc_code']: d for d in rows('dtc_reference.csv')}
    orders = rows('work_orders.csv')
    eligible = [a for a in all_alerts if utc_time(a['event_time_utc']) <= cutoff and utc_time(a['received_time_utc']) <= cutoff]
    by_vehicle = defaultdict(list)
    for a in eligible:
        by_vehicle[a['vehicle_id']].append(a)
    for group in by_vehicle.values():
        group.sort(key=lambda a: utc_time(a['event_time_utc']))

    def order_text(v):
        related = [w for w in orders if w['vehicle_id'] == v]
        if not related:
            return 'No work order in supplied file.'
        return '; '.join(f"{w['wo_id']} ({w['status']}; opened {w['opened_local']} local; closed {w['closed_local'] or 'not recorded'}; {w['work_done']}; note: {w['technician_note']})" for w in related)

    def evidence(v, types):
        return [a for a in by_vehicle[v] if a['alert_type'] in types]

    def line(a):
        detail = f"DTC {a['dtc_code']} ({dtcs[a['dtc_code']]['meaning']}; reference: {dtcs[a['dtc_code']]['reference_urgency']})" if a['dtc_code'] in dtcs else a['alert_type']
        value = f"; value {a['value']} {a['unit']}" if a['value'] else ''
        delay = (utc_time(a['received_time_utc']) - utc_time(a['event_time_utc'])).total_seconds() / 60
        return f"- {a['alert_id']}: {detail}{value}; vendor {a['vendor_severity']}; event {fmt(utc_time(a['event_time_utc']))}; received {fmt(utc_time(a['received_time_utc']))}; delay {delay:.1f} min."

    cases = [
        ('V-137', 'P1 / immediate', 'Critical P0524 after an earlier sensor-related P0217 repair',
         'Maintenance lead: hold from dispatch pending an immediate oil-pressure assessment; do not assume the earlier repair cleared this new fault.',
         ['engine_fault']),
        ('V-158', 'P2 / before dispatch', 'P0300 misfire with open inspection work order',
         'Maintenance lead and dispatch: confirm inspection and assignment status before the next dispatch.',
         ['engine_fault', 'maintenance_due']),
        ('V-151', 'P2 / before dispatch', 'P0300 misfire plus substantial overdue service',
         'Maintenance lead: assess misfire and 2,350-km service overrun together; decide vehicle readiness and whether to accelerate service.',
         ['engine_fault', 'maintenance_due']),
    ]
    if include_backfill:
        cases = [
            ('V-108', 'P1 / immediate', 'Two newly delivered critical faults: P0217 overheating and P0524 low oil pressure; earlier WO-5512 repaired a different P0171 condition',
             'Maintenance lead and dispatch: urgently locate and hold V-108 pending mechanical assessment; confirm whether it is currently assigned.', ['engine_fault']),
            cases[0], cases[1],
        ]
    out = [
        '# Maple Freight — Dispatch Action Report',
        f'**As of:** {fmt(cutoff)} ({"backfill update; original 6 p.m. snapshot preserved" if include_backfill else "fixed assessment cutoff"})',
        f'**Source:** supplied CSV exports only. **Action capacity:** up to 10/day, not a quota.',
        '',
        '## Three evidence-backed actions',
        'These are selected high-confidence cases, not a proof that all other fleet issues are resolved.',
    ]
    for i, (v, tier, reason, action, types) in enumerate(cases, 1):
        info = vehicles[v]
        out.extend(['', f'### {i}. {v} — {tier}', f'**Depot:** {info["depot"]}. **Reason:** {reason}.', f'**Next action:** {action}', '**Supporting alerts:**'])
        for a in evidence(v, types):
            out.append(line(a))
        out.extend([f'**Shop record:** {order_text(v)}', ''])
    ids = [a['alert_id'] for a in all_alerts]
    delays = [(utc_time(a['received_time_utc']) - utc_time(a['event_time_utc'])).total_seconds() for a in eligible]
    missing_limits = sum(a['alert_type'] == 'speeding' and not a['posted_limit_kmh'] for a in eligible)
    counts = Counter(a['alert_type'] for a in eligible)
    out += ['## Export checks',
            f'- {len(all_alerts)} raw alerts ({len(raw)} original + {len(added)} backfill); {len(eligible)} at or before the selected event/receipt cutoff; {len(vehicles)} vehicles; {len(orders)} work orders.',
            f'- Unique alert IDs: {len(set(ids))}; repeated IDs: {len(ids)-len(set(ids))}. This does not rule out repeated underlying events.',
            f'- Engine-fault alerts: {counts["engine_fault"]}; speeding alerts: {counts["speeding"]}; speeding alerts without posted limit: {missing_limits}.',
            f'- Alerts received >24 hours after event: {sum(d > 86400 for d in delays)}; negative delivery delays: {sum(d < 0 for d in delays)}.',
            '- Event time and received time are separate; displayed in Toronto local time. Work-order times are already local.',
            '- Hamilton gateway outage contradicts vendor connectivity notes; late receipt does not make the underlying event new.',
            '', '## Ranking and limitations',
            '- P1: critical reference DTC with no documented resolution after its latest event; P2: high-reference fault requiring prompt inspection or a combined unresolved concern.',
            '- This intentionally outputs three selected cases, not ten manufactured tasks. It is not a complete fleet-wide triage engine.',
            '- Repeated alerts are grouped by vehicle in this report; distinct fault codes and their timestamps remain visible.',
            '- Vendor severity is retained as evidence, not treated as authoritative for DTC urgency.',
            '- A work order closing does not prove a different subsequent fault is resolved.',
            '- Missing speed limits, firmware-dependent harsh-event sensitivity and delayed receipt make naive driver ranking unreliable.',
            '- Nightly device interruptions may be expected according to vendor notes; they are not investigated in this minimal report.',
            '- This report recommends human review; it does not certify mechanical safety or dispatch clearance.',
            '']
    if include_backfill:
        out += ['', '## What changed after the new information',
                '- Hamilton Depot gateway reconnected at 6:47 p.m. EDT and delivered 10 alerts; these were not visible at the original 6:00 p.m. cutoff.',
                '- V-108 becomes first priority: A-120811 P0217 at 12:05 p.m. EDT (received 6:47 p.m.), and A-707191 P0524 at 3:41 p.m. EDT (received 6:47 p.m.). Both are critical despite vendor MEDIUM.',
                '- WO-5512 closed September 9 for P0171; it does not resolve the new P0217/P0524 faults.',
                '- V-151 remains a known follow-up (A-668410 misfire and A-927832 2,350 km overdue), but moves below the top three, not cleared.',
                '- The remaining eight backfill records are retained and inspectable in the source explorer; this minimal report does not certify them as harmless.',
                '']
    return '\n'.join(out), eligible


if __name__ == '__main__':
    import sys
    include_backfill = '--backfill' in sys.argv
    report, eligible = build(include_backfill=include_backfill)
    target = ROOT / ('BACKFILL_REPORT.md' if include_backfill else 'DISPATCH_REPORT.md')
    target.write_text(report, encoding='utf-8')
    print(f'Generated {target.name} from {len(eligible)} eligible alerts.')
