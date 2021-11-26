import random #随机数生成
from collections import deque #队列数据结构

"""
运煤实现：
初始状态：进入装载队列，初始化统计量

变化原因：仿真时钟推进至未来事件表的下一事件

变化：
1.结束装载：将结束装载的火车状态加入称重队列，或仅更新卡车开始称重时间（基于称重排队队列）；

2.结束称重：改变结束称重的火车状态为结束转运；

3.结束转运：改变结束转运的火车状态为结束装载，或仅更新卡车开始装载时间（基于装载排队队列）；

实现方式：一个truck类记录货车状态、三个函数（方法）实现变化；

更新未来事件表
货车更新状态时，更新排队队列
循环1次更新统计量，
"""

Event = {1:'EndLoading',2:'EndWeighing',3:'EndTravel'}
#各类事件概率
LoadingTime = [5,10,15]
LoadingTimeProb = [0.3,0.8,1]
WeighingTime = [12,16]
WeighingTimeProb = [0.7,1]
TravelTime = [40,60,80,100]
TravelTimeProb = [0.4,0.7,0.9,1] 
StopSimulationTime = 1000
#事件发生的时间段(按概率随机确定时间)
def event_time(times,prob):
    num = random.randint(1,10)
    for i,j in enumerate(prob):
        if num<=j*10:
            time = times[i]
            break
    return time
#统计量
T = 0 #卡车停留在系统内的时间
BL = 0 #装载车台总工作事件
BS = 0 #称重台总工作时间
MLQ = 0 #最大装载队长
MWQ = 0 #最大称重队长
#实体集合
LoaderQueue = deque([]) #正在排队装载的卡车，按到达时间排序
ScaleQueue = deque([]) #正在排队称重的卡车，按到达时间排序
#未来事件表
FutureEventList = deque([])
#未来事件表的调整排序
def sort_one(x):
    x = list(x)
    x.sort(key = lambda t: t.time)
    x = deque(x)
    return x
def sort_all():
    global FutureEventList,LoaderQueue,ScaleQueue
    FutureEventList = sort_one(FutureEventList)
#状态变量
Lt = 0 #正在装载的卡车数量 0，1，2
Wt = 0 #正在称重的卡车数量 0，1
max_Loader_num = 2
max_Scale_num = 1

#仿真时钟
Clock = 0
#卡车容器
Truck = [0 for i in range(7)]
#创建truck类
class truck:
    def __init__(self,ID,Time,Event,t):
        self.ID = ID
        self.time = Time #某个状态的时间
        self.event = Event
        self.t = t
#打印报告
def print_report():
    LoaderUtil  = BL/max_Loader_num/StopSimulationTime
    ScaleUtil   = BS/max_Scale_num/StopSimulationTime
    print()
    print('\t六辆卡车转运煤炭 —— 事件调度法')
    print( "\t仿真时长(分钟)      %f\n"%Clock)
    print( "\t装载车工作时间      %f\n"%BL)
    print( "\t装载车利用率        %f\n"%LoaderUtil)
    print( "\t最大装载队长        %d\n"%MLQ )
    print( "\t称重台工作时间      %f\n"%BS )
    print( "\t称重台利用率        %f\n"%ScaleUtil)
    print( "\t最大称重队长        %d\n"%MWQ)
    print( "\t卡车平均停留时间        %f\n"%(T/6))
#更新统计量
def CollectStatistics():
    global MLQ,MWQ
    MLQ = max(MLQ,len(LoaderQueue)) #最大装载队长
    MWQ = max(MWQ,len(ScaleQueue))  #最大称重队长


#结束装载
def endload(ptruck):
    global Lt
    #释放一个装载车
    Lt -= 1
    #更新状态
    ptruck.event = Event[2]
    #进入称重队列
    ScaleQueue.append(ptruck)
    update_fel()
    print('Clock = %d \t完成了对Truck%d 的装载'%(Clock,ptruck.ID))


#结束称重
def endweigh(ptruck):
    global Wt,T
    #称重台空闲
    Wt -= 1
    ##更新状态
    ptruck.event = Event[3]
    ptruck.time = Clock + event_time(TravelTime,TravelTimeProb)
    T += (Clock - ptruck.t)
    #进入转运状态
    FutureEventList.append(ptruck)
    update_fel()
    print('Clock = %d \t完成了对Truck%d 的称重'%(Clock,ptruck.ID))

#结束转运
def endtravel(ptruck):
    #更新状态
    ptruck.event = Event[1]
    ptruck.t = Clock
    #进入装载队列
    LoaderQueue.append(ptruck)
    update_fel()
    print('Clock = %d \t完成了对Truck%d 的转运'%(Clock,ptruck.ID))

#未来事件表的更新
def update_fel():
        global Lt,Wt,BS,BL
        #开始装载
        while Lt<max_Loader_num and len(LoaderQueue)>0:
                truck_0 = LoaderQueue.popleft()#结束排队装载
                Lt += 1
                print('Clock= %d Truck%d  开始装载'%(Clock,truck_0.ID))
                #更新状态
                interval = event_time(LoadingTime,LoadingTimeProb)
                truck_0.time = Clock + interval#结束装载的时间
                BL += interval
                FutureEventList.append(truck_0)
        #开始称重
        while Wt<max_Scale_num and len(ScaleQueue)>0:
                truck_0 = ScaleQueue.popleft()#结束排队称重
                Wt += 1
                print('Clock= %d Truck%d  开始称重'%(Clock,truck_0.ID))
                interval = event_time(WeighingTime,WeighingTimeProb)
                truck_0.time = Clock + interval#结束称重的时间
                BS += interval
                FutureEventList.append(truck_0)

#初始化        
def Initialization():
    global Lt,Wt,MLQ,MWQ,BL,BS,L,LoaderQueue,ScaleQueue,FutureEventList
    #仿真时钟初始化
    Clock = 0
    #统计量初始化
    L = 0
    BL = 0 #装载车台总工作事件
    BS = 0 #称重台总工作时间
    MLQ = 0 #最大装载队长
    MWQ = 0 #最大称重队长
    #集合清空
    LoaderQueue.clear()
    ScaleQueue.clear()
    FutureEventList.clear()

    #第一辆卡车
    Truck[1] = truck(1,Clock+event_time(WeighingTime,WeighingTimeProb),Event[2],Clock)
    FutureEventList.append(Truck[1])
    #称重台占用
    Wt = 1
    #第2辆卡车
    Truck[2] = truck(2,Clock+event_time(LoadingTime,LoadingTimeProb),Event[1],Clock)
    FutureEventList.append(Truck[2])
    #第3辆卡车
    Truck[3] = truck(3,Clock+event_time(LoadingTime,LoadingTimeProb),Event[1],Clock)
    FutureEventList.append(Truck[3])
    #装载车占用
    Lt = 2
    #第4辆卡车
    Truck[4] = truck(4,Clock,Event[1],Clock)
    LoaderQueue.append(Truck[4])
    #第5辆卡车
    Truck[5] = truck(5,Clock,Event[1],Clock)
    LoaderQueue.append(Truck[5])
    #第6辆卡车
    Truck[6] = truck(6,Clock,Event[1],Clock)
    LoaderQueue.append(Truck[6])
    #称重队长
    MWQ=0
    #装载队长
    MLQ=len(LoaderQueue)
    #调整未来事件表
    sort_all()


#主程序（一次仿真）
def main():
    global Clock
    Initialization()
    flag = False
    while(not flag):
        try:
            #FEL移出下一事件
            ptruck = FutureEventList.popleft()
            #仿真时钟推进至下一未来事件
            Clock = ptruck.time
            #执行该事件
            pEvent = ptruck.event
            if pEvent == Event[1]:
                endload(ptruck)
            elif pEvent == Event[2]:
                endweigh(ptruck)
            elif pEvent == Event[3]:
                endtravel(ptruck)
            else:
                flag = True
            if Clock>=StopSimulationTime: flag=True
        except:
            print(FutureEventList)
            print(LoaderQueue)
            print(ScaleQueue)
            break
        #更新统计量
        CollectStatistics()
        #更新未来事件表
        #update_fel()
        #调整未来事件表顺序
        sort_all()
    #打印报告
    print_report()

if __name__ == '__main__':
    main()