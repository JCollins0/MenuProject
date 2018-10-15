from menu_parser import read_html
from datetime import datetime, timedelta
import pprint as PP
import threading
import time

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
    t_list = []
    start = time.time()
    # TODO: Make this faster
    for date in list:
        try:
            thread_1 = threading.Thread(target=get_items_for_location_lunch, args=(food_item, date, J2, j2date_list['Lunch']))
            thread_2 = threading.Thread(target=get_items_for_location_dinner, args=(food_item, date, J2, j2date_list['Dinner']))
            thread_3 = threading.Thread(target=get_items_for_location_lunch, args=(food_item, date, Kinsolving, kinsdate_list['Lunch']))
            thread_4 = threading.Thread(target=get_items_for_location_dinner, args=(food_item, date, Kinsolving, kinsdate_list['Dinner']))
            thread_5 = threading.Thread(target=get_items_for_location_lunch, args=(food_item, date, FastLine, fastline_list['Lunch']))
            thread_6 = threading.Thread(target=get_items_for_location_dinner, args=(food_item, date, FastLine, fastline_list['Dinner']))
            t_list.append(thread_1)
            t_list.append(thread_2)
            t_list.append(thread_3)
            t_list.append(thread_4)
            t_list.append(thread_5)
            t_list.append(thread_6)
            thread_1.start()
            thread_2.start()
            thread_3.start()
            thread_4.start()
            thread_5.start()
            thread_6.start()
        except:
            print("Error: unable to start thread")
        # get_items_for_location_lunch(food_item, date, J2, j2date_list['Lunch'])
        # get_items_for_location_dinner(food_item, date, J2, j2date_list['Dinner'])
        # get_items_for_location_lunch(food_item, date, Kinsolving, kinsdate_list['Lunch'])
        # get_items_for_location_dinner(food_item,date, Kinsolving, kinsdate_list['Dinner'])
        # get_items_for_location_lunch(food_item,date, FastLine, fastline_list['Lunch'])
        # get_items_for_location_dinner(food_item,date, FastLine, fastline_list['Dinner'])
        for thread in t_list:
            thread.join()
    end = time.time()
    print(end-start)
    ret_map = {}
    ret_map.update(J2=j2date_list)
    ret_map.update(Kinsolving=kinsdate_list)
    ret_map.update(FastLine=fastline_list)
    return ret_map

# TODO: REMOVE THE NEED FOR THESE FUNCTIONS
def get_items_for_location_lunch(food_item, date, loc, out_list):
    return get_items_for_location(food_item,date,loc,'Lunch',out_list)

def get_items_for_location_dinner(food_item, date, loc, out_list):
    return get_items_for_location(food_item,date,loc,'Dinner',out_list)

def get_items_for_location(food_item, date, loc, meal_time, out_list):
    date_map = {}
    ld_dictionary = read_html(date_arg=date,loc_arg=loc) #for lunch
    # print(date, loc)
    # PP.pprint(ld_dictionary)
    dictionary = ld_dictionary[meal_time]
    for key in dictionary:
        if food_item in dictionary[key]:
            if(date_map.get(key) == None):
                date_map[key] = []
            date_map[key].append(date)
            # print("Found it")
    if(len(date_map) > 0):
        out_list.append(date_map)

if __name__ == '__main__':
    print(find_day_for_food("Chicken Noodle Soup"))
