from process import *
import operator
import copy

def FCFS(processes, maxSwitch):
  print("FCFS results:")
  processes.sort(key = operator.attrgetter('arrivalTime'))

  finishedProcesses = []
  cpuSched = ""
  ioSched = ""

  t = 0
  io = 0
  while(len(processes) > 0 and maxSwitch > 0):
    p = processes.pop(0)

    if(t < p.arrivalTime):
      t = p.arrivalTime
      cpuSched += (str(t) + ":" + p.name + "  ")
      maxSwitch -= 1
    else:
      cpuSched += (str(t) + ":" + p.name + "  ")
      maxSwitch -= 1
    if(p.new):
      p.stats[1] = t
    t, ioInfo = p.run(t, io)
    io = ioInfo[0]
    ioSched += ioInfo[1]

    if(p.nextBurst):
      insertByArrival(processes, p)
    else:
      p.stats[2] = t
      finishedProcesses.append(p)

  cpuSched += (str(t) + ":END")
  print("\t" + cpuSched)
  ioSched += (str(io) + ":END")
  print("\t" + ioSched)

  printStats(finishedProcesses)

def RR(processes, maxSwitch):
  timeSlice = int(input("Timeslice? "))
  #timeSlice = 2

  print("RR results:")
  processes.sort(key = operator.attrgetter('arrivalTime'))

  finishedProcesses = []
  cpuSched = ""
  ioSched = ""

  t = 0
  io = 0
  while(len(processes) > 0 and maxSwitch > 0):
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

    if(p.nextBurst):
      insertByArrival(processes, p)
    else:
      p.stats[2] = t
      finishedProcesses.append(p)

  cpuSched += (str(t) + ":END")
  print("\t" + cpuSched)
  ioSched += (str(io) + ":END")
  print("\t" + ioSched)

  printStats(finishedProcesses)

def SJF(processes, maxSwitch):
  print("SJF results:")
  processes.sort(key = operator.attrgetter('arrivalTime'))

  finishedProcesses = []
  cpuSched = ""
  ioSched = ""

  t = 0
  io = 0
  while(len(processes) > 0 and maxSwitch > 0):
    a = processes[0].arrivalTime
    b = processes[0].nextBurst
    p = 0
    jump = 1
    for i, process in enumerate(processes):
      if(process.arrivalTime == a):
        if(process.nextBurst < b):
          b = process.nextBurst
          p = i
      else:
        jump = i
        break

    p = processes.pop(p)
    if(t < p.arrivalTime):
      t = p.arrivalTime
      maxSwitch -= 1
      cpuSched += (str(t) + ":" + p.name + "  ")
    else:
      maxSwitch -= 1
      cpuSched += (str(t) + ":" + p.name + "  ")

    if(p.new):
      p.stats[1] = t

    shorter = False
    for i, process in enumerate(processes[jump-1:]):                      #-1 because pop...
      if(process.arrivalTime < p.arrivalTime + p.nextBurst):
        if(process.nextBurst < p.nextBurst-(process.arrivalTime-p.arrivalTime)):
          shorter  = True
          t, ioInfo = p.run(t, io, process.arrivalTime - p.arrivalTime)
          io = ioInfo[0]
          ioSched += ioInfo[1]

          for proc in processes[0:jump - 1 + i]:
            proc.arrivalTime = process.arrivalTime
          insertByArrival(processes, p)
          break
      else:
        break

    if(not shorter):
      t, ioInfo = p.run(t, io)
      io = ioInfo[0]
      ioSched += ioInfo[1]

      for process in processes:
        process.arrivalTime = t
      if(p.nextBurst):
        insertByArrival(processes, p)
      else:
        p.stats[2] = t
        finishedProcesses.append(p)
  
  cpuSched += (str(t) + ":END")
  print("\t" + cpuSched)
  ioSched += (str(io) + ":END")
  print("\t" + ioSched)

  printStats(finishedProcesses)


if __name__ == '__main__':
  infile = open("in.txt")

  processes = []
  for line in infile:
    line = line.strip()
    p = Process(line)
    processes.append(p)

  maxSwitch = int(input("How many context switches? "))
  FCFS(copy.deepcopy(processes), maxSwitch)
  RR(copy.deepcopy(processes), maxSwitch)
  SJF(copy.deepcopy(processes), maxSwitch)

  infile.close()
