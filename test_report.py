import unittest
from report import build, rows, utc_time, REFERENCE

class ReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report, cls.eligible = build()

    def test_fixed_cutoff(self):
        self.assertTrue(all(utc_time(a['event_time_utc']) <= REFERENCE and utc_time(a['received_time_utc']) <= REFERENCE for a in self.eligible))

    def test_critical_after_repair(self):
        a = next(a for a in self.eligible if a['alert_id'] == 'A-784686')
        self.assertEqual((a['vehicle_id'], a['dtc_code'], a['vendor_severity']), ('V-137', 'P0524', 'MEDIUM'))
        self.assertIn('WO-5540', self.report)

    def test_v151_misfire_not_missed(self):
        self.assertIn('A-668410', self.report)
        self.assertIn('A-927832', self.report)

    def test_v158_open_order(self):
        self.assertIn('A-468820', self.report)
        self.assertIn('WO-5543 (Open', self.report)

    def test_three_action_cards(self):
        self.assertEqual(self.report.count('### '), 3)

    def test_backfill_changes_top_priority(self):
        updated, eligible = build(include_backfill=True)
        self.assertEqual(len(eligible), 2380)
        self.assertIn('### 1. V-108', updated)
        self.assertIn('A-120811', updated)
        self.assertIn('A-707191', updated)
        self.assertIn('WO-5512', updated)
        self.assertNotIn('### 1. V-108', self.report)

    def test_source_count(self):
        self.assertEqual(len(rows('alerts.csv')), 2370)

if __name__ == '__main__':
    unittest.main()
