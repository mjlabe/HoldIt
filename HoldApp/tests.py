from django.test import TestCase
from .models import Report


# Create your tests here.
class CreateReport(TestCase):
    def setUp(self):
        Report.objects.create(title="testtitle", summary="testSummary")

    def test_stuff(self):
        r1 = Report.objects.get(title="testtitle")
        r2 = Report.objects.get(summary="testSummary")

        self.assertEqual(r1.title, "testtitle")
        self.assertEqual(r2.summary, "testSummary")
