import locale, sys

locale.setlocale(locale.LC_ALL, '')

inflation_rate = 1.0 + 1.8/100;

def currency(val):
	return locale.currency(val, grouping=True)

def inflation_multiplier(year):
	return inflation_rate ** (year - 2016) # all numbers are based off of amounts in 2016

def get_split(bear, cat):
	try:
		return bear / (bear + cat)
	except:
		return 0

def split_amount(amount, split):
	return (amount * split, amount * (1.0-split))


class Project(object):
	def get_name(self):
		return self.__class__.__name__

	def get_description(self, year):
		raise Exception("Not implemented")

	def calc_amount(self, year):
		raise Exception("Not implemented")

	def get_amount(self, year, split):
		return split_amount(self.calc_amount(year), split)

class OneTimeProject(Project):
	def __init__(self, start_year):
		self.start_year = start_year
		super(OneTimeProject, self).__init__()

	def get_description(self, year):
		return 'Total cost'

class RecurringProject(Project):
	def __init__(self, start_year, end_year):
		self.start_year = start_year
		self.end_year = end_year
		super(RecurringProject, self).__init__()

	def get_description(self, year):
		return 'Year %s'%(year - self.start_year)


class BearCareer(RecurringProject):
	def calc_amount(self, year):
		rel_year = year - self.start_year
		amount = +180000 * 0.64 # income tax based on tax brackets today
		if rel_year < 0:
			return 0
		if year >= self.end_year:
			return 0
		if year == 2016:
			amount = ((5.0/12)*180000 + (7.0/12)*65000) * 0.64
		return amount * inflation_multiplier(year)

	def get_amount(self, year, split):
		return super(BearCareer, self).get_amount(year, 1)

class CatCareer(RecurringProject):
	def calc_amount(self, year):
		rel_year = year - self.start_year
		amount = +105000 * 0.66 # income tax based on tax brackets today
		if rel_year < 0:
			return 0
		if year >= self.end_year:
			return 0
		if year == 2016:
			amount = ((6.0/12)*105000 + (6.0/12)*75000) * 0.66
		return amount * inflation_multiplier(year)

	def get_amount(self, year, split):
		return super(CatCareer, self).get_amount(year, 0)

class LivingExpenses(RecurringProject):
	def calc_amount(self, year):
		rel_year = year - self.start_year
		amount = -2000*12
		if rel_year < 0:
			return 0
		if year >= self.end_year:
			return 0
		return amount * inflation_multiplier(year)

class Vacation(RecurringProject):
	def calc_amount(self, year):
		rel_year = year - self.start_year
		amount = -6000
		if rel_year < 0:
			return 0
		if year >= self.end_year:
			return 0
		return amount * inflation_multiplier(year)
	
	def get_amount(self, year, split):
		return super(Vacation, self).get_amount(year, 0.5)

class Gifts(RecurringProject):
	def calc_amount(self, year):
		rel_year = year - self.start_year
		amount = -6000
		if rel_year < 0:
			return 0
		if year >= self.end_year:
			return 0
		return amount * inflation_multiplier(year)

	def get_amount(self, year, split):
		return super(Gifts, self).get_amount(year, 0.5)

class Engagement(OneTimeProject):
	def calc_amount(self, year):
		rel_year = year - self.start_year
		amount = -73000
		if rel_year != 0:
			return 0
		return amount * inflation_multiplier(year)

	def get_amount(self, year, split):
		return super(Engagement, self).get_amount(year, 1)

class Marriage(OneTimeProject):
	def calc_amount(self, year):
		rel_year = year - self.start_year
		amount = -70000
		if rel_year != 0:
			return 0
		return amount * inflation_multiplier(year)

class CurrentRent(RecurringProject):
	def calc_amount(self, year):
		if year < self.start_year or year > self.end_year:
			return 0
		elif year > self.end_year:
			return 0
		else:
			amount = -1950 * (1.09 ** (year - 2016)) * 12
		return amount * inflation_multiplier(year)

class PetFriendlyRent(RecurringProject):
	def calc_amount(self, year):
		if year < self.start_year or year > self.end_year:
			return 0
		elif year > self.end_year:
			return 0
		else:
			amount = -2900 * (1.09 ** (year - 2016)) * 12
		return amount * inflation_multiplier(year)

class Shiba(RecurringProject):
	def calc_amount(self, year):
		rel_year = year - self.start_year
		amount = 0
		if year < self.start_year or year > self.end_year:
			return 0
		elif rel_year > 15: # expected 15 year life
			return 0
		else:
			amount = -150 * 12

		if rel_year == 0: # purchase
			amount += -2500

		return amount * inflation_multiplier(year)

	def get_amount(self, year, split):
		return super(Shiba, self).get_amount(year, 0.5)

class Apartment(RecurringProject):
	def calc_amount(self, year):
		rel_year = year - self.start_year
		amount = 0
		if year < self.start_year or year > self.end_year:
			return 0
		elif rel_year >= 30: # 30 year mortgage
			amount = -1500 * 12
		else:
			amount = -6000 * 12

		if rel_year == 0: # downpayment
			amount += -120000

		return amount * inflation_multiplier(year)

class House(RecurringProject):
	def calc_amount(self, year):
		rel_year = year - self.start_year
		amount = 0
		if year < self.start_year or year > self.end_year:
			return 0
		elif rel_year >= 30: # 30 year mortgage
			amount = -3000 * 12
		else:
			amount = -18000 * 12

		if rel_year == 0: # downpayment
			amount += -500000

		return amount * inflation_multiplier(year)

class FirstChild(RecurringProject):
	def get_description(self, year):
		return 'Year %s'%(year - self.start_year)

	def calc_amount(self, year):
		rel_year = year - self.start_year
		amount = 0
		if rel_year < 0:
			return 0
		elif rel_year < 8:
			amount = -20000
		elif rel_year < 12:
			amount = -24000
		elif rel_year < 18:
			amount = -48000 # private school
		elif rel_year < 23:
			amount = -60000 # college
		else:
			amount = -2000
		return amount * inflation_multiplier(year)

class SecondChild(RecurringProject):
	def get_description(self, year):
		return 'Year %s'%(year - self.start_year)

	def calc_amount(self, year):
		rel_year = year - self.start_year
		amount = 0
		if rel_year < 0:
			return 0
		elif rel_year < 8:
			amount = -20000
		elif rel_year < 12:
			amount = -22000
		elif rel_year < 18:
			amount = -44000 # private school
		elif rel_year < 23:
			amount = -60000 # college
		else:
			amount = -2000
		return amount * inflation_multiplier(year)


projects = 	[	# income
				BearCareer(2016, 2059),

				#CatCareer(2016, 2059),

				CatCareer(2016, 2021),
				# materinity leave
				CatCareer(2026, 2059),				

				# recurring expenses
				LivingExpenses(2016, 3000),
				Vacation(2016, 3000),
				Gifts(2016, 3000),
				PetFriendlyRent(2016, 2028),
				Shiba(2017, 2032),
				# CurrentRent(2016, 2028),

				# upcoming projects
				Engagement(2017),
				Marriage(2018),
				
				FirstChild(2022, -1),
				SecondChild(2024, -1),

				# House(2029, 2029+30),
				Apartment(2029, 2029+30),

				# retirement? 4% rule means you'll need to have saved up 4M in today's dollars for 100k each year

			]


detail = 2020
plan_success = True
bear_bank = 0
cat_bank = 0

print '*'*80

for year in xrange(2016, 2055):
	if year <= detail:
		print 'Year:', year, '( Age', year-1989, ')'
	year_income_bear = 0
	year_expense_bear = 0
	year_income_cat = 0
	year_expense_cat = 0
	for p in projects:
		split = get_split(year_income_bear, year_income_cat)
		p_amount_bear, p_amount_cat = p.get_amount(year, split)
		if p_amount_bear >= 0:
			year_income_bear += p_amount_bear
		else:
			year_expense_bear += p_amount_bear
		if p_amount_cat >= 0:
			year_income_cat += p_amount_cat
		else:
			year_expense_cat += p_amount_cat
		if year <= detail:
			if (p_amount_bear, p_amount_cat) != (0, 0):
				print '\t', currency(p_amount_bear + p_amount_cat), ':', currency(p_amount_bear), '/', currency(p_amount_cat), '-', p.get_name(), '-', p.get_description(year)
	bear_bank += year_income_bear + year_expense_bear
	cat_bank += year_income_cat + year_expense_cat
	if bear_bank <= 0 or cat_bank <= 0:
		plan_success = False
		print '####### FAIL %s ########'%year
	if year <= detail or plan_success == False:
		print 'Bear Bank:', currency(bear_bank)
		print '\tBear Income:', currency(year_income_bear)
		print '\tBear Expense:', currency(year_expense_bear)
		print '\tBear Net:', currency(year_income_bear + year_expense_bear)
		print 'Cat Bank:', currency(cat_bank)
		print '\tCat Income:', currency(year_income_cat)
		print '\tCat Expense:', currency(year_expense_cat)
		print '\tCat Net:', currency(year_income_cat + year_expense_cat)
		print '-------'
		if plan_success == False:
			sys.exit(0)

print '********'
print 'Congrats. You will each retire on a salary of', currency((bear_bank + cat_bank) / inflation_multiplier(year) / 25 / 2), "(2016's dollars)"
print '********'
