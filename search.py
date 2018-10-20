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
    for date in list:
        try:
            thread_1 = threading.Thread(target=get_items_for_location, args=(food_item, date, J2, j2date_list))
            thread_2 = threading.Thread(target=get_items_for_location, args=(food_item, date, Kinsolving, kinsdate_list))
            thread_3 = threading.Thread(target=get_items_for_location, args=(food_item, date, FastLine, fastline_list))
            t_list.append(thread_1)
            t_list.append(thread_2)
            t_list.append(thread_3)
            thread_1.start()
            thread_2.start()
            thread_3.start()
        except:
            print("Error: unable to start thread")
        for thread in t_list:
            thread.join()
    end = time.time()
    print(end-start)
    ret_map = {}
    ret_map.update(J2=j2date_list)
    ret_map.update(Kinsolving=kinsdate_list)
    ret_map.update(FastLine=fastline_list)
    return ret_map


def get_items_for_location(food_item, date, loc, out_map):
    date_map = {}
    ld_dictionary = read_html(date_arg=date,loc_arg=loc)
    # print(date, loc)
    # PP.pprint(ld_dictionary)
    for meal_time in out_map:
        dictionary = ld_dictionary[meal_time]
        for key in dictionary:
            if food_item in dictionary[key]:
                if(date_map.get(key) == None):
                    date_map[key] = []
                date_map[key].append(date)
                # print("Found it")
        if(len(date_map) > 0):
            out_map[meal_time].append(date_map)

if __name__ == '__main__':
    print(find_day_for_food("Chicken Noodle Soup"))
