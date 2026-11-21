from decimal import Decimal

def billable_amount(hours, rate): return Decimal(str(hours))*Decimal(str(rate))
def labour_cost(hours, cost_rate): return Decimal(str(hours))*Decimal(str(cost_rate))
def gross_profit(revenue, direct_costs): return Decimal(str(revenue))-Decimal(str(direct_costs))
def net_profit(revenue, direct_costs, overhead): return Decimal(str(revenue))-Decimal(str(direct_costs))-Decimal(str(overhead))
def margin_percent(profit, revenue):
 revenue=Decimal(str(revenue))
 return (Decimal(str(profit))/revenue*100) if revenue else Decimal('0')
def outstanding(total, allocated, credits=0): return Decimal(str(total))-Decimal(str(allocated))-Decimal(str(credits))
def utilization(billable_hours, available_hours):
 available=Decimal(str(available_hours))
 return Decimal(str(billable_hours))/available*100 if available else Decimal('0')
def monthly_equivalent(value, frequency):
 months={'monthly':1,'quarterly':3,'half_yearly':6,'annual':12,'yearly':12}
 return Decimal(str(value))/months.get(frequency,1)
