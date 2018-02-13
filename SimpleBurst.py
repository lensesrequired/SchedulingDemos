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
  while(len(processes) > 0):
    p = processes.pop(0)

    reinsert = False
    pop = 0
    for i, process in enumerate(processes):
      if(p.arrivalTime >= process.arrivalTime and p.nextBurst > process.nextBurst):
        reinsert = p
        pop = i
        p = process
      else:
        if(t < p.arrivalTime):
          t = p.arrivalTime
          print(str(t) + ":" + p.name, end = "  ")
        else:
          print(str(t) + ":" + p.name, end = "  ")

        if(p.new):
          p.stats[1] = t

        if(p.arrivalTime + p.nextBurst > process.arrivalTime):
          if(p.nextBurst-process.arrivalTime > process.nextBurst):
            t = p.run(t, process.arrivalTime - t)
        else:
          t = p.run(t)
          p.stats[2] = t
          finishedProcesses.append(p)
          break

    if(reinsert):
      processes.pop(pop)
      insertByArrival(processes, reinsert)
    if(p.nextBurst):
      insertByArrival(processes, p)

  
  print(str(t) + ":END")

  printStats(finishedProcesses)


if __name__ == '__main__':
  infile = open("in.txt")

  processes = []
  for line in infile:
    line = line.strip()
    p = Process(line)
    processes.append(p)

  #FCFS(copy.deepcopy(processes))
  #RR(copy.deepcopy(processes))
  SJF(copy.deepcopy(processes))

  infile.close()