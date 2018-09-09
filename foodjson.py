import json
import io

def write_json(dictionary={}):
    file_path = 'food.json'
    list = []
    try:
        f = open(file_path,'r')
        list = json.loads(f.read())

    except Exception as e:
        pass


    for key in dictionary:
        for val in dictionary[key]:
            if(val not in list and val.strip() != ""):
                list.append(val)

    try:
        f.close()
    except Exception as e:
        pass

    f = open(file_path,"w")
    f.write(json.dumps(sorted(list)))
    f.close()

def get_food_list():
    list = []
    try:
        f = open('food.json','r')
        list = json.loads(f.read())
        f.close()
    except:
        pass
    return list
