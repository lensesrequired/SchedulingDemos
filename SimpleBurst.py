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
    t = p.run(t)
    finishTimes.append(t)
  print(str(t) + ":END")

  turnaroundTimes = [finishTimes[i]-arrivalTimes[i] for i in range(len(arrivalTimes))]
  responseTimes = [startTimes[i]-arrivalTimes[i] for i in range(len(arrivalTimes))]
  print("\tAverage Turnaround Time: " + str(float(sum(turnaroundTimes))/len(arrivalTimes)))
  print("\tAverage Response Time: " + str(float(sum(responseTimes))/len(arrivalTimes)))

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

  turnaroundTimes = [process.stats[2]-process.stats[0] for process in finishedProcesses]
  responseTimes = [process.stats[1]-process.stats[0] for process in finishedProcesses]
  print("\tAverage Turnaround Time: " + str(float(sum(turnaroundTimes))/len(finishedProcesses)))
  print("\tAverage Response Time: " + str(float(sum(responseTimes))/len(finishedProcesses)))

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

  turnaroundTimes = [process.stats[2]-process.stats[0] for process in finishedProcesses]
  responseTimes = [process.stats[1]-process.stats[0] for process in finishedProcesses]
  print("\tAverage Turnaround Time: " + str(float(sum(turnaroundTimes))/len(finishedProcesses)))
  print("\tAverage Response Time: " + str(float(sum(responseTimes))/len(finishedProcesses)))


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