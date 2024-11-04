from flask import Flask
from flask import render_template
from flask import request
import math

app = Flask(__name__)

PRICES = {
    'panel': 50,
    'post': 20,
    'pale': 3,
    '6x1': 2,
    '6x2': 4,
    'postcrete': 10
}

@app.route("/")
# Function to display default app layout and display job type dropdown
def layout():
    return render_template('layout.html')

@app.route("/measurements", methods=['GET'])
def measurements():
    selected_option = request.form.get('option')

    enabled_inputs = {
        'Length': False,
        'Width': False,
        'Height': False,
        'Area': False
    }

    if selected_option == 'panel_fence' or 'hit_miss' or 'feather_edge':
        enabled_inputs['Length'] = True
        enabled_inputs['Height'] = True
    return render_template('measurements.html', selected_option=selected_option, enabled_inputs=enabled_inputs)

@app.route("/calculations", methods=['GET', 'POST'])
def calculations():
    selected_option = request.form.get('selected_option')
    results = []

    length = float(request.form.get('Length', 0))
    width = float(request.form.get('Width', 0))
    height = float(request.form.get('Height', 0))
    area = float(request.form.get('Area', 0))

    if selected_option == 'panel_fence':
        total_panels = length / 1.8
        total_posts = math.ceil(length / 1.8) + 1
        total_postcrete = total_panels * 1.5
        results = {
            {'item': 'Panels', 'quantity': total_panels, 'cost': total_panels * PRICES['panel']},
            {'item': 'Posts', 'quantity': total_posts, 'cost': total_posts * PRICES['post']},
            {'item': 'Postcrete', 'quantity': total_postcrete, 'cost': total_postcrete * PRICES['postcrete']}
        }

    elif selected_option == 'hit_miss':
        total_posts = math.ceil(length / 1.8) + 1
        total_6x1 = ((height * 0.2 ) * length) + (length * 1.15)
        total_postcrete = total_panels * 1.5
        results = {
            {'item': '6x1', 'quantity': total_6x1, 'cost': total_6x1 * PRICES['6x1']},
            {'item': 'Posts', 'quantity': total_posts, 'cost': total_posts * PRICES['post']},
            {'item': 'Postcrete', 'quantity': total_postcrete, 'cost': total_postcrete * PRICES['postcrete']}
        }


    elif selected_option == 'feather_fence':
        total_pales = (length * 0.12) * 1.2
        total_6x2 = (length * 3) * 1.15
        total_6x1 = length * 1.1
        total_posts = (length / 1.8) + 1
        total_postcrete = total_panels * 1.5
        results = {
            {'item': 'Featheredge', 'quantity': total_pales, 'cost': total_pales * PRICES['pale']},
            {'item': '6x2', 'quantity': total_6x2, 'cost': total_6x2 * PRICES['6x2']},
            {'item': '6x1', 'quantity': total_6x1, 'cost': total_6x1 * PRICES['6x1']},
            {'item': 'Posts', 'quantity': total_posts, 'cost': total_posts * PRICES['post']},
            {'item': 'Postcrete', 'quantity': total_postcrete, 'cost': total_postcrete * PRICES['postcrete']}
        }

    # else:
    #     results = [{'item': 'Error', 'quantity': 'Invalid fence type selected', 'cost': 0}]
    
    total_cost = sum(item['cost'] for item in results)    



    return render_template('calculations.html', results=results, total_cost=total_cost, selected_option=selected_option)


if __name__ == "__main__":
    app.run(debug=True)
