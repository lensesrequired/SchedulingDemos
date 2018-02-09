from process import *
import operator

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
  print("RR results:")
  print("\t", end = "")

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


def SJF(processes):
  processes.sort(key = operator.attrgetter('nextBurst'))
  for p in processes:
    print(p.name)


if __name__ == '__main__':
  infile = open("in.txt")

  processes = []
  for line in infile:
    line = line.strip()
    p = Process(line)
    processes.append(p)

  FCFS(processes)
  #SJF(processes)

  infile.close()