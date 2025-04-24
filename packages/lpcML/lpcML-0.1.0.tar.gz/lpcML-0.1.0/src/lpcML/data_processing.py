from pathlib import Path
from pickle import dump, load
import os
import re

import pandas as pd 
import matplotlib.pyplot as plt
import torch
from torcheval.metrics.functional import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import  StandardScaler, MinMaxScaler


def import_lpc_data(path, delimiter=','):
    '''
    Imports data into a pandas dataFrame from csv
    -------
    Input:
    ------
    path: path
        path where the data is stored
    delimiter: str
        delimiter between columns of csv
    Output:
    -------
    data: pandas dataframe 
        dataframe with data
    '''
    data = pd.read_csv(path, delimiter=delimiter)
    return data

def data_to_input_output_tensors(data, input_param=None, output_param=None, verbosity=False):
    '''Preprocessing function that creates the input and output tensors
    ---------
    Input:
    -----
    data: pd.Dataframe
        hLPC optimization data
    input_param: list
        list of input parameters used to train the neural network, ['C1_up2_thick','C1_up2_dop','C1_down1_thick','C1_down1_dop','wavelength'] by default
    output_param: list
        list of output parameter(s) used to train the neural network, ['Eff'] by default
    verbosity: bool
        Print information about the final scaled tensors
    Output:
    ------
    X_list: torch.tensor
        Input tensor
    Y_list: torch.tensor
        Output tensor
    '''
    if not input_param:
        print('List of input parameters to feed the neural network not defined')
        input_param = ['C1_up2_thick','C1_up2_dop','C1_down1_thick','C1_down1_dop','wavelength']
    if not output_param:
        print('List of output parameter(s) to feed the neural network not defined')
        output_param = ['Eff']
    df_inputs = pd.DataFrame(data, columns=input_param)
    df_outputs = pd.DataFrame(data, columns=output_param)
    X_list, Y_list = df_inputs.to_numpy(), df_outputs.to_numpy()
    if verbosity:
        print("Total dimension (rank)\n","\tInput:", torch.tensor(X_list, dtype=torch.float32).ndim,"\tOutput:",torch.tensor(Y_list, dtype=torch.float32).ndim)
        print("Total size (shape)\n","\tInput:", torch.tensor(X_list, dtype=torch.float32).shape,"\tOutput:",torch.tensor(Y_list, dtype=torch.float32).shape)
        print("Total data type (dtype)\n","\tInput:", torch.tensor(X_list, dtype=torch.float32).dtype,"\tOutput:",torch.tensor(Y_list, dtype=torch.float32).dtype)
    return torch.tensor(X_list, dtype=torch.float32), torch.tensor(Y_list, dtype=torch.float32)


def split_data(X, Y, test_split = 0.2, verbosity=False):
    '''Split data into train, validation and test subsets
    ---------
    Input:
    ------
    X: torch.tensor
        Input tensor
    Y: torch.tensor
        Output tensor
    test_split: float
        Percentage of subsets distribution, 20% test by default
    
    Output:
    -------
    X_train, Y_train: torch.tensor
        Input, Output train subsets
    X_val, Y_val: torch.tensor
        Input, Output validation subsets
    X_test, Y_test: torch.tensor
        Input, Output test subsets
    '''
    X, X_test, Y, Y_test = train_test_split(X, Y, test_size=test_split) 
    X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=test_split)
    if verbosity:
        print("Train size\n","\tInput:", X_train.shape,"\tOutput:",Y_train.shape)
        print("Validation size\n","\tInput:", X_val.shape,"\tOutput:",Y_val.shape)
        print("Test size\n","\tInput:", X_test.shape,"\tOutput:",Y_test.shape)
    return X_train, X_val, X_test, Y_train, Y_val, Y_test


def scale_input(X_train, X_val, X_test, scaler='standard'):
    '''Preprocessing function that normalize the input and output of the neural network and store the scalers
    ---------
    Input:
    -----
    data: pd.Dataframe
        hLPC optimization data
    scaler: str
        Choose the scaler to apply to the data, two options: StandardScaler 'standard' (default) and MinMaxScaler 'minmax'

    Output:
    ------
    X_train: torch.tensor
        Input train tensor
    X_val: torch.tensor
        Input validation tensor
    X_test: torch.tensor
        Input test tensor
    scaler_inputs: object
        Scaler object for inputs, standard by default
    '''
    if scaler == 'standard':
        scaler_inputs = StandardScaler()
    elif scaler == 'minmax':
        scaler_inputs = MinMaxScaler()
    X_train_scaled = scaler_inputs.fit_transform(X_train)
    X_val_scaled = scaler_inputs.transform(X_val)
    X_test_scaled = scaler_inputs.transform(X_test)
    directory =  'scaler_objects/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    dump(scaler_inputs, open(directory+'scaler_inputs.pkl', 'wb'))
    return torch.tensor(X_train_scaled, dtype=torch.float32), torch.tensor(X_val_scaled, dtype=torch.float32), torch.tensor(X_test_scaled, dtype=torch.float32), scaler_inputs

def scale_output(Y_train, Y_val, Y_test, scaler='standard'):
    '''Preprocessing function that normalize the input and output of the neural network and store the scalers
    ---------
    Input:
    -----
    data: pd.Dataframe
        hLPC optimization data
    scaler: str
        Choose the scaler to apply to the data, two options: StandardScaler 'standard' (default) and MinMaxScaler 'minmax'
    Output:
    ------
    Y_train: torch.tensor
        Output tensor
    Y_val: torch.tensor
        Output tensor
    Y_test: torch.tensor
        Output tensor
    scaler_outputs: object
        Scaler object for outputs, standard by default
    '''
    if scaler == 'standard':
        scaler_output = StandardScaler()
    elif scaler == 'minmax':
        scaler_output = MinMaxScaler()
    Y_train_scaled = scaler_output.fit_transform(Y_train)
    Y_val_scaled = scaler_output.transform(Y_val)
    Y_test_scaled = scaler_output.transform(Y_test)
    directory =  'scaler_objects/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    dump(scaler_output, open(directory+'scaler_output.pkl', 'wb'))
    return torch.tensor(Y_train_scaled, dtype=torch.float32), torch.tensor(Y_val_scaled, dtype=torch.float32), torch.tensor(Y_test_scaled, dtype=torch.float32), scaler_output

def scale_load(path):
    return load(open(path, 'rb'))

def prediction_versus_simulation_plot(simulation, prediction, r2, xlabel = None, ylabel = None, rms = None, storepath = None, figname = None):
    '''Plot for the comparison of the simulated versus predicted data with machine learning
    --------------------
    Parameters:
    ------
    simulation: list or torch.tensor
        Simulated data
    prediction: list or torch.tensor
        Predicted data
    r2: float
        Coefficient of determination between simulated and predicted data
    xlabel: str
        Text for the xlabel
    ylabel: str
        Text fot the ylabel
    rms: list 
        Root mean square errors in the prediction of each value
    storepath: str
        Path to store the plot, by default is stored in the execution directory
    figname: str
        File name of the stored plot, by default is prediction_vs_simulation.pdf
    '''
    fig, ax = plt.subplots()
    if rms:
        rms = mean_squared_error(simulation, prediction)**0.5
        plt.errorbar(simulation, prediction, fmt='.', yerr=rms, label='RMSE')
    else:
        plt.plot(simulation, prediction,'.',color='darkorange',markersize=15,alpha=0.8)
    plt.xlabel(xlabel,fontsize=20)
    plt.ylabel(ylabel,fontsize=20)
    plt.plot(simulation, simulation,'-', color='darkgrey')
    textstr0 = rf'$R^2$={r2}'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.3)
    plt.text(x=0.1,y=0.8, s=textstr0, transform=ax.transAxes, fontsize=20,
        verticalalignment='top', bbox=props)
    plt.locator_params(axis='x', nbins=6)
    plt.locator_params(axis='y', nbins=6)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    if figname:
        plt.savefig(figname, bbox_inches='tight')

def ml_input_versus_output_plot(X_train, X_val, X_test, Y_train, Y_val, Y_test, input_params_name, output_params_name, figname = None):
    '''Plot the simulated data that is used as input for the machine learning vs the output
    --------------------
    Parameters:
    ------
    data: pd.Dataframe
        hLPC optimization data
    input_params_name: list
        List of text for the input parameters
    output_params_name: list
        List of text for the output parameter
    figname: str
        File name of the stored plot
    '''

    FONT = 16
    LFONT = 14
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    plt.subplots_adjust(hspace=0.25, wspace=0.05)
    axs[0, 0].scatter(X_train[:,0]*1000, Y_train, color='blue', label='Train')
    axs[0, 0].scatter(X_val[:,0]*1000+2, Y_val, color='red', label='Validation')
    axs[0, 0].scatter(X_test[:,0]*1000+4, Y_test, color='green', label='Test')
    axs[0, 0].set_xlabel(input_params_name[0], fontsize = FONT)
    axs[0, 0].set_ylabel(output_params_name[0], fontsize = FONT)
    axs[0, 0].tick_params(axis="x", labelsize = LFONT)
    axs[0, 0].tick_params(axis="y", labelsize = LFONT)
    # axs[0, 0].legend()
    axs[1, 0].scatter(X_train[:,1], Y_train, color='blue', label='Train')
    axs[1, 0].scatter(X_val[:,1], Y_val, color='red', label='Validation')
    axs[1, 0].scatter(X_test[:,1], Y_test, color='green', label='Test')
    axs[1, 0].set_xscale('log')
    axs[1, 0].set_xlabel(input_params_name[1], fontsize = FONT)
    axs[1, 0].set_ylabel(output_params_name[0], fontsize = FONT)
    axs[1, 0].tick_params(axis="x", labelsize = LFONT)
    axs[1, 0].tick_params(axis="y", labelsize = LFONT)
    axs[1, 0].legend(fontsize = LFONT)
    axs[0, 1].scatter(X_train[:,2]*1000, Y_train, color='blue', label='Train')
    axs[0, 1].scatter(X_val[:,2]*1000+20, Y_val, color='red', label='Validation')
    axs[0, 1].scatter(X_test[:,2]*1000+40, Y_test, color='green', label='Test')
    axs[0, 1].set_xlabel(input_params_name[2], fontsize = FONT)
    axs[0, 1].tick_params(axis="x", labelsize = LFONT)
    axs[0, 1].tick_params(labelleft=False)
    #axs[0, 1].legend()
    axs[1, 1].scatter(X_train[:,3], Y_train, color='blue', label='Train')
    axs[1, 1].scatter(X_val[:,3], Y_val, color='red', label='Validation')
    axs[1, 1].scatter(X_test[:,3], Y_test, color='green', label='Test')
    axs[1, 1].set_xscale('log')
    axs[1, 1].set_xlabel(input_params_name[3], fontsize = FONT)
    axs[1, 1].tick_params(axis="x", labelsize = LFONT)
    axs[1, 1].tick_params(labelleft=False)
    #axs[1, 1].legend()
    if figname is not None:
        plt.savefig(figname, bbox_inches='tight')

def prediction_versus_simulation_plot_colored(simulation, prediction, X_test, r2, xlabel = None, ylabel = None, input_params = None, input_params_name = None, figname = None):
    '''Plot for the comparison of the simulated versus predicted data with machine learning, subplots for each input parameter
    --------------------
    Parameters:
    ------
    simulation: list or torch.tensor
        Simulated data
    prediction: list or torch.tensor
        Predicted data
    X_test: torch.tensor
        Input test tensor
    r2: float
        Coefficient of determination between simulated and predicted data
    xlabel: str
        Text for the xlabel
    ylabel: str
        Text fot the ylabel
    input_params: list 
        List of identifiers for the input parameters
    input_params_name: list
        List of input parameter names with units
    figname: str
        File name of the stored plot
    '''

    for i in range(len(input_params)):
        fig, ax = plt.subplots()
        plt.xlabel(xlabel,fontsize=20)
        plt.ylabel(ylabel,fontsize=20)

        plt.plot(simulation, simulation,'-', color='darkgrey')

        plt.title(f'Dependent of {input_params_name[i]}', fontsize=20)

        x_diffent = sorted(set(X_test[:,i].tolist()))
        color_list = ['blue','green','red','purple','orange','brown','pink','gray','olive','cyan']
        for f_x_i,_ in enumerate(x_diffent):
            filter = X_test[:,i] == x_diffent[f_x_i]

            simulation_filter = simulation[filter]
            prediction_filter = prediction[filter]

            if 'cm' in input_params_name[i]:
                plt.plot(simulation_filter, prediction_filter,'.',color=color_list[f_x_i],markersize=15,alpha=0.8, label=re.sub(r'e\+?([-\d]+)', r'$\\times$10$^{{\1}}$', f'{x_diffent[f_x_i]:.0e} cm$^{{-3}}$'))
            else:
                plt.plot(simulation_filter, prediction_filter,'.',color=color_list[f_x_i],markersize=15,alpha=0.8, label=f'{1000*x_diffent[f_x_i]:3.0f} nm')


        legend = plt.legend(fontsize=10, title=f'R$^2$={r2}')
        legend.get_title().set_fontweight('bold')  # Set the title font to bold
        plt.locator_params(axis='x', nbins=6)
        plt.locator_params(axis='y', nbins=6)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        if figname is not None:
            figname2 = figname + str(i) + '.png'
            plt.savefig(figname2, bbox_inches='tight')

def prediction_versus_simulation_subplot_colored(simulation, prediction, X_test, r2, xlabel = None, ylabel = None, input_params = None, input_params_name = None, figname = None):
    '''Plot for the comparison of the simulated versus predicted data with machine learning, subplots for each input parameter
    --------------------
    Parameters:
    ------
    simulation: list or torch.tensor
        Simulated data
    prediction: list or torch.tensor
        Predicted data
    X_test: torch.tensor
        Input test tensor
    r2: float
        Coefficient of determination between simulated and predicted data
    xlabel: str
        Text for the xlabel
    ylabel: str
        Text fot the ylabel
    input_params: list 
        List of identifiers for the input parameters
    input_params_name: list
        List of input parameter names with units
    figname: str
        File name of the stored plot
    '''

    FONT = 16
    LFONT = 14
    color_list = ['blue','green','red','purple','orange','brown','pink','gray','olive','cyan']

    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    fig.subplots_adjust(hspace=0)
    fig.subplots_adjust(wspace=0)

    # top left
    axs[0, 0].plot(simulation[:,0].tolist(), simulation[:,0].tolist(),'-', color='darkgrey')
    axs[0, 0].tick_params(labelbottom=False)

    i = 0
    x_diffent = sorted(set(X_test[:,i].tolist()))
    for f_x_i,_ in enumerate(x_diffent):
        filter = X_test[:,i] == x_diffent[f_x_i]

        simulation_filter = simulation[filter]
        prediction_filter = prediction[filter]

        axs[0, 0].plot(simulation_filter, prediction_filter,'.',color=color_list[f_x_i],markersize=15,alpha=0.8, label=f'{1000*x_diffent[f_x_i]:3.0f} nm')

    # axs[0, 0].legend(fontsize=10, title=f'R$^2$={r2}', title_fontproperties={'weight':'bold'})
    legend = axs[0, 0].legend(fontsize=10, title=f'{input_params_name[i]}', ncols=2)
    legend.get_title().set_fontweight('bold')
    axs[0, 0].locator_params(axis='x', nbins=6)
    axs[0, 0].locator_params(axis='y', nbins=6)
    # axs[0, 0].set_xlabel(xlabel, fontsize = FONT)
    axs[0, 0].set_ylabel(ylabel, fontsize = FONT)
    # axs[0, 0].tick_params(axis="x", labelsize = LFONT)
    axs[0, 0].tick_params(axis="y", labelsize = LFONT)

    # bottom left
    axs[1, 0].plot(simulation[:,0].tolist(), simulation[:,0].tolist(),'-', color='darkgrey')

    i = 1
    x_diffent = sorted(set(X_test[:,i].tolist()))
    for f_x_i,_ in enumerate(x_diffent):
        filter = X_test[:,i] == x_diffent[f_x_i]

        simulation_filter = simulation[filter]
        prediction_filter = prediction[filter]

        axs[1, 0].plot(simulation_filter, prediction_filter,'.',color=color_list[f_x_i],markersize=15,alpha=0.8, label=re.sub(r'e\+?([-\d]+)', r'$\\times$10$^{{\1}}$', f'{x_diffent[f_x_i]:.0e} cm$^{{-3}}$'))

    # axs[1, 0].legend(fontsize=10, title=f'R$^2$={r2}', title_fontproperties={'weight':'bold'})
    legend = axs[1, 0].legend(fontsize=10, title=f'{input_params_name[i]}', ncols=2)
    legend.get_title().set_fontweight('bold')
    axs[1, 0].locator_params(axis='x', nbins=6)
    axs[1, 0].locator_params(axis='y', nbins=6)
    axs[1, 0].set_xlabel(xlabel, fontsize = FONT)
    axs[1, 0].set_ylabel(ylabel, fontsize = FONT)
    axs[1, 0].tick_params(axis="x", labelsize = LFONT)
    axs[1, 0].tick_params(axis="y", labelsize = LFONT)

    # top right
    axs[0, 1].plot(simulation[:,0].tolist(), simulation[:,0].tolist(),'-', color='darkgrey')
    axs[0, 1].tick_params(labelleft=False)

    i = 2
    x_diffent = sorted(set(X_test[:,i].tolist()))
    for f_x_i,_ in enumerate(x_diffent):
        filter = X_test[:,i] == x_diffent[f_x_i]

        simulation_filter = simulation[filter]
        prediction_filter = prediction[filter]

        axs[0, 1].plot(simulation_filter, prediction_filter,'.',color=color_list[f_x_i],markersize=15,alpha=0.8, label=f'{1000*x_diffent[f_x_i]:3.0f} nm')

    # axs[0, 1].legend(fontsize=10, title=f'R$^2$={r2}', title_fontproperties={'weight':'bold'})
    legend = axs[0, 1].legend(fontsize=10, title=f'{input_params_name[i]}', ncols=2)
    legend.get_title().set_fontweight('bold')    
    axs[0, 1].locator_params(axis='x', nbins=6)
    axs[0, 1].locator_params(axis='y', nbins=6)
    # axs[0, 1].set_xlabel(xlabel, fontsize = FONT)
    # axs[0, 1].set_ylabel(ylabel, fontsize = FONT)
    # axs[0, 1].tick_params(axis="x", labelsize = LFONT)
    # axs[0, 1].tick_params(axis="y", labelsize = LFONT)

    # bottom right
    axs[1, 1].plot(simulation[:,0].tolist(), simulation[:,0].tolist(),'-', color='darkgrey')
    axs[1, 1].tick_params(labelleft=False)

    i = 3
    x_diffent = sorted(set(X_test[:,i].tolist()))
    for f_x_i,_ in enumerate(x_diffent):
        filter = X_test[:,i] == x_diffent[f_x_i]

        simulation_filter = simulation[filter]
        prediction_filter = prediction[filter]

        axs[1, 1].plot(simulation_filter, prediction_filter,'.',color=color_list[f_x_i],markersize=15,alpha=0.8, label=re.sub(r'e\+?([-\d]+)', r'$\\times$10$^{{\1}}$', f'{x_diffent[f_x_i]:.0e} cm$^{{-3}}$'))

    # axs[1, 1].legend(fontsize=10, title=f'R$^2$={r2}', title_fontproperties={'weight':'bold'})
    legend = axs[1, 1].legend(fontsize=10, title=f'{input_params_name[i]}', ncols=2)
    legend.get_title().set_fontweight('bold')
    axs[1, 1].locator_params(axis='x', nbins=6)
    axs[1, 1].locator_params(axis='y', nbins=6)
    axs[1, 1].set_xlabel(xlabel, fontsize = FONT)
    # axs[1, 1].set_ylabel(ylabel, fontsize = FONT)
    axs[1, 1].tick_params(axis="x", labelsize = LFONT)
    # axs[1, 1].tick_params(axis="y", labelsize = LFONT)
    if figname:
        plt.savefig(figname, bbox_inches='tight')

    
# import re

# simulation = simulated_values
# prediction = predicted_values
# r2 = round(r2_test,3)


# for i in range(len(INPUT_PARAMS)):
#     out_filename_2 = '/home/daniel/research/0_CDE/images/precision/2e4/Voc/SimPred_ML_hLPC_GaN_300K_1W_MIERDA_DE_ENRIQUE_' + str(i) + '.png'

#     xlabel = OUTPUT_PARAMS_NAME2[0]
#     ylabel = OUTPUT_PARAMS_NAME2[1]
#     figname = out_filename_2

#     fig, ax = plt.subplots()
#     # plt.plot(simulation, prediction,'.',color='darkorange',markersize=15,alpha=0.8)
#     plt.xlabel(xlabel,fontsize=20)
#     plt.ylabel(ylabel,fontsize=20)

#     plt.plot(simulation, simulation,'-', color='darkgrey')

#     plt.title(f'Dependent of {INPUT_PARAMS_NAME[i]}', fontsize=20)

#     x_diffent = sorted(set(X_test[:,i].tolist()))
#     color_list = ['blue','green','red','purple','orange','brown','pink','gray','olive','cyan']
#     for f_x_i,_ in enumerate(x_diffent):
#         filter = X_test[:,i] == x_diffent[f_x_i]

#         simulation_filter = simulation[filter]
#         prediction_filter = prediction[filter]

#         if 'cm' in INPUT_PARAMS_NAME[i]:
#             plt.plot(simulation_filter, prediction_filter,'.',color=color_list[f_x_i],markersize=15,alpha=0.8, label=re.sub(r'e\+?([-\d]+)', r'$\\times$10$^{{\1}}$', f'{x_diffent[f_x_i]:.0e} cm$^{{-3}}$'))
#         else:
#             plt.plot(simulation_filter, prediction_filter,'.',color=color_list[f_x_i],markersize=15,alpha=0.8, label=f'{1000*x_diffent[f_x_i]:3.0f} nm')



#     plt.legend(fontsize=10, title=f'R$^2$={r2}', title_fontproperties={'weight':'bold'})
#     # textstr0 = rf'$R^2$={r2}'
#     # props = dict(boxstyle='round', facecolor='wheat', alpha=0.3)
#     # plt.text(s=textstr0, transform=ax.transAxes, fontsize=20, bbox=props)
#     plt.locator_params(axis='x', nbins=6)
#     plt.locator_params(axis='y', nbins=6)
#     plt.xticks(fontsize=20)
#     plt.yticks(fontsize=20)
#     plt.savefig(figname, bbox_inches='tight')
#     plt.close()