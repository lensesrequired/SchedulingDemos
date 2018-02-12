from process import *
import operator
import copy

def FCFS(processes):
  print("FCFS results:")
  print("\t", end = "")
  processes.sort(key = operator.attrgetter('arrivalTime'))

  finishedProcesses = []

  t = 0
  while(len(processes) > 0):
    p = processes.pop(0)

    if(t < p.arrivalTime):
      t = p.arrivalTime
      print(str(t) + ":" + p.name, end = "  ")
    else:
      print(str(t) + ":" + p.name, end = "  ")
    p.stats[1] = t
    t = p.run(t)
    p.stats[2] = t
    print(str(t) + ":END")

  printStats(finishedProcesses)

def RR(processes):
  timeSlice = int(input("Timeslice? "))

  processes.sort(key = operator.attrgetter('arrivalTime'))
  finishedProcesses = []
  print("RR results:")
  print("\t", end = "")

  t = 0
  while(len(processes) > 0):
    p = processes.pop(0)

    if(t < p.arrivalTime):
      t = p.arrivalTime
      print(str(t) + ":" + p.name, end = "  ")
    else:
      print(str(t) + ":" + p.name, end = "  ")

    if(p.new):
      p.stats[1] = t

    t = p.run(t, timeSlice)

    if(p.nextBurst):
      insertByArrival(processes, p)
    else:
      p.stats[2] = t
      finishedProcesses.append(p)

  print(str(t) + ":END")

  printStats(finishedProcesses)

def SJF(processes):
  print("SJF results:")
  print("\t", end = "")

  processes.sort(key = operator.attrgetter('arrivalTime'))
  finishedProcesses = []

  t = 0
  while(len(processes) > 1):
    p = processes.pop(0)
    p2 = processes.pop(0)

    if(t < p.arrivalTime):
      t = p.arrivalTime
      print(str(t) + ":" + p.name, end = "  ")
    else:
      print(str(t) + ":" + p.name, end = "  ")
    if(p.new):
      p.stats[1] = t

    if(p2.arrivalTime < (p.arrivalTime + p.nextBurst) and 
      p2.nextBurst < (p.nextBurst - (p2.arrivalTime-p.arrivalTime))):
      t = p.run(t, p2.arrivalTime-p.arrivalTime)
      insertByArrival(processes, p)
      processes.insert(0, p2)
    else:
      t = p.run(t)
      insertByArrival(processes, p2)
      p.stats[2] = t
      finishedProcesses.append(p)

  p = processes.pop(0)

  if(t < p.arrivalTime):
    t = p.arrivalTime
    print(str(t) + ":" + p.name, end = "  ")
  else:
    print(str(t) + ":" + p.name, end = "  ")
  if(p.new):
    p.stats[1] = t

  t = p.run(t)
  p.stats[2] = t
  finishedProcesses.append(p)

  print(str(t) + ":END")

  printStats(finishedProcesses)


if __name__ == '__main__':
  infile = open("in.txt")

  processes = []
  for line in infile:
    line = line.strip()
    p = Process(line)
    processes.append(p)

  FCFS(copy.deepcopy(processes))
  RR(copy.deepcopy(processes))
  SJF(copy.deepcopy(processes))

  infile.close()