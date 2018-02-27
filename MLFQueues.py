from process import *
import operator
import copy

global RESET_DUR
RESET_DUR = 7

def MLF(processes, maxSwitch): 
  timeSlice = int(input("Timeslice? "))

  print("Multi-level feedback queue results:")
  processes.sort(key = operator.attrgetter('arrivalTime'))

  finishedProcesses = []
  cpuSched = ""
  ioSched = ""
  priorities = [processes]

  t = 0
  io = 0
  priority = 0
  lastReset = 0
  cpuInfo = [t, cpuSched, lastReset]
  ioInfo = [io, ioSched]
  while(len(priorities[priority]) > 0 and maxSwitch > 0):
    while(len(priorities[priority]) > 0 and maxSwitch > 0 and cpuInfo[0]-lastReset < RESET_DUR) :
      p = priorities[priority].pop(0)

      if(t < p.arrivalTime):
        t = p.arrivalTime
        maxSwitch -= 1
        cpuSched += (str(t) + ":" + p.name + "  ")
      else:
        maxSwitch -= 1
        cpuSched += (str(t) + ":" + p.name + "  ")

      if(p.new):
        p.stats[1] = t

      t, ioInfo = p.run(t, io, timeSlice)
      io = ioInfo[0]
      ioSched += ioInfo[1]

      if(p.nextBurst): 
        while(len(priorities) <= p.priority):
          priorities.append([])
        insertByArrival(priorities[p.priority], p)
      else:   
        p.stats[2] = t
        finishedProcesses.append(p)

    priority += 1
    while(len(priorities) <= priority):
      priorities.append([])

    if(cpuInfo[0]-lastReset < RESET_DUR):
      cpuInfo[2] = cpuInfo[0]
      priority = 0
      resetAllPriorities(priorities)
      priorities = [priorities[0]]

  cpuSched += (str(t) + ":END")
  print("\t" + cpuSched)
  ioSched += (str(io) + ":END")
  print("\t" + ioSched)

  printStats(finishedProcesses, processes)

def RR(processes, mainCpuInfo, mainIoInfo, timeSlice, maxSwitch):
  processes.sort(key = operator.attrgetter('arrivalTime'))

  finishedProcesses = []
  priority = processes[0].priority
  cpuSched = mainCpuInfo[1]
  ioSched = mainIoInfo[1]

  t = mainCpuInfo[0]
  io = mainIoInfo[0]
  while(len(processes) > 0 and maxSwitch > 0 and t-mainCpuInfo[2] < RESET_DUR):
    p = processes.pop(0)

    if(t < p.arrivalTime):
      t = p.arrivalTime
      maxSwitch -= 1
      cpuSched += (str(t) + ":" + p.name + "  ")
    else:
      maxSwitch -= 1
      cpuSched += (str(t) + ":" + p.name + "  ")

    if(p.new):
      p.stats[1] = t

    t, ioInfo = p.run(t, io, timeSlice)
    io = ioInfo[0]
    ioSched += ioInfo[1]

    if(p.nextBurst and p.priority == priority):
      insertByArrival(processes, p)
    else:   
      p.stats[2] = t
      finishedProcesses.append(p)

  mainCpuInfo[0] = t
  mainCpuInfo[1] = cpuSched
  mainIoInfo[0] = io
  mainIoInfo[1] = ioSched
  return finishedProcesses, maxSwitch


if __name__ == '__main__':
  infile = open("in.txt")

  processes = []
  for line in infile:
    line = line.strip()
    p = Process(line)
    processes.append(p)

  maxSwitch = int(input("How many context switches? "))
  MLF(copy.deepcopy(processes), maxSwitch)

  infile.close()
