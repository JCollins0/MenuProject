import requests
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import pprint as PP
import datetime as Date
import foodjson
import re

def get_url(date_arg,loc_arg):

    # constants
    J2= 'Jester+2nd+Floor+Dining'
    j2location = '12'
    Kinsolving = 'Kinsolving+Dining+Hall'
    kinslocation = '03'
    FastLine='J2+FAST+Line'
    fastloc = '27'

    (year, month, day) = date_arg.split('-')
    location = loc_arg.replace(' ','+')
    # url vars
    action = 'myaction=read'
    name = 'sName=The+University+of+Texas+at+Austin+-+Housing+and+Dining'
    date = 'dtdate=' + '%2f'.join((month,day,year))

    if(location == J2):
        locNum = j2location
        locName = J2
    elif(location == Kinsolving):
        locNum = kinslocation
        locName = Kinsolving
    elif(location == FastLine):
        locNum = fastloc
        locName = FastLine

    locationNum ='locationNum=' + locNum
    locationName = 'locationName=' + locName
    flags = 'naFlag=1'

    # combine to make url
    vars = '&'.join((action,name,date,locationNum,locationName,flags))
    url = 'http://hf-food.austin.utexas.edu/foodpro/menuSamp2.asp?' + vars
    return url


def read_html(date_arg,loc_arg):
    meal_dict = {'Breakfast':{},'Lunch':{}, 'Dinner':{}}

    url = get_url(date_arg,loc_arg)
    r = requests.get(url)

    #print(r.status_code)
    if(r.status_code == 200):
        soup = BeautifulSoup(r.text, features="html.parser")


        REGEXnl  = re.compile("\r|\n|\xa0")
        REGEXsp = re.compile("(\\s\\s)+")
        REGEXline = re.compile("(-- [A-Za-z0-9\\s&!@#$%^']+ --?)")
        meals = soup.find("div", {"class" : "menusampmeals"})
        if(meals == None):
            return meal_dict
        meals = meals.parent.parent.parent.parent.parent.parent.parent.parent
        # print(meals)
        meals = filter(lambda x : x is not None and x != "\n", meals.children)
        meals = list(meals)
        l = []


        for meal in meals:
            data = re.sub(REGEXnl," ", meal.text.strip())
            data = re.sub(REGEXsp,"  ", data)
            lines = re.split(REGEXline, data)
            line_iter = iter(lines)
            meal_time = next(line_iter).strip()
            meal_dict[meal_time] = dict()

            try:
                while(True):
                    line = next(line_iter)
                    food = next(line_iter)
                    meal_dict[meal_time][line] = []
                    food = filter(lambda x: x.strip() !="", re.split(REGEXsp,food))
                    food = list(map(lambda x : x.strip(), food))
                    for food_item in food:
                        meal_dict[meal_time][line].append(food_item)
            except StopIteration as e:
                pass
    return meal_dict

def command_line():
    J2= 'Jester+2nd+Floor+Dining'
    Kinsolving = 'Kinsolving+Dining+Hall'
    FastLine='J2+FAST+Line'
    locations = [J2.replace('+',' '), Kinsolving.replace('+',' '), FastLine.replace('+',' ')]

    day = '10'

    year = str(Date.date.today().year)
    month = str(Date.date.today().month)

    day = input("Enter the day (number): ")
    print()

    i = 0
    for location in locations:
        print("{0}) {1}".format(i,location))
        i=i+1
    print()
    locIndex = input("Enter the number of the location: ")
    location = locations[int(locIndex)]
    map = read_html('-'.join((year,month,day)),location)

    PP.pprint(map)


if __name__ == '__main__':
    command_line()
