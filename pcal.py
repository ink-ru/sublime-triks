# coding: utf-8

'''Производственный календарь'''


#http://data.gov.ru/opendata/7708660670-proizvcalendar
calendar =  {
'2016' : [
[1,2,3,4,5,6,7,8,9,10,16,17,23,24,30,31],
[6,7,13,14,21,22,23,27,28],
[5,6,7,8,12,13,19,20,26,27],
[2,3,9,10,16,17,23,24,30],
[1,2,3,7,8,9,14,15,21,22,28,29],
[4,5,11,12,13,18,19,25,26],
[2,3,9,10,16,17,23,24,30,31],
[6,7,13,14,20,21,27,28],
[3,4,10,11,17,18,24,25],
[1,2,8,9,15,16,22,23,29,30],
[4,5,6,12,13,19,20,26,27],
[3,4,10,11,17,18,24,25,31]
],
'2017' : [
[1,2,3,4,5,6,7,8,9,14,15,21,22,28,29],
[4,5,11,12,18,19,23,25,26],
[4,5,8,11,12,18,19,25,26],
[1,2,8,9,15,16,22,23,29,30],
[1,6,7,8,9,13,14,20,21,27,28],
[3,4,10,11,12,17,18,24,25],
[1,2,8,9,15,16,22,23,29,30],
[5,6,12,13,19,20,26,27],
[2,3,9,10,16,17,23,24,30],
[1,7,8,14,15,21,22,28,29],
[4,5,6,11,12,18,19,25,26],
[2,3,9,10,16,17,23,24,30,31]
],
'2018' : [
[1,2,3,4,5,6,7,8,9,10,13,14,20,21,27,28],
[3,4,10,11,17,18,23,24,25],
[3,4,8,10,11,17,18,24,25,31],
[1,7,8,14,15,21,22,28,29],
[1,5,6,9,12,13,19,20,26,27],
[2,3,9,10,12,16,17,23,24,30],
[1,7,8,14,15,21,22,28,29],
[4,5,11,12,18,19,25,26],
[1,2,8,9,15,16,22,23,29,30],
[6,7,13,14,20,21,27,28],
[3,4,5,10,11,17,18,24,25],
[1,2,8,9,15,16,22,23,29,30]
],
'2019' : [
[1,2,3,4,5,6,7,8,9,10,12,13,19,20,26,27],
[2,3,9,10,16,17,23,24,25],
[2,3,8,9,10,16,17,23,24,30,31],
[6,7,13,14,20,21,27,28],
[4,5,9,11,12,18,19,25,26],
[1,2,8,9,12,15,16,22,23,29,30],
[6,7,13,14,20,21,27,28],
[3,4,10,11,17,18,24,25,31],
[1,7,8,14,15,21,22,28,29],
[5,6,12,13,19,20,26,27],
[2,3,9,10,16,17,23,24,30],
[1,7,8,14,15,21,22,28,29]
]
}

def today_is_working():
	return False
