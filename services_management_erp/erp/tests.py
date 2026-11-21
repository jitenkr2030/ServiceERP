from decimal import Decimal
from django.test import TestCase
from .calculations import billable_amount,labour_cost,gross_profit,net_profit,margin_percent,outstanding,utilization,monthly_equivalent
class FinancialCalculationTests(TestCase):
 def test_billable_and_cost(self):
  self.assertEqual(billable_amount('2.5','800'),Decimal('2000.0'))
  self.assertEqual(labour_cost('2','300'),Decimal('600'))
 def test_profit_and_margin(self):
  self.assertEqual(gross_profit(1000,400),Decimal('600'))
  self.assertEqual(net_profit(1000,400,100),Decimal('500'))
  self.assertEqual(margin_percent(250,1000),Decimal('25.00'))
 def test_receivables_and_utilization(self):
  self.assertEqual(outstanding(1000,300,100),Decimal('600'))
  self.assertEqual(utilization(30,120),Decimal('25'))
  self.assertEqual(monthly_equivalent(12000,'annual'),Decimal('1000'))
