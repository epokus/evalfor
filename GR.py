from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, TextInput, Row, Column, MultiSelect, Button, Div, RangeSlider
from bokeh.io import curdoc, show



import pandas as pd
import numpy as np

df = pd.read_csv('well.csv',sep=';').dropna(subset=['GR'])
df = df[['GR', 'DEPT']].iloc[::10,:].reset_index(drop=True)
df['idx'] = df.index
df['zone'] = -999
df['color'] = 'black'
df['grmax'] = 100
df['grmin'] = 20

cds = ColumnDataSource(df)
orig = ColumnDataSource(df)

nama = TextInput(value='', title='Nama')
nim = TextInput(value='',title='Nim')

gr_input = RangeSlider(start=0, end=150, value=(10,110), step=1, title="Gr Max Gr Min")

#
grmin_input = TextInput(value='10', title='Gr Min Input')
grmax_input = TextInput(value='110', title='Gr Max Input')

options = [("1", "zona 1"), ("2", "zona 2"), ("3", "zona 3"), ("4", "zona 4"),
           ("5", "zona 5"), ("6", "zona 6"), ("7", "zona 7"), ("8", "zona 8")]

color ={'1':'red','2':'green','3':'blue','4':'purple','5':'orange','6':'teal','7':'gray','8':'violet'}
zone = MultiSelect(value=['1'],options=options, height=300, width=150)
save = Button(label="Save", button_type="success")
reset = Button(label="Reset", button_type="success")
apply = Button(label="Apply", button_type="success")

text = Div(text="""<table style="width: 100%; border-collapse: collapse; border-style: none;">
                        <tbody>
                        <tr>
                        <td style="width: 14.076%;"><img src="https://universitaspertamina.ac.id/wp-content/uploads/2017/11/logo-Press.png" alt="" width="50" height="36" /></td>
                        <td style="width: 85.924%;">
                        <p style="font-size:11px">This app is created for <strong>Evaluation Formation Course (GL 3202) </strong> by Epo P Kusumah Geological Engineering Department&copy;</p>
                        </td>
                        </tr>
                        </tbody>
                        </table>
    """, )
debug = Div(text='')
gr = figure(plot_width=300, plot_height=600, title='Gr', tools='ypan, ywheel_zoom, box_select')
gr.scatter('GR', 'DEPT', source=cds, color='color', alpha=0.5)
gr.line('GR', 'DEPT', source=cds,color='green', alpha=0.3)
gr.line('grmax', 'DEPT', source=cds,color='blue', line_width=3)
gr.line('grmin', 'DEPT', source=cds,color='red', line_width=3)

gr.y_range.flipped = True

stack = Column(Row(nama, nim), Row(save, reset),Row(zone,gr,Column(grmin_input,grmax_input, gr_input, apply)), text, debug)

selected = []

def select_callback(attr, old, new):
     global selected
     selected = new

# def zone_callback(attr, old, new):
def zone_callback():

    try:
        # print(gr_input.value)
        new_data = zone.value
        temp = cds.data['zone']
        temp[selected] = int(new_data[0])
        cds.data['zone'] = temp

        temp = cds.data['grmax']
        temp[selected] = int(gr_input.value[1])
        cds.data['grmax'] = temp

        temp = cds.data['grmin']
        temp[selected] = int(gr_input.value[0])
        cds.data['grmin'] = temp

        sel_color = color[new_data[0]]
        temp = cds.data['color']
        temp[selected] = sel_color
        cds.data['color'] = temp


    except:
        debug.text = 'error please select data or zone'

def gr_input_callback(attr, old, new):
    grmin_input.value = str(gr_input.value[0])
    grmax_input.value = str(gr_input.value[1])

def save_callback():
    try:
        temp = pd.DataFrame(cds.data)
        nm = nama.value
        ni = nim.value
        temp.to_csv(f'tugas_gr\{nm}_{ni}.csv')
        debug.text = f'successfully saved as {nm}_{ni}'
    except:
        debug.text = f'failed to saved as {nm}_{ni}'


def reset_callback():
    cds.data['zone'] = [-999]*len(cds.data['zone'])
    cds.data['color'] = ['black']*len(cds.data['color'])

gr_input.on_change('value', gr_input_callback)
cds.selected.on_change('indices', select_callback)
# zone.on_change('value', zone_callback)
apply.on_click(zone_callback)
save.on_click(save_callback)
reset.on_click(reset_callback)

# show(stack)

curdoc().add_root(stack)
# AttributeError: unexpected attribute 'data' to Scatter, possible attributes are angle, angle_units, fill_alpha, fill_color, js_event_callbacks, js_property_callbacks, line_alpha, line_cap, line_color, line_dash, line_dash_offset, line_join, line_width, marker, name, size, subscribed_events, tags, x or y
