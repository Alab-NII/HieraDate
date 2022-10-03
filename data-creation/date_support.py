import re
from datetime import datetime
from dateutil import relativedelta
import copy


def normalize_date(date_):
	new_date = {}
	if date_['day'] > 31:
		new_date['day'] = date_['day']%30
		date_['month'] = date_['month'] + int(date_['day']/30)
	else:
		new_date['day'] = date_['day']
	if date_['month'] > 12:
		new_date['month'] = date_['month']%12
		new_date['year'] = date_['year'] + int(date_['month']/12)
	else:
		new_date['month'] = date_['month']
		new_date['year'] = date_['year']
	return new_date


def convert_date2str(date_input):
	"""
		input:
		{'year': 1799, 'month': 12, 'day': 14, 'hour': 0, 'minute': 0, 'second': 0}
		output:
		list of str values:
		December 14, 1799
		14 December 1799
	"""
	month_dict = { 1 : "January",
       2 : "February",
       3 : "March",
       4 : "April",
       5 : "May",
       6 : "June",
       7 : "July",
       8 : "August",
       9 : "September",
       10 : "October",
       11 : "November",
       12 : "December"
	}
	results = []
	date_ = normalize_date(date_input)
	# print(date_)
	if date_['month'] != 0 and date_['day'] != 0 and date_['year'] != 0:
		year = int(re.sub("\D", "", str(date_['year'])))
		month = int(re.sub("\D", "", str(date_['month'])))
		day = int(re.sub("\D", "", str(date_['day'])))
		#
		try: 
			new_dict = datetime(year, month, day)
			str_1 = new_dict.strftime("%B %d, %Y") # 'June 08, 1930'
			str_2 = new_dict.strftime("%d %B %Y") # '08 June 1930'
			# 
			str_3 = new_dict.strftime("%B%e, %Y") # 'June 8, 1930'
			str_4 = new_dict.strftime("%e %B %Y").strip() # '8 June 1930'
			str_5 = new_dict.strftime("%e %B, %Y").strip() # '8 June, 1930'
			str_6 = new_dict.strftime("%B %e, %Y") # 'June 8, 1930'
			results.append(str_1)
			results.append(str_2)
			results.append(str_3)
			results.append(str_4)
			results.append(str_5)
			results.append(str_6)
		except ValueError:
			results.append(str(date_['year']))
	#
	elif date_['month'] != 0 and date_['year'] != 0:
		year = int(re.sub("\D", "", str(date_['year'])))
		month = int(re.sub("\D", "", str(date_['month'])))
		str_month = month_dict[month]
		str_1 = str_month + ' ' + str(year)
		str_2 = str_month + ', ' + str(year)
		#
		results.append(str_1)
		results.append(str_2)
	else:
		results.append(str(date_['year']))
	return results


# we can use it when the month or date is 0
def subtract_two_dates_old(dict_1, dict_2):
	"""
		Return a dictionary date
	"""
	dic_ = {}
	# day
	if dict_2['day'] > dict_1['day']:
		dic_['day'] = dict_2['day'] - dict_1['day']
	else:
		dict_2['day'] = dict_2['day'] + 30
		dict_2['month'] = dict_2['month'] - 1
		dic_['day'] = dict_2['day'] - dict_1['day']
	# month
	if dict_2['month'] > dict_1['month']:
		dic_['month'] = dict_2['month'] - dict_1['month']
	else:
		dict_2['month'] = dict_2['month'] + 12
		dict_2['year'] = dict_2['year'] - 1
		dic_['month'] = dict_2['month'] - dict_1['month']
	# year
	dic_['year'] = dict_2['year'] - dict_1['year']
	return dic_


def subtract_two_dates(dict_1_input, dict_2_input):
	"""
		Return a dictionary date
	"""
	dict_1 = copy.deepcopy(dict_1_input)
	dict_2 = copy.deepcopy(dict_2_input)
	if 	dict_1['month'] == 0 or dict_1['day'] == 0 or dict_2['month'] == 0 or dict_2['day'] == 0:
		return subtract_two_dates_old(dict_1, dict_2)
	else: 
		dic_ = {}
		date_1 = datetime(dict_1['year'], dict_1['month'], dict_1['day'])
		date_2 = datetime(dict_2['year'], dict_2['month'], dict_2['day'])
		diff = relativedelta.relativedelta(date_2, date_1)
		#
		dic_['year'] = diff.years
		dic_['month'] = diff.months
		dic_['day'] = diff.days
		return dic_


def compare_two_dates(dict_1, dict_2):
	"""
		Return 1 if dict_1 < dict_2
	"""
	# Return 0 when there are something wrong with the date
	if (dict_1['year'] == 0 and dict_1['month'] == 0 \
		and dict_1['day'] == 0) or (dict_2['year'] == 0 and dict_2['month'] == 0 and dict_2['day'] == 0):
		return 0
	# # 
	if dict_1['year'] < dict_2['year']:
		return 1
	elif dict_1['year'] > dict_2['year']:
		return -1
	elif dict_1['year'] == dict_2['year']:
		if dict_1['month'] < dict_2['month']:
			return 1
		elif dict_1['month'] > dict_2['month']:
			return -1
		elif dict_1['month'] == dict_2['month']:
			if dict_1['day'] < dict_2['day']:
				return 1
			elif dict_1['day'] > dict_2['day']:
				return -1
			elif dict_1['day'] == dict_2['day']:
				return 2