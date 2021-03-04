from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, TextInput, Row, Column, MultiSelect, Button, Div, RangeSlider, \
    LinearColorMapper, LinearAxis, Range1d, HoverTool
from bokeh.io import curdoc
import pandas as pd

df = pd.read_csv('nd_data.csv')

def calc_petro(temp):
    temp['VSHALE'] = (temp['GR'] - temp['grmin'])/ (temp['grmax'] - temp['grmin'])
    temp['PHID'] = (temp['RHOB'] - temp['rhofl'])/(temp['rhoma'] - temp['rhofl'])
    temp['PHIT'] = (temp['NPHI'] + temp['PHID']) /2
    temp['PHIE'] = temp['PHIT'] - temp['VSHALE'] * temp['phish']
    return temp

cds = ColumnDataSource(df)
orig = ColumnDataSource(df)

temp = cds.data
cds.data = dict(calc_petro(temp))

nama = TextInput(value='', title='Nama')
nim = TextInput(value='', title='Nim')

gr_input = RangeSlider(start=0, end=150, value=(10, 110), step=1, title="Gr Max Gr Min", width=150)

grmin_input = TextInput(value='10', title='Gr Min Input', width=150)
grmax_input = TextInput(value='110', title='Gr Max Input', width=150)
rhoma_input = TextInput(value='2.65', title='Rho Matrix', width=150)
rhofl_input = TextInput(value='1.1', title='Rho Fluid', width=150)
phish_input = TextInput(value='0.4', title='Shale Porosity', width=150)

options = [("1", "zona 1"), ("2", "zona 2"), ("3", "zona 3"), ("4", "zona 4"),
           ("5", "zona 5"), ("6", "zona 6"), ("7", "zona 7"), ("8", "zona 8")]

matrix_opt = [("1", "Quartz"), ("2", "Calcite"), ("3", "Dolomite"), ('4', 'Coal'), ('5', 'Halite')]

color = {'1': 'red', '2': 'green', '3': 'blue', '4': 'purple', '5': 'orange', '6': 'teal', '7': 'gray', '8': 'violet'}
zone = MultiSelect(value=['1'], options=options, height=300, width=150)
matrix = MultiSelect(value=['1'], options=matrix_opt, height=150, width=150)

save = Button(label="Save", button_type="success")
reset = Button(label="Reset", button_type="success")
apply = Button(label="Apply", button_type="success", width=150)

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
zone_data = ColumnDataSource(dict(image=[df['zone'].values.reshape(-1, 1)[::-1]]))
zone_color = figure(plot_width=100, plot_height=600, title='Zone', tools='', x_axis_location="above")
zone_color.image(image='image', x=0, y=len(df), dw=1, dh=len(df), source=zone_data, palette='Spectral11')
zone_color.axis.visible = False
zone_color.toolbar.logo = None

TOOLTIPS = [("DEPT", "$index"),
            ("GR", "(@GR)"),
            ("N, D", "(@NPHI, @RHOB)"),
            ("Vshale",('@VSHALE')),
            ("PHIE", "@PHIE"),
            ("PHIT", "@PHIT"),]

gr_hover = HoverTool(tooltips=TOOLTIPS, mode='hline', line_policy='nearest', names=['gr_log'])
gr = figure(plot_width=300, plot_height=600, title='Gr', tools='ypan, ywheel_zoom, box_select', x_range=[0, 150],
            x_axis_location="above")
gr.add_tools(gr_hover)
gr.scatter('GR', 'DEPT', source=cds, color='color', line_alpha=0, alpha=0, selection_fill_alpha=0.5,
           nonselection_fill_alpha=0, nonselection_line_alpha=0)
gr.line('GR', 'DEPT', source=cds, color='green', name='gr_log')

gr.line('grmax', 'DEPT', source=cds, color='blue', line_width=3,  line_dash='dashed')
gr.line('grmin', 'DEPT', source=cds, color='red', line_width=3,  line_dash='dashed')
gr.yaxis.visible = False
gr.toolbar.logo = None

nphi = figure(plot_width=300, plot_height=600, title='nphi', tools='',
              x_range=[0.45, -0.15], x_axis_location="above", y_range=[max(df['DEPT']), min(df['DEPT'])])
nphi.line('NPHI', 'DEPT', source=cds, color='green')
nphi.line('phish', 'DEPT', source=cds, color='green', line_dash='dashed', line_width=3)
nphi.xaxis.axis_line_color = 'green'
nphi.xaxis.major_label_text_color = 'green'

nphi.extra_x_ranges = {'RHOB': Range1d(start=1.7, end=2.71, )}
nphi.add_layout(LinearAxis(x_range_name='RHOB'), 'above')
nphi.line('RHOB', 'DEPT', source=cds, color='red', x_range_name='RHOB')
nphi.line('rhoma', 'DEPT', source=cds, color='red', line_dash='dashed', x_range_name='RHOB', line_width=3)
nphi.toolbar.logo = None

phi = figure(plot_width=150, plot_height=600, title='PHI', tools='', x_range=[0, 0.6],
            x_axis_location="above")
phi.line('PHIE', 'DEPT', source=cds, color='green')
phi.line('PHIT', 'DEPT', source=cds, color='red')
phi.yaxis.visible = False
phi.toolbar.logo = None


color_mapper = LinearColorMapper(palette='Viridis256', low=0, high=120)

nd_plot = figure(plot_width=500, plot_height=500, title='ND Plot', tools='pan, wheel_zoom, reset,box_select',
                 x_range=[0, 1],
                 y_range=[3, 0])
nd_plot.scatter('NPHI', 'RHOB', source=cds, color={'field': 'GR', 'transform': color_mapper},
                size=5, alpha=0.4,
                nonselection_fill_alpha=0, nonselection_line_alpha=0)

nd_plot.line([-0.028, 1.15], [2.65 + 0.1, 1], line_dash='dashed', color='black')
nd_plot.line([0, 1.15], [2.71 + 0.1, 1], line_dash='dashed', color='black')
nd_plot.line([0.05, 1.15], [2.83 + 0.1, 1], line_dash='dashed', color='black')
nd_plot.toolbar.logo = None

phi.y_range = zone_color.y_range = gr.y_range = nphi.y_range

stack = Column(Row(Column(Row(nama, nim),
               Row(save, reset)), text, ),
               Row(Column(zone), Column(grmin_input, grmax_input, gr_input, rhoma_input, rhofl_input, phish_input, matrix, apply),
                   zone_color, gr, nphi, phi, nd_plot),
               Row(debug))

selected = []


def select_callback(attr, old, new):
    global selected
    selected = new


# def zone_callback(attr, old, new):
def zone_callback():
    try:
        mins = min(selected)
        maxs = max(selected)
        zone_sel = zone.value
        sel_color = color[zone_sel[0]]

        temp = cds.data
        temp['zone'][mins:maxs] = int(zone_sel[0])
        temp['grmax'][mins:maxs] = int(gr_input.value[1])
        temp['grmin'][mins:maxs] = int(gr_input.value[0])
        print(float(rhoma_input.value))
        temp['rhoma'][mins:maxs] = float(rhoma_input.value)
        temp['rhofl'][mins:maxs] = float(rhofl_input.value)
        temp['phish'][mins:maxs] = float(phish_input.value)
        temp['color'][mins:maxs] = sel_color

        temp = calc_petro(temp)
        cds.data = dict(temp)

        temp = cds.data['zone'].reshape(-1, 1)[::-1]
        temp[0] = 0
        temp[-1] = 12
        zone_data.data['image'] = [temp]

        # new_data = zone.value
        # temp = cds.data['zone']
        # temp[mins:maxs] = int(new_data[0])
        # cds.data['zone'] = temp
        #
        # temp = cds.data['grmax']
        # temp[mins:maxs] = int(gr_input.value[1])
        # cds.data['grmax'] = temp
        #
        # temp = cds.data['grmin']
        # temp[mins:maxs] = int(gr_input.value[0])
        # cds.data['grmin'] = temp
        #
        # temp = cds.data['rhoma']
        # temp[mins:maxs] = float(rhoma_input.value)
        # cds.data['rhoma'] = temp
        #
        # temp = cds.data['rhofl']
        # temp[mins:maxs] = float(rhofl_input.value)
        # cds.data['rhofl'] = temp
        #
        #
        # temp = cds.data['phish']
        # temp[mins:maxs] = float(phish_input.value)
        # cds.data['phish'] = temp
        #
        #
        # sel_color = color[new_data[0]]
        # temp = cds.data['color']
        # temp[mins:maxs] = sel_color
        # cds.data['color'] = temp


        # temp = cds.data['zone'].reshape(-1, 1)[::-1]
        # temp[0] = 0
        # temp[-1] = 12
        # zone_data.data['image'] = [temp]

        # cds.data['VSHALE'] = (cds.data['GR'] - cds.data['grmin']) / (cds.data['grmax'] - cds.data['grmin'])
        # cds.data['PHID'] = (cds.data['RHOB'] - cds.data['rhofl']) / (cds.data['rhoma'] - cds.data['rhofl'])
        # cds.data['PHIT'] = (cds.data['NPHI'] + cds.data['PHID']) / 2
        # cds.data['PHIE'] = cds.data['PHIT'] - cds.data['VSHALE'] * cds.data['phish']

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
        temp.to_csv(f'tugas_nd\{nm}_{ni}.csv')
        debug.text = f'successfully saved as {nm}_{ni}'
    except:
        debug.text = f'failed to saved as {nm}_{ni}'


def reset_callback():
    cds.data['zone'] = [-999] * len(cds.data['zone'])
    cds.data['color'] = ['black'] * len(cds.data['color'])

def matrix_callback(attr, old, new):
    mat_code = {'1':2.65, '2':2.71, '3':2.83, '4':1.4, '5':2.20}
    val = mat_code[matrix.value[0]]
    rhoma_input.value = str(val)

matrix.on_change('value', matrix_callback)

gr_input.on_change('value', gr_input_callback)
cds.selected.on_change('indices', select_callback)
apply.on_click(zone_callback)
save.on_click(save_callback)
reset.on_click(reset_callback)

curdoc().add_root(stack)
