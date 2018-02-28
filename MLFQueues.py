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
  while(len(priorities[priority]) > 0 and maxSwitch > 0):
    while(len(priorities[priority]) > 0 and maxSwitch > 0 and t-lastReset < RESET_DUR) :
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

    if(t-lastReset >= RESET_DUR):
      lastReset = t
      priority = 0
      resetAllPriorities(priorities)
      priorities = [priorities[0]]
    else:
      priority += 1
      while(len(priorities) <= priority):
        priorities.append([])


  cpuSched += (str(t) + ":END")
  print("\tCPU: " + cpuSched)
  ioSched += (str(io) + ":END")
  print("\tIO: " + ioSched)

  printStats(finishedProcesses, processes)


if __name__ == '__main__':
  infile = open("mlfIn2.txt")

  processes = []
  for line in infile:
    line = line.strip()
    p = Process(line)
    print(p)
    processes.append(p)

  maxSwitch = int(input("How many context switches? "))
  MLF(copy.deepcopy(processes), maxSwitch)

  infile.close()
