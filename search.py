from menu_parser import read_html
from datetime import datetime, timedelta

def find_day_for_food(food_item):
    # constants
    J2= 'Jester+2nd+Floor+Dining'
    j2location = '12'
    Kinsolving = 'Kinsolving+Dining+Hall'
    kinslocation = '03'
    FastLine='J2+FAST+Line'
    fastloc = '27'

    day = (datetime.today().strftime('%d/%m/%Y'))
    dt = datetime.strptime(day, '%d/%m/%Y')
    dayIndex = dt.weekday()
    start = dt - timedelta(days=( (dayIndex%5 ) +2 * ( 1 if dayIndex<5 else 0 )))
    end = start + timedelta(days=6)
    # print(start.strftime('%d/%m/%Y'))
    # print(end.strftime('%d/%m/%Y'))
    list = []
    for d in range(0,7):
        list.append((start + timedelta(days=d)).strftime('%Y-%m-%d'))

    j2date_list = {'Lunch':[], 'Dinner':[]}
    kinsdate_list ={'Lunch':[], 'Dinner':[]}
    fastline_list = {'Lunch':[], 'Dinner':[]}
    # for each date get the web data and if food item is contained in there, return date, location
    for date in list:
        dat = get_items_for_location_lunch(food_item, date, J2)
        if len(dat) != 0:
            j2date_list['Lunch'].append(dat)
        dat = get_items_for_location_dinner(food_item, date, J2)
        if len(dat) != 0:
            j2date_list['Dinner'].append(dat)
        dat = get_items_for_location_lunch(food_item, date, Kinsolving)
        if len(dat) != 0:
            kinsdate_list['Lunch'].append(dat)
        dat = get_items_for_location_dinner(food_item,date, Kinsolving)
        if len(dat) != 0:
            kinsdate_list['Dinner'].append(dat)
        dat = get_items_for_location_lunch(food_item,date, FastLine)
        if len(dat) != 0:
            fastline_list['Lunch'].append(dat)
        dat = get_items_for_location_dinner(food_item,date, FastLine)
        if len(dat) != 0:
            fastline_list['Dinner'].append(dat)

    ret_map = {}
    ret_map.update(J2=j2date_list)
    ret_map.update(Kinsolving=kinsdate_list)
    ret_map.update(FastLine=fastline_list)
    return ret_map


def get_items_for_location_lunch(food_item, date, loc):
    date_map = {}
    dictionary = read_html(date_arg=date,loc_arg=loc, meal_time='Lunch') #for lunch
    for key in dictionary:
        if food_item in dictionary[key]:
            if(date_map.get(key) == None):
                date_map[key] = []
            date_map[key].append(date)
            # print("Found it")

    return date_map

def get_items_for_location_dinner(food_item, date, loc):
    date_map = {}
    dictionary = read_html(date_arg=date,loc_arg=loc, meal_time='Dinner') #for lunch
    for key in dictionary:
        if food_item in dictionary[key]:
            if(date_map.get(key) == None):
                date_map[key] = []
            date_map[key].append(date)
            # print("Found it")

    return date_map
