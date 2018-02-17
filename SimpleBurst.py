from process import *
import operator
import copy

def FCFS(processes):
  print("FCFS results:")
  print("\t", end = "")
  processes.sort(key = operator.attrgetter('arrivalTime'))

  arrivalTimes = []
  startTimes = []
  finishTimes = []

  t = 0
  while(len(processes) > 0):
    p = processes.pop(0)

    arrivalTimes.append(p.arrivalTime)
    if(t < p.arrivalTime):
      t = p.arrivalTime
      print(str(t) + ":" + p.name, end = "  ")
    else:
      print(str(t) + ":" + p.name, end = "  ")
    startTimes.append(t)
    t, ioInfo = p.run(t, 0)
    finishTimes.append(t)
  print(str(t) + ":END")

  turnaroundTimes = [finishTimes[i]-arrivalTimes[i] for i in range(len(arrivalTimes))]
  responseTimes = [startTimes[i]-arrivalTimes[i] for i in range(len(arrivalTimes))]
  print("\tAverage Turnaround Time: " + str(float(sum(turnaroundTimes))/len(arrivalTimes)))
  print("\tAverage Response Time: " + str(float(sum(responseTimes))/len(arrivalTimes)))

def RR(processes):
  timeSlice = int(input("Timeslice? "))
  #timeSlice = 2

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

    t, ioInfo = p.run(t, 0, timeSlice)

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
  while(len(processes) > 0):
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
      print(str(t) + ":" + p.name, end = "  ")
    else:
      print(str(t) + ":" + p.name, end = "  ")

    if(p.new):
      p.stats[1] = t

    shorter = False
    for i, process in enumerate(processes[jump-1:]):                      #-1 because pop...
      if(process.arrivalTime < p.arrivalTime + p.nextBurst):
        if(process.nextBurst < p.nextBurst-(process.arrivalTime-p.arrivalTime)):
          shorter  = True
          t, ioInfo = p.run(t, 0, process.arrivalTime - p.arrivalTime)
          for proc in processes[0:jump - 1 + i]:
            proc.arrivalTime = process.arrivalTime
          insertByArrival(processes, p)
          break
      else:
        break

    if(not shorter):
      t, ioInfo = p.run(t, 0)
      for process in processes:
        process.arrivalTime = t
      p.stats[2] = t
      finishedProcesses.append(p)
  
  print(str(t) + ":END")

  printStats(finishedProcesses)


if __name__ == '__main__':
  infile = open("in2.txt")

  processes = []
  for line in infile:
    line = line.strip()
    p = Process(line)
    processes.append(p)

  FCFS(copy.deepcopy(processes))
  RR(copy.deepcopy(processes))
  SJF(copy.deepcopy(processes))

  infile.close()
