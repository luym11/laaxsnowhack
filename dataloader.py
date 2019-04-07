import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# read the raw data
nils_data = pd.read_csv('./data0406.csv', delimiter=',')
nils_data = nils_data.rename(index=str, columns={"time_received_debug": "time"})
nils_data['time']=pd.to_datetime(nils_data['time'])
# time difference correction 1:15 slower for data
nils_data['time']=nils_data['time'] + pd.Timedelta('00:01:15')


# moving average
nils_data['acc_x_mov']=nils_data['acc_x'].rolling(window=100).mean()
nils_data['acc_y_mov']=nils_data['acc_y'].rolling(window=100).mean()
nils_data['acc_z_mov']=nils_data['acc_z'].rolling(window=100).mean()
nils_data['gyro_x_mov']=nils_data['gyro_x'].rolling(window=100).mean()
nils_data['gyro_y_mov']=nils_data['gyro_y'].rolling(window=100).mean()
nils_data['gyro_z_mov']=nils_data['gyro_z'].rolling(window=100).mean()

# maybe LPF
# round the acc and gyro to 3 decimal digits
# rounded_nils_data=nils_data.round({"acc_x":3,"acc_y":3,"acc_z":3, "gyro_x":3,"gyro_y":3,"gyro_z":3})

# mean analysis
# nils_data.mean(0)



def get_second(ser):
    return ser.second

# plot function
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

def plot_ts_graph(df=[], s='00:00:00',f='23:59:59',cols=['x', 'y']):
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
    # plt.show()

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

def plot_comparisons(df=[],s='00:00:00',f='23:59:59'):
    fig = plt.figure()
    plt.subplot(3, 3, 1)
    plot_ts_graph(nils_data,s,f,cols=['new_time','acc_x_mov'])
    plt.subplot(3, 3, 2)
    plot_ts_graph(nils_data,s,f,cols=['new_time','acc_y_mov'])
    plt.subplot(3, 3, 3)
    plot_ts_graph(nils_data,s,f,cols=['new_time','acc_z_mov'])
    plt.subplot(3, 3, 4)
    plot_ts_graph(nils_data,s,f,cols=['new_time','gyro_x_mov'])
    plt.subplot(3, 3, 5)
    plot_ts_graph(nils_data,s,f,cols=['new_time','gyro_y_mov'])
    plt.subplot(3, 3, 6)
    plot_ts_graph(nils_data,s,f,cols=['new_time','gyro_z_mov'])
    plt.subplot(3, 3, 7)
    plot_ts_graph(nils_data,s,f,cols=['acc_x_mov','acc_y_mov'])
    plt.subplot(3, 3, 8)
    plot_ts_graph(nils_data,s,f,cols=['acc_x_mov','acc_z_mov'])
    plt.subplot(3, 3, 9)
    plot_ts_graph(nils_data,s,f,cols=['gyro_x_mov','gyro_z_mov'])
    plt.show()

# TODO
# histo analysis
# round_acc_x = rounded_nils_data['acc_x']
# draw histogram
# ax=round_acc_x.plot.hist(grid=True, bins=20, rwidth=0.9, color='#607c8e')
# plt.show()