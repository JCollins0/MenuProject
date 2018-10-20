from flask import Flask, render_template, request
from menu_parser import read_html
from foodjson import get_food_list
from search import find_day_for_food
import pprint as PP
app = Flask(__name__)

if __name__ == '__main__' :
    app.run(debug=True)

@app.route('/')
def index():
    list = get_food_list()
    return render_template('input.html', foodlist=list)

@app.route('/menu', methods=['POST','GET'])
def result():
    if request.method == 'POST':
        form_result = request.form
        j2data = read_html(form_result["date"], 'Jester 2nd Floor Dining')
        kinsdata = read_html(form_result["date"], 'Kinsolving Dining Hall')
        headers = ("Jester 2nd Floor Dining","Kinsolving Dining Hall")
        return render_template("result.html", headers=headers, j2data=j2data[form_result['meal_time']], kinsdata=kinsdata[form_result['meal_time']])

@app.route('/search', methods=['POST','GET'])
def search():
    if request.method == 'POST':
        form_result = request.form
        ret_map = find_day_for_food(form_result["food"])
        # PP.pprint(ret_map)
        return render_template("search.html", food=form_result["food"], dateloc=ret_map)
