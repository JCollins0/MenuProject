import requests
from html.parser import HTMLParser
import pprint as PP
import datetime as Date
import foodjson

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

class MyHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.found_data = False
        self.found_cat = False
        self.found_meal = False
        self.found_instruct=False
        self.currmeal = ''
        self.currcat = ''
        self.map = {}
        self.skip = False

    def handle_starttag(self, tag, attrs):
        #print("Start tag:", tag)
        for attr in attrs:
            if(attr[0] == 'class' and attr[1] == 'menusamprecipes'):
                self.found_data = True
            if(attr[0] == 'class' and attr[1] == 'menusampcats'):
                self.found_cat = True
            if(attr[0] == 'class' and attr[1] == 'menusampmeals'):
                self.found_meal = True
            if(attr[0] == 'class' and attr[1] == 'menusampinstructs'):
                self.found_instruct = True


    def handle_data(self, data):
        if(self.skip==False):
            if(self.found_data):
                # only match specified meal
                if(self.meal_time == self.currmeal):
                    #print("Data     :", data)
                    if(self.map.get(self.currcat) == None):
                        self.map[self.currcat] = []
                    self.map[self.currcat].append(data)
                    self.found_data = False
            if(self.found_cat):
                self.found_cat = False
                self.currcat = data
            if(self.found_meal):
                self.found_meal=False
                self.currmeal = data
            if(self.found_instruct):
                self.found_instruct = False
                if data.strip() == 'No Data Available':
                    self.skip = True

def read_html(date_arg,loc_arg,meal_time='Lunch'):
    url = get_url(date_arg,loc_arg)
    r = requests.get(url)

    #print(r.status_code)
    if(r.status_code == 200):
        html = r.text

    parser = MyHTMLParser()
    parser.meal_time = meal_time
    parser.feed(html)

    foodjson.write_json(parser.map)
    return parser.map

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
    map = read_html('-'.join((year,month,day)),location,'Lunch')
    print()


    i = 0
    for line in map.keys():
        print("{0}) {1}".format(i,line))
        i=i+1
    print()
    lineIndex = input("Enter the number(s) of the line you want sep. by spaces: ")
    lineIndex = lineIndex.split(" ")
    print()
    for num in lineIndex:
        PP.pprint(map[list(map.keys())[int(num)]])
        print("")


if __name__ == '__main__':
    command_line()
