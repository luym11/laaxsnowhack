import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# read the raw data
nils_data = pd.read_csv('./data0406.csv', delimiter=',')
nils_data = nils_data.rename(index=str, columns={"time_received_debug": "time"})
nils_data['time']=pd.to_datetime(nils_data['time'])

# time difference correction 1:15 slower for data
nils_data['time']=nils_data['time'] + pd.Timedelta('00:01:15')


# moving average filter
nils_data['acc_x_mov']=nils_data['acc_x'].rolling(window=100).mean()
nils_data['acc_y_mov']=nils_data['acc_y'].rolling(window=100).mean()
nils_data['acc_z_mov']=nils_data['acc_z'].rolling(window=100).mean()
nils_data['gyro_x_mov']=nils_data['gyro_x'].rolling(window=100).mean()
nils_data['gyro_y_mov']=nils_data['gyro_y'].rolling(window=100).mean()
nils_data['gyro_z_mov']=nils_data['gyro_z'].rolling(window=100).mean()

def get_second(ser):
    return ser.second

# basic plot function
def plot_ts_graph_original(df=[], s='00:00:00',f='23:59:59',cols=['x', 'y']):
    startTime = pd.to_datetime('2019-04-07 '+ s)
    finishTime = pd.to_datetime('2019-04-07 '+ f)
    df = df[ (df['time'] > startTime) & (df['time'] < finishTime) ]
    df = df.sort_values(by=['sample_ctr'])
    # firstMs = int(df['time_received_ms'][0])
    # df['new_time'] = df['time'].apply(get_second) + (df['time_received_ms'].apply(int)-firstMs) * 0.001
    firstCTR = int(df['sample_ctr'][0])
    df['new_time'] = df['time'].apply(get_second)[0] + (df['sample_ctr'].apply(int)-firstCTR) * 1/200
    x = df[cols[0]]
    y = df[cols[1]]
    plt.plot(x,y)
    plt.legend()
    plt.show()

# plot function called by function plot_comparisons
def plot_ts_graph(df=[], s='00:00:00',f='23:59:59',cols=['x', 'y']):
    startTime = pd.to_datetime('2019-04-07 '+ s)
    finishTime = pd.to_datetime('2019-04-07 '+ f)
    df = df[ (df['time'] > startTime) & (df['time'] < finishTime) ]
    df = df.sort_values(by=['sample_ctr'])
    df['acc_x_mov']=df['acc_x'].rolling(window=5).mean()
    df['acc_y_mov']=df['acc_y'].rolling(window=5).mean()
    df['acc_z_mov']=df['acc_z'].rolling(window=5).mean()
    df['gyro_x_mov']=df['gyro_x'].rolling(window=5).mean()
    df['gyro_y_mov']=df['gyro_y'].rolling(window=5).mean()
    df['gyro_z_mov']=df['gyro_z'].rolling(window=5).mean()
    # firstMs = int(df['time_received_ms'][0])
    # df['new_time'] = df['time'].apply(get_second) + (df['time_received_ms'].apply(int)-firstMs) * 0.001
    firstCTR = int(df['sample_ctr'][0])
    df['new_time'] = df['time'].apply(get_second)[0] + (df['sample_ctr'].apply(int)-firstCTR) * 1/200
    x = df[cols[0]]
    y = df[cols[1]]
    plt.plot(x,y)
    plt.legend()
    # plt.show()

# all data on a plot
def plot_all_ts_graphs(df=[], s='00:00:00',f='23:59:59',opts=None):
    startTime = pd.to_datetime('2019-04-07 '+ s)
    finishTime = pd.to_datetime('2019-04-07 '+ f)
    f = df[ (df['time'] > startTime) & (df['time'] < finishTime) ]
    df = df.sort_values(by=['sample_ctr'])
    # firstMs = int(df['time_received_ms'][0])
    # df['new_time'] = df['time'].apply(get_second) + (df['time_received_ms'].apply(int)-firstMs) * 0.001
    firstCTR = int(df['sample_ctr'][0])
    df['new_time'] = df['time'].apply(get_second)[0] + (df['sample_ctr'].apply(int)-firstCTR) * 1/200

    t = df['new_time']
    acc_x = df['acc_x_mov']
    acc_y =  df['acc_y_mov']
    acc_z =  df['acc_z_mov']
    gyro_x = df['gyro_x_mov']
    gyro_z = df['gyro_z_mov']
    gyro_y = df['gyro_y_mov']
    #baro = df['baro']

    plt.clf()
    plt.plot(t,acc_x)
    plt.plot(t,acc_y)
    plt.plot(t,acc_z)
    plt.plot(t,gyro_x)
    plt.plot(t,gyro_y)
    plt.plot(t,gyro_z)
    #plt.plot(t,baro)
    plt.legend()

    plt.show()

# all data in separate plots
def plot_comparisons(df=[],s='00:00:00',f='23:59:59'):
    fig = plt.figure()
    plt.subplot(2, 3, 1)
    plot_ts_graph(nils_data,s,f,cols=['new_time','acc_x_mov'])
    plt.subplot(2, 3, 2)
    plot_ts_graph(nils_data,s,f,cols=['new_time','acc_y_mov'])
    plt.subplot(2, 3, 3)
    plot_ts_graph(nils_data,s,f,cols=['new_time','acc_z_mov'])
    plt.subplot(2, 3, 4)
    plot_ts_graph(nils_data,s,f,cols=['new_time','gyro_x_mov'])
    plt.subplot(2, 3, 5)
    plot_ts_graph(nils_data,s,f,cols=['new_time','gyro_y_mov'])
    plt.subplot(2, 3, 6)
    plot_ts_graph(nils_data,s,f,cols=['new_time','gyro_z_mov'])
    # plt.subplot(3, 3, 7)
    # plot_ts_graph(nils_data,s,f,cols=['acc_x_mov','acc_y_mov'])
    # plt.subplot(3, 3, 8)
    # plot_ts_graph(nils_data,s,f,cols=['acc_x_mov','acc_z_mov'])
    # plt.subplot(3, 3, 9)
    # plot_ts_graph(nils_data,s,f,cols=['gyro_x_mov','gyro_z_mov'])

    # plt.show()
    fig.savefig('plot_comparisons.jpeg',dpi=600)

# save all data in separate plots
def plot_comparisons_saveall(df=[],s='00:00:00',f='23:59:59'):
    fig = plt.figure()
    plot_ts_graph(nils_data,s,f,cols=['new_time','acc_x_mov'])
    fig.savefig('plot_comparisons_acc_x.jpeg',dpi=600)
    fig = plt.figure()
    plot_ts_graph(nils_data,s,f,cols=['new_time','acc_y_mov'])
    fig.savefig('plot_comparisons_acc_y.jpeg',dpi=600)
    fig = plt.figure()
    plot_ts_graph(nils_data,s,f,cols=['new_time','acc_z_mov'])
    fig.savefig('plot_comparisons_acc_z.jpeg',dpi=600)
    fig = plt.figure()
    plot_ts_graph(nils_data,s,f,cols=['new_time','gyro_x_mov'])
    fig.savefig('plot_comparisons_gyro_x.jpeg',dpi=600)
    fig = plt.figure()
    plot_ts_graph(nils_data,s,f,cols=['new_time','gyro_y_mov'])
    fig.savefig('plot_comparisons_gyro_y.jpeg',dpi=600)
    fig = plt.figure()
    plot_ts_graph(nils_data,s,f,cols=['new_time','gyro_z_mov'])
    fig.savefig('plot_comparisons_gyro_z.jpeg',dpi=600)