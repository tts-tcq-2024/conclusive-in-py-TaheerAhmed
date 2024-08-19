import unittest
from typewise_alert import typewise_alert

class TypewiseTest(unittest.TestCase):
    def test_infers_breach_as_per_limits(self):
        self.assertTrue(typewise_alert.infer_breach(20, 50, 100) == 'TOO_LOW')

    def test_infer_breach_too_high(self):
        self.assertEqual(typewise_alert.infer_breach(120, 50, 100), 'TOO_HIGH')

    def test_infer_breach_normal(self):
        self.assertEqual(typewise_alert.infer_breach(70, 50, 100), 'NORMAL')

    def test_passive_cooling_breach(self):
        cooling = typewise_alert.PassiveCooling()
        self.assertEqual(cooling.classify_breach(40), 'TOO_HIGH')
        self.assertEqual(cooling.classify_breach(30), 'NORMAL')

    def test_hi_active_cooling_breach(self):
        cooling = typewise_alert.HiActiveCooling()
        self.assertEqual(cooling.classify_breach(50), 'TOO_HIGH')
        self.assertEqual(cooling.classify_breach(40), 'NORMAL')

    def test_med_active_cooling_breach(self):
        cooling = typewise_alert.MedActiveCooling()
        self.assertEqual(cooling.classify_breach(45), 'TOO_HIGH')
        self.assertEqual(cooling.classify_breach(35), 'NORMAL')

    def test_controller_alert(self):
        alert = typewise_alert.ControllerAlert()
        self.assertEqual(alert.send_alert('TOO_HIGH'), 'Controller Alert: TOO_HIGH')

    def test_email_alert(self):
        alert = typewise_alert.EmailAlert()
        self.assertEqual(alert.send_alert('TOO_HIGH'), 'To: a.b@c.com\nHi, the temperature is too high')
        self.assertEqual(alert.send_alert('TOO_LOW'), 'To: a.b@c.com\nHi, the temperature is too low')
        self.assertEqual(alert.send_alert('NORMAL'), 'No action needed')

    def test_check_and_alert(self):
        # Test with HiActiveCooling and ControllerAlert
        result = typewise_alert.check_and_alert(typewise_alert.ControllerAlert(), typewise_alert.HiActiveCooling(), 50)
        self.assertEqual(result, 'Controller Alert: TOO_HIGH')

        # Test with PassiveCooling and EmailAlert
        result = typewise_alert.check_and_alert(typewise_alert.EmailAlert(), typewise_alert.PassiveCooling(), 30)
        self.assertEqual(result, 'No action needed')

        # Test with MedActiveCooling and EmailAlert
        result = typewise_alert.check_and_alert(typewise_alert.EmailAlert(), typewise_alert.MedActiveCooling(), 45)
        self.assertEqual(result, 'To: a.b@c.com\nHi, the temperature is too high')

if __name__ == '__main__':
    unittest.main()
