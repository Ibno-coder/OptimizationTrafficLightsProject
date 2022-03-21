import random
from tkinter import *
from tkinter import ttk

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from DE import BaseDE
from GA import BaseGA

_matrice_Feux_R = []
_matrice_Feux_V = []
_matrice_Veh = []
_matrice_Feux_Veh = [0 for _ in range(64)]
_matrice_sec_Veh = [0 for _ in range(16)]

completeGA, completeDE = False, False
solutionGA = []
solutionDE = []
fitnessDE = []
fitnessGA = []

def obj_func(X, problem):
    """
    :param X:
    :return:
    """
    # use import variables from ga_settings

    for i in range(len(X)):
        if _matrice_Feux_Veh[i] > (_matrice_sec_Veh[int(i/4)] * .5):
            r = random.randint(2, 5)
        else:
            r = random.randint(0, 2)
        if problem == 0:
            X[i] = int(X[i]) - r
        else:
            X[i] = int(X[i]) + r

    return sum(X)

def createTableVeh(root, columns=(1, 2, 3, 4), label=None):
    if label is None:
        label = ['N° Veh', 'X_POS', 'Y_POS', 'N° interSec']
    trv_ = ttk.Treeview(root, columns=columns)
    trv_['show'] = 'headings'
    for i in range(4):
        trv_.heading(str(i + 1), text=label[i])
        trv_.column(str(i + 1), minwidth=120, width=143, stretch=NO, anchor='center')

    ysb = ttk.Scrollbar(root, orient=VERTICAL, command=trv_.yview)
    xsb = ttk.Scrollbar(root, orient=HORIZONTAL, command=trv_.xview)
    trv_['yscroll'] = ysb.set
    trv_['xscroll'] = xsb.set

    trv_.place(x=0, y=0, width=590, height=390)
    ysb.pack(side=RIGHT, fill='y')
    xsb.pack(side=BOTTOM, fill='x')
    return trv_

def createFeux_Veh(base, width=None, height=None, x=0, y=0):
    columnsF = [i for i in range(1, 67)]
    trv_ = ttk.Treeview(base, columns=columnsF)
    trv_['show'] = 'headings'

    trv_.heading('1', text='N° Feux')
    trv_.column('1', minwidth=100, width=100, stretch=NO, anchor='center')
    for i in range(2, 66):
        trv_.heading(str(i), text='F ' + str(i - 1))
        trv_.column(str(i), minwidth=50, width=70, stretch=NO, anchor='center')

    trv_.heading('66', text='Total ')
    trv_.column('66', minwidth=100, width=100, stretch=NO, anchor='center')
    ysb = ttk.Scrollbar(base, orient=VERTICAL, command=trv_.yview)
    xsb = ttk.Scrollbar(base, orient=HORIZONTAL, command=trv_.xview)
    trv_['yscroll'] = ysb.set
    trv_['xscroll'] = xsb.set

    trv_.place(x=x, y=y, width=width, height=height)
    ysb.pack(side=RIGHT, fill='y')
    xsb.pack(side=BOTTOM, fill='x')
    return trv_



def createSec_Veh(base, width=None, height=None):
    columnsF = [i for i in range(1, 19)]
    trv_ = ttk.Treeview(base, columns=columnsF)
    trv_['show'] = 'headings'

    trv_.heading('1', text='N° inter-Section')
    trv_.column('1', minwidth=100, width=100, stretch=NO, anchor='center')
    for i in range(2, 18):
        trv_.heading(str(i), text='In-Sec ' + str(i - 1))
        trv_.column(str(i), minwidth=50, width=70, stretch=NO, anchor='center')

    trv_.heading('18', text='Total ')
    trv_.column('18', minwidth=100, width=100, stretch=NO, anchor='center')
    ysb = ttk.Scrollbar(base, orient=VERTICAL, command=trv_.yview)
    xsb = ttk.Scrollbar(base, orient=HORIZONTAL, command=trv_.xview)
    trv_['yscroll'] = ysb.set
    trv_['xscroll'] = xsb.set

    trv_.place(x=0, y=0, width=width, height=height)
    ysb.pack(side=RIGHT, fill='y')
    xsb.pack(side=BOTTOM, fill='x')
    return trv_

def createFeux(base, width=None, height=None):
    columnsF = [i for i in range(1, 67)]
    trv_ = ttk.Treeview(base, columns=columnsF)
    trv_['show'] = 'headings'

    trv_.heading('1', text='Iteration')
    trv_.column('1', minwidth=100, width=100, stretch=NO, anchor='center')
    for i in range(2, 66):
        trv_.heading(str(i), text='F' + str(i - 1))
        trv_.column(str(i), minwidth=50, width=50, stretch=NO, anchor='center')

    trv_.heading('66', text='Total')
    trv_.column('66', minwidth=100, width=100, stretch=NO, anchor='center')
    ysb = ttk.Scrollbar(base, orient=VERTICAL, command=trv_.yview)
    xsb = ttk.Scrollbar(base, orient=HORIZONTAL, command=trv_.xview)
    trv_['yscroll'] = ysb.set
    trv_['xscroll'] = xsb.set

    trv_.place(x=0, y=0, width=width, height=height)
    ysb.pack(side=RIGHT, fill='y')
    xsb.pack(side=BOTTOM, fill='x')
    return trv_


def creationResau(size=None):
    if size is None:
        size = int(nbr_vec.get())
    trv_veh.delete(*trv_veh.get_children())
    trv_feux_veh.delete(*trv_feux_veh.get_children())
    trv_sec_veh.delete(*trv_sec_veh.get_children())
    _matrice_Veh.clear()
    _matrice_Veh.clear()
    _matrice_Veh.clear()
    for i in range(size):
        id_sec = random.randint(0, 15)
        _matrice_sec_Veh[id_sec] += 1
        id_Feux = id_sec * 4 + random.randint(0, 3)
        _matrice_Feux_Veh[id_Feux] += 1
        _i_Veh = ['Veh ' + str(i + 1), 0, 0, str(id_sec+1)]
        trv_veh.insert('', 'end', value=_i_Veh)
        _matrice_Veh.append(_i_Veh)
    showSec_Veh = ['N° Vehicules']
    showSec_Veh +=  _matrice_sec_Veh
    showSec_Veh.append(sum(_matrice_sec_Veh))

    showFeux_Veh = ['N° Vehicules']
    showFeux_Veh += _matrice_Feux_Veh
    showFeux_Veh.append(sum(_matrice_Feux_Veh))
    trv_sec_veh.insert('','end', value=showSec_Veh)
    trv_feux_veh.insert('','end', value=showFeux_Veh)

def creationSolution(size=None):
    if size is None:
        size = int(_iter.get())
    trv_F_R.delete(*trv_F_R.get_children())
    trv_F_V.delete(*trv_F_V.get_children())
    _matrice_Feux_V.clear()
    _matrice_Feux_R.clear()
    for i in range(size):
        _i_Feux_R = [i + 1]
        _i_Feux_R += [random.randint(int(_r_min.get()), int(_r_max.get())) for _ in range(64)]
        _i_Feux_R.append(sum(_i_Feux_R[1:]))

        _i_Feux_V = [i + 1]
        _i_Feux_V += [random.randint(int(_g_min.get()), int(_g_max.get())) for _ in range(64)]
        _i_Feux_V.append(sum(_i_Feux_V[1:]))

        trv_F_R.insert('', 'end', value=_i_Feux_R)
        trv_F_V.insert('', 'end', value=_i_Feux_V)
        _matrice_Feux_R.append(_i_Feux_R)
        _matrice_Feux_V.append(_i_Feux_V)

#------------------------------------------- DE Setting and frame ---------------------------------------------
def lanceFrameDE():

    frameDe = Toplevel(root)
    wrapper_settings_global = LabelFrame(frameDe, text='Paramettre du réseau')
    wrapper_settings_DE = LabelFrame(frameDe, text='Paramettres de DE')
    wrapper_show_DE = LabelFrame(frameDe, text='Affichage de DE')

    tabControlDE = ttk.Notebook(wrapper_show_DE)

    pop_intial_red = ttk.Frame(tabControlDE)
    pop_intial_green = ttk.Frame(tabControlDE)
    variation_fit_red = ttk.Frame(tabControlDE)
    variation_fit_green = ttk.Frame(tabControlDE)
    best_solutions_red = ttk.Frame(tabControlDE)
    best_solutions_green = ttk.Frame(tabControlDE)

    tabControlDE.add(pop_intial_red, text='Rouge Pop Initial')
    tabControlDE.add(pop_intial_green, text='Vert Pop Initial')
    tabControlDE.add(variation_fit_red, text='Rouge Variation Fit')
    tabControlDE.add(variation_fit_green, text='Vert Variation Fit')
    tabControlDE.add(best_solutions_red, text='Rouge Meil. Sols.')
    tabControlDE.add(best_solutions_green, text='Vert Meil. Sols.')
    tabControlDE.pack(expand=1, fill="both")

    # tables
    trv_pop_init_red = createFeux(pop_intial_red, 680, 220)
    trv_pop_init_green = createFeux(pop_intial_green, 680, 220)
    trv_best_solu_red = createFeux(best_solutions_red, 680, 220)
    trv_best_solu_green = createFeux(best_solutions_green, 680, 220)
    _mat__ = {
        0: {},
        -1: {}
    }
    _mat__[0]['pop'] = trv_pop_init_red
    _mat__[-1]['pop'] = trv_pop_init_green
    _mat__[0]['best'] = trv_best_solu_red
    _mat__[-1]['best'] = trv_best_solu_green
    # settings
    lbl_vec_de = Label(wrapper_settings_global, text='Nbr. de vehicules')
    nbr_vec_de = Entry(wrapper_settings_global, foreground='black')
    lbl_vec_de.place(x=10, y=10, width=100)
    nbr_vec_de.place(x=140, y=10, width=100)
    wrapper_F_R_de = LabelFrame(wrapper_settings_global, text='Feux Rouges')
    wrapper_F_V_de = LabelFrame(wrapper_settings_global, text='Feux Vert')
    wrapper_F_R_de.place(x=250, y=5, width=120, height=100)
    wrapper_F_V_de.place(x=390, y=5, width=120, height=100)
    # red min & max
    lbl_r_min_de = Label(wrapper_F_R_de, text='Tps .min')
    _r_min_de = Entry(wrapper_F_R_de, foreground='red')
    lbl_r_max_de = Label(wrapper_F_R_de, text='Tps .max')
    _r_max_de = Entry(wrapper_F_R_de, foreground='red')

    lbl_r_min_de.place(x=10, y=10, width=50)
    _r_min_de.place(x=60, y=10, width=50)
    lbl_r_max_de.place(x=10, y=50, width=50)
    _r_max_de.place(x=60, y=50, width=50)
    # green min & max
    lbl_g_min_de = Label(wrapper_F_V_de, text='Tps .min')
    _g_min_de = Entry(wrapper_F_V_de, foreground='green')
    lbl_g_max_de = Label(wrapper_F_V_de, text='Tps .max')
    _g_max_de = Entry(wrapper_F_V_de, foreground='green')

    lbl_g_min_de.place(x=10, y=10, width=50)
    _g_min_de.place(x=60, y=10, width=50)
    lbl_g_max_de.place(x=10, y=50, width=50)
    _g_max_de.place(x=60, y=50, width=50)
    _r_min_de.insert('end', '20')
    _r_max_de.insert('end', '30')

    _g_min_de.insert('end', '30')
    _g_max_de.insert('end', '50')
    nbr_vec_de.insert('end', nbr_vec.get())
    nbr_vec_de.configure(state='disabled')
    # setting DE
    btn_sol_de = Button(wrapper_settings_DE, text='Lance DE', command=lambda: lanceDE([int(_g_min_de.get()),int(_g_max_de.get())],
                                                                                      [int(_r_min_de.get()),int(_r_max_de.get())],
                                                                                      int(_epoch_DE.get()),
                                                                                      int(_pop_DE.get()),
                                                                                      float(_cr_DE.get())/100,
                                                                                      float(_fw_DE.get())/100,
                                                                                      _mat__,
                                                                                      variation_fit_red,
                                                                                      variation_fit_green
                                                                                      )
                        )
    btn_sol_de.place(x=5, y=25, width=115, height=40)
    lbl_wf_DE = Label(wrapper_settings_DE, text='facteur de pondération %')
    _fw_DE = Entry(wrapper_settings_DE)
    lbl_cr_DE = Label(wrapper_settings_DE, text='Taux de croissement %')
    _cr_DE = Entry(wrapper_settings_DE)
    lbl_epoch_DE = Label(wrapper_settings_DE, text='Nbr. d\'iteration')
    _epoch_DE = Entry(wrapper_settings_DE)
    lbl_pop_DE = Label(wrapper_settings_DE, text='Taille de population')
    _pop_DE = Entry(wrapper_settings_DE)

    lbl_wf_DE.place(x=130, y=10, width=150)
    _fw_DE.place(x=280, y=10, width=50)
    lbl_cr_DE.place(x=140, y=60, width=130)
    _cr_DE.place(x=280, y=60, width=50)

    lbl_epoch_DE.place(x=350, y=10, width=130)
    _epoch_DE.place(x=480, y=10, width=50)
    lbl_pop_DE.place(x=350, y=60, width=130)
    _pop_DE.place(x=480, y=60, width=50)
    _fw_DE.insert('end','2.5')
    _cr_DE.insert('end','90')
    _epoch_DE.insert('end', '50')
    _pop_DE.insert('end', '32')

    wrapper_settings_global.place(x=5, y=5, width=690, height=130)
    wrapper_settings_DE.place(x=5, y=135, width=690, height=120)
    wrapper_show_DE.place(x=5, y=260, width=690, height=280)

    frameDe.geometry('700x550')

def lanceFrameGA():

    frameGA = Toplevel(root)
    wrapper_settings_global = LabelFrame(frameGA, text='Paramettre du réseau')
    wrapper_settings_GA = LabelFrame(frameGA, text='Paramettres de GA')
    wrapper_show_GA = LabelFrame(frameGA, text='Affichage de GA')

    tabControlGA = ttk.Notebook(wrapper_show_GA)

    pop_intial_red = ttk.Frame(tabControlGA)
    pop_intial_green = ttk.Frame(tabControlGA)
    variation_fit_red = ttk.Frame(tabControlGA)
    variation_fit_green = ttk.Frame(tabControlGA)
    best_solutions_red = ttk.Frame(tabControlGA)
    best_solutions_green = ttk.Frame(tabControlGA)

    tabControlGA.add(pop_intial_red, text='Rouge Pop Initial')
    tabControlGA.add(pop_intial_green, text='Vert Pop Initial')
    tabControlGA.add(variation_fit_red, text='Rouge Variation Fit')
    tabControlGA.add(variation_fit_green, text='Vert Variation Fit')
    tabControlGA.add(best_solutions_red, text='Rouge Meil. Sols.')
    tabControlGA.add(best_solutions_green, text='Vert Meil. Sols.')
    tabControlGA.pack(expand=1, fill="both")

    # tables
    trv_pop_init_red = createFeux(pop_intial_red, 680, 220)
    trv_pop_init_green = createFeux(pop_intial_green, 680, 220)
    trv_best_solu_red = createFeux(best_solutions_red, 680, 220)
    trv_best_solu_green = createFeux(best_solutions_green, 680, 220)
    _mat__ = {
        0: {},
        -1: {}
    }
    _mat__[0]['pop'] = trv_pop_init_red
    _mat__[-1]['pop'] = trv_pop_init_green
    _mat__[0]['best'] = trv_best_solu_red
    _mat__[-1]['best'] = trv_best_solu_green
    # settings
    lbl_vec_ga = Label(wrapper_settings_global, text='Nbr. de vehicules')
    nbr_vec_ga = Entry(wrapper_settings_global, foreground='black')
    lbl_vec_ga.place(x=10, y=10, width=100)
    nbr_vec_ga.place(x=140, y=10, width=100)
    wrapper_F_R_ga = LabelFrame(wrapper_settings_global, text='Feux Rouges')
    wrapper_F_V_ga = LabelFrame(wrapper_settings_global, text='Feux Vert')
    wrapper_F_R_ga.place(x=250, y=5, width=120, height=100)
    wrapper_F_V_ga.place(x=390, y=5, width=120, height=100)
    # red min & max
    lbl_r_min_ga = Label(wrapper_F_R_ga, text='Tps .min')
    _r_min_ga = Entry(wrapper_F_R_ga, foreground='red')
    lbl_r_max_ga = Label(wrapper_F_R_ga, text='Tps .max')
    _r_max_ga = Entry(wrapper_F_R_ga, foreground='red')

    lbl_r_min_ga.place(x=10, y=10, width=50)
    _r_min_ga.place(x=60, y=10, width=50)
    lbl_r_max_ga.place(x=10, y=50, width=50)
    _r_max_ga.place(x=60, y=50, width=50)
    # green min & max
    lbl_g_min_ga = Label(wrapper_F_V_ga, text='Tps .min')
    _g_min_ga = Entry(wrapper_F_V_ga, foreground='green')
    lbl_g_max_ga = Label(wrapper_F_V_ga, text='Tps .max')
    _g_max_ga = Entry(wrapper_F_V_ga, foreground='green')

    lbl_g_min_ga.place(x=10, y=10, width=50)
    _g_min_ga.place(x=60, y=10, width=50)
    lbl_g_max_ga.place(x=10, y=50, width=50)
    _g_max_ga.place(x=60, y=50, width=50)
    _r_min_ga.insert('end', '20')
    _r_max_ga.insert('end', '30')

    _g_min_ga.insert('end', '30')
    _g_max_ga.insert('end', '50')
    nbr_vec_ga.insert('end', nbr_vec.get())
    nbr_vec_ga.configure(state='disabled')
    # setting DE
    btn_sol_ga = Button(wrapper_settings_GA, text='Lance GA', command=lambda: lanceGA([int(_g_min_ga.get()),int(_g_max_ga.get())],
                                                                                      [int(_r_min_ga.get()),int(_r_max_ga.get())],
                                                                                      int(_epoch_ga.get()),
                                                                                      int(_pop_ga.get()),
                                                                                      float(_cr_ga.get())/100,
                                                                                      float(_mt_ga.get())/100,
                                                                                      _mat__,
                                                                                      variation_fit_red,
                                                                                      variation_fit_green
                                                                                      )
                        )
    btn_sol_ga.place(x=5, y=25, width=115, height=40)
    lbl_cr_ga = Label(wrapper_settings_GA, text='Taux de croissement %')
    _cr_ga = Entry(wrapper_settings_GA)
    lbl_mt_ga = Label(wrapper_settings_GA, text='Taux de mutation %')
    _mt_ga = Entry(wrapper_settings_GA)

    lbl_epoch_ga = Label(wrapper_settings_GA, text='Nbr. d\'iteration')
    _epoch_ga = Entry(wrapper_settings_GA)
    lbl_pop_ga = Label(wrapper_settings_GA, text='Taille de population')
    _pop_ga = Entry(wrapper_settings_GA)

    lbl_cr_ga.place(x=140, y=10, width=130)
    _cr_ga.place(x=280, y=10, width=50)
    lbl_mt_ga.place(x=140, y=50, width=130)
    _mt_ga.place(x=280, y=50, width=50)

    lbl_epoch_ga.place(x=350, y=10, width=130)
    _epoch_ga.place(x=480, y=10, width=50)
    lbl_pop_ga.place(x=350, y=60, width=130)
    _pop_ga.place(x=480, y=60, width=50)

    _cr_ga.insert('end','90')
    _mt_ga.insert('end','2.5')
    _epoch_ga.insert('end', '50')
    _pop_ga.insert('end', '32')

    wrapper_settings_global.place(x=5, y=5, width=690, height=130)
    wrapper_settings_GA.place(x=5, y=135, width=690, height=120)
    wrapper_show_GA.place(x=5, y=260, width=690, height=280)

    frameGA.geometry('700x550')


def lanceDE(g, r, epoch, pop_size, cr, wf, _mat__, fit_red, fit_green):
    global completeDE, solutionDE, fitnessDE
    verbose = False
    lowB_r, lowB_g = r[0], g[0]
    upB_r,  upB_g = r[1], g[1]
    md_red = BaseDE(obj_func, lowB_r, upB_r, 0, _mat__, verbose, epoch, pop_size, wf, cr, problem_size=64)
    md_green = BaseDE(obj_func, lowB_g, upB_g, -1, _mat__, verbose, epoch, pop_size, wf, cr, problem_size=64)
    best_sol_gr, best_fit_gr, variation_fit_g = md_green.train()
    best_sol_red, best_fit_red, variation_fit_r = md_red.train()

    figure_gr = plt.Figure(figsize=(7, 1), dpi=100)
    ax_green = figure_gr.add_subplot(111)
    ax_green.plot(np.arange(1, epoch+1), variation_fit_g, color='g')
    plot_gr = FigureCanvasTkAgg(figure_gr, fit_green)
    plot_gr.get_tk_widget().pack(side=LEFT, fill=BOTH)
    ax_green.legend(['Fitness Vert'])
    ax_green.set_xlim(0, epoch + 1)
    ax_green.set_ylabel('Scores DE')
    ax_green.grid(True)
    ax_green.set_title('Variation de Fitness Feux Vert')

    figure_red = plt.Figure(figsize=(7,4), dpi=100)
    ax_red = figure_red.add_subplot(111)
    ax_red.plot(np.arange(1, epoch + 1), variation_fit_r, color='r')
    plot_red = FigureCanvasTkAgg(figure_red, fit_red)
    plot_red.get_tk_widget().pack(side=LEFT, fill=BOTH)
    ax_red.legend(['Fitness Rouge'])
    ax_red.set_xlim(0, epoch + 1)
    ax_red.set_ylabel('Scores DE')
    ax_red.grid(True)
    ax_red.set_title('Variation de Fitness Feux Rouge')

    best_sol_gr = [a for a in best_sol_gr]
    best_sol_red = [a for a in best_sol_red]
    best_sol_gr.append(best_fit_gr)
    best_sol_red.append(best_fit_red)
    showBest_solu_g_DE = ['Valeur s'] + best_sol_gr
    showBest_solu_r_DE = ['Valeur s'] + best_sol_red
    t_b_g_de.insert('', 'end', value=showBest_solu_g_DE)
    t_b_r_de.insert('', 'end', value=showBest_solu_r_DE)
    completeDE = True
    solutionDE = [best_sol_gr, best_sol_red]
    fitnessDE = [variation_fit_g, variation_fit_r]

def lanceGA(g, r, epoch, pop_size, cr, mt, _mat__, fit_red, fit_green):
    global completeGA, solutionGA, fitnessGA
    verbose = False
    lowB_r, lowB_g = [r[0] for _ in range(64)], [g[0] for _ in range(64)]
    upB_r,  upB_g = [r[1] for _ in range(64)], [g[1] for _ in range(64)]
    md_red = BaseGA(obj_func, lowB_r, upB_r, 0, _mat__, verbose, epoch, pop_size, cr, mt)
    md_green = BaseGA(obj_func, lowB_g, upB_g, -1, _mat__, verbose, epoch, pop_size, cr, mt)
    best_sol_gr, best_fit_gr, variation_fit_g = md_green.train()
    best_sol_red, best_fit_red, variation_fit_r = md_red.train()
    # green
    figure_gr = plt.Figure(figsize=(7, 1), dpi=100)
    ax_green = figure_gr.add_subplot(111)
    #ax_green.fill_between(np.arange(1, epoch + 1), variation_fit_g[0]-20, variation_fit_g, facecolor='green', alpha=0.5)
    ax_green.plot(np.arange(1, epoch+1), variation_fit_g, color='g')
    plot_gr = FigureCanvasTkAgg(figure_gr, fit_green)
    plot_gr.get_tk_widget().pack(side=LEFT, fill=BOTH)
    ax_green.legend(['Fitness Vert'])
    ax_green.set_xlim(0, epoch + 1)
    ax_green.set_ylabel('Scores GA')
    ax_green.grid(True)
    ax_green.set_title('Variation de Fitness Feux Vert')
    #red
    figure_red = plt.Figure(figsize=(7,4), dpi=100)
    ax_red = figure_red.add_subplot(111)
    #ax_red.fill_between(np.arange(1, epoch + 1), variation_fit_r[-1]-20, variation_fit_r, facecolor='red', alpha=0.5)
    ax_red.plot(np.arange(1, epoch + 1), variation_fit_r, color='r')
    plot_red = FigureCanvasTkAgg(figure_red, fit_red)
    plot_red.get_tk_widget().pack(side=LEFT, fill=BOTH)
    ax_red.legend(['Fitness Rouge'])
    ax_red.set_xlim(0, epoch + 1)
    ax_red.set_ylabel('Scores GA')
    ax_red.grid(True)
    ax_red.set_title('Variation de Fitness Feux Rouge')

    best_sol_gr = [a for a in best_sol_gr]
    best_sol_red = [a for a in best_sol_red]
    best_sol_gr.append(best_fit_gr)
    best_sol_red.append(best_fit_red)
    showBest_solu_g_GA = ['Valeur s'] + best_sol_gr
    showBest_solu_r_GA = ['Valeur s'] + best_sol_red
    t_b_g_ga.insert('','end',value=showBest_solu_g_GA)
    t_b_r_ga.insert('','end',value=showBest_solu_r_GA)
    completeGA = True
    solutionGA = [best_sol_gr, best_sol_red]
    fitnessGA = [variation_fit_g, variation_fit_r]

def comparison():
    global completeDE, completeGA
    if completeGA and completeDE:
        # green
        figure_gr = plt.Figure(figsize=(7, 1), dpi=90)
        ax_gr = figure_gr.add_subplot(111)

        ax_gr.plot(np.arange(1, len(fitnessGA[0]) + 1), fitnessGA[0], color='g')
        ax_gr.plot(np.arange(1, len(fitnessDE[0]) + 1), fitnessDE[0], color='r')
        ax_gr.legend(['Fitness GA', 'Fitness DE'])
        ax_gr.set_xlim(0, len(fitnessDE[0]) + 1)
        ax_gr.set_ylabel('Scores GA and DE')
        ax_gr.grid(True)

        plot_gr = FigureCanvasTkAgg(figure_gr, comp_g_)
        plot_gr.get_tk_widget().pack(side=LEFT, fill=BOTH)
        # red
        figure_red = plt.Figure(figsize=(7, 1), dpi=90)
        ax_red = figure_red.add_subplot(111)
        ax_red.plot(np.arange(1, len(fitnessGA[1]) + 1), fitnessGA[1], color='g')
        ax_red.plot(np.arange(1, len(fitnessDE[1]) + 1), fitnessDE[1], color='r')
        ax_red.legend(['Fitness GA', 'Fitness DE'])
        ax_red.set_xlim(0, len(fitnessDE[1]) + 1)
        ax_red.set_ylabel('Scores GA and DE')
        ax_red.grid(True)


        plot_red = FigureCanvasTkAgg(figure_red, comp_r_)
        plot_red.get_tk_widget().pack(side=LEFT, fill=BOTH)


root = Tk()
wrapper_setting = LabelFrame(root, text='Paramettre du réseau')
wrapper_choice = LabelFrame(root, text='Lance Solution')
wrapper_solutions = LabelFrame(root, text='Solutions')
tabControl = ttk.Notebook(wrapper_solutions)

tab_veh = ttk.Frame(tabControl)
tab_veh_Sec = ttk.Frame(tabControl)
tab_veh_Feu = ttk.Frame(tabControl)
tab_Solutions = ttk.Frame(tabControl)
tab_Comp = ttk.Frame(tabControl)
tab_Feux_R = ttk.Frame(tabControl)
tab_Feux_V = ttk.Frame(tabControl)

tabControl.add(tab_veh, text='Vehicules')
tabControl.add(tab_veh_Sec, text='inter-Section')
tabControl.add(tab_veh_Feu, text='Feux')
tabControl.add(tab_Feux_V, text='Feux Vert')
tabControl.add(tab_Feux_R, text='Feux Rouge')
tabControl.add(tab_Solutions, text='Solutions')
tabControl.add(tab_Comp, text='Comparaison')
tabControl.pack(expand=1, fill="both")

# tables
trv_veh = createTableVeh(tab_veh)
trv_sec_veh = createSec_Veh(tab_veh_Sec, 590, 100)
trv_feux_veh = createFeux_Veh(tab_veh_Feu, 590, 100)
trv_F_R = createFeux(tab_Feux_R, 590, 390)
trv_F_V = createFeux(tab_Feux_V, 590, 390)

f_g_de = LabelFrame(tab_Solutions, text='Meilleur Solution Vert DE')
f_r_de = LabelFrame(tab_Solutions, text='Meilleur Solution Rouge DE')
f_g_ga = LabelFrame(tab_Solutions, text='Meilleur Solution Vert GA')
f_r_ga = LabelFrame(tab_Solutions, text='Meilleur Solution Rouge GA')
f_g_de.place(x=0,y=0, width=590, height=90)
f_r_de.place(x=0,y=100, width=590, height=90)
f_g_ga.place(x=0,y=200, width=590, height=90)
f_r_ga.place(x=0,y=300, width=590, height=90)
t_b_g_de = createFeux_Veh(f_g_de, 590, 75)
t_b_r_de = createFeux_Veh(f_r_de, 590, 75)
t_b_g_ga = createFeux_Veh(f_g_ga, 590, 75)
t_b_r_ga = createFeux_Veh(f_r_ga, 590, 75)

# settings
lbl_vec = Label(wrapper_setting, text='Nbr. de vehicules')
nbr_vec = Entry(wrapper_setting, foreground='black')
lbl_vec.place(x=10, y=10, width=100)
nbr_vec.place(x=140, y=10, width=100)
wrapper_F_R = LabelFrame(wrapper_setting, text='Feux Rouges')
wrapper_F_V = LabelFrame(wrapper_setting, text='Feux Vert')
wrapper_F_R.place(x=5, y=50, width=120, height=100)
wrapper_F_V.place(x=125, y=50, width=120, height=100)
# red min & max
lbl_r_min = Label(wrapper_F_R, text='Tps .min')
_r_min = Entry(wrapper_F_R, foreground='red')

lbl_r_max = Label(wrapper_F_R, text='Tps .max')
_r_max = Entry(wrapper_F_R, foreground='red')
lbl_r_min.place(x=10, y=10, width=50)
_r_min.place(x=60, y=10, width=50)
lbl_r_max.place(x=10, y=50, width=50)
_r_max.place(x=60, y=50, width=50)
# green min & max
lbl_g_min = Label(wrapper_F_V, text='Tps .min')
_g_min = Entry(wrapper_F_V, foreground='green')
lbl_g_max = Label(wrapper_F_V, text='Tps .max')
_g_max = Entry(wrapper_F_V, foreground='green')
lbl_g_min.place(x=10, y=10, width=50)
_g_min.place(x=60, y=10, width=50)
lbl_g_max.place(x=10, y=50, width=50)
_g_max.place(x=60, y=50, width=50)
_r_min.insert('end', '20')
_r_max.insert('end', '30')

_g_min.insert('end', '30')
_g_max.insert('end', '50')

nbr_vec.insert('end', '50')
#
btn_reseau = Button(wrapper_setting, text='Creer le réseau', command=creationResau)
btn_sol_in = Button(wrapper_setting, text='Solutions initial', command=creationSolution)
btn_reseau.place(x=5, y=180, width=115, height=40)
btn_sol_in.place(x=125, y=180, width=115, height=40)
lbl_iter = Label(wrapper_setting, text='Nbr. solution initial')
_iter = Entry(wrapper_setting, foreground='black')
lbl_iter.place(x=5, y=240, width=115)
_iter.place(x=125, y=240, width=115)
_iter.insert('end', '50')
# button choice AG & DE
btn_AG = Button(wrapper_choice, text='Lance AG', command=lanceFrameGA)
btn_DE = Button(wrapper_choice, text='Lance DE', command=lanceFrameDE)
btn_cmp = Button(wrapper_choice, text='Comparaison', command=comparison)
btn_AG.place(x=5, y=15, width=115, height=40)
btn_DE.place(x=125, y=15, width=115, height=40)
btn_cmp.place(x=60, y=60, width=115, height=40)
#

comp_g_ = LabelFrame(tab_Comp, text='Compratison les Solution Feux Vert DE & GA')
comp_r_ = LabelFrame(tab_Comp, text='Compratison les Solution Feux Rouge DE & GA')
comp_g_.place(x=10,y=10, width=580, height=190)
comp_r_.place(x=10,y=200, width=580, height=190)
#

wrapper_setting.place(x=5, y=5, width=250, height=300)
wrapper_solutions.place(x=255, y=5, width=600, height=450)
wrapper_choice.place(x=5, y=305, width=250, height=150)


root.geometry("860x460")
# lance tkinter
root.mainloop()
