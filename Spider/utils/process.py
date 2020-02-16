import re


def match_keyword(whole_str, *key_str_list):
	result_list = []
	for key_str in key_str_list:
		rule_str = '.*%s.*?small">(.*?)</div>.*'%key_str
		match_re = re.match(rule_str, whole_str, re.S)
		if match_re:
			result_list.append(match_re.group(1))
		else:
			result_list.append("")
	return result_list


def process_date_str(date_str):
	match_re = re.match('(\d+)<sup>.*</sup> (.*?) <span>(\d+)</span>', date_str)
	if match_re:
		day, month, year = match_re.groups()
		return '%s %s %s'%(month, day, year)
	elif date_str.isdigit():
		return date_str
	else:
		return ""


def process_claim_str(claim_str):
	match_re = re.match('<p class="date">(.*) \\| (\d*) Enslaved \\| £(.*?) (.*?)s (.*?)d', claim_str)
	claim_date = process_date_str(match_re.group(1))
	return (claim_date,)+match_re.groups()[1:]


def process_person_date_str(person_date_str):
	match_re = re.match('<p class="date">(.*) - (.*)</p>', person_date_str)
	if match_re:
		birth_date, death_date = process_date_str(match_re.group(1)), process_date_str(match_re.group(2))
		return birth_date, death_date
	else:
		return '', ''


if __name__ == "__main__":
	str1 = '<p class="date">29<sup>th</sup> Oct <span>1838</span> | 1 Enslaved | £5 13s 2d</p>'
	str2 = '<p class="date"><span class="faded">No Date</span> | 32 Enslaved | £1665 17s 9d</p>'

	str3 = '<p class="date">4<sup>th</sup> Nov <span>1775</span> - 1820</p>'
	str4 = '<p class="date">7<sup>th</sup> Dec <span>1775</span> - 29<sup>th</sup> Nov <span>1853</span></p>'
	str5 = '<p class="date">1775 - ????</p>'
	str6 = '<p class="date"><span class="faded">No Dates</span></p>'

	print(process_claim_str(str1))
	print(process_claim_str(str2))
	#print(process_person_date_str(str3))
	#print(process_person_date_str(str4))
	#print(process_person_date_str(str5))
	#print(process_person_date_str(str6))
