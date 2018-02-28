from process import *
import operator
import copy

def SJFApprox(processes, maxSwitch, alpha, tau_naught):
  print("Aproximation results:")
  processes.sort(key = operator.attrgetter('arrivalTime'))

  for p in processes:
    print(p)
    p.approx = tau_naught

  finishedProcesses = []
  cpuSched = ""
  ioSched = ""

  t = 0
  io = 0
  while(len(processes) > 0 and maxSwitch > 0):
    a = processes[0].arrivalTime
    b = processes[0].approx
    p = 0
    jump = 1
    for i, process in enumerate(processes):
      print(process)
      if(process.arrivalTime == a):
        if(process.approx < b):
          b = process.approx
          p = i
      else:
        jump = i
        break

    p = processes.pop(p)
    print("before", p)
    if(t < p.arrivalTime):
      t = p.arrivalTime
      maxSwitch -= 1
      cpuSched += (str(t) + ":" + p.name + "  ")
    else:
      maxSwitch -= 1
      cpuSched += (str(t) + ":" + p.name + "  ")
    print("after", p)

    if(p.new):
      print(p.name)
      print(p.arrivalTime)
      print(t)
      p.stats[1] = t

    shorter = False
    for i, process in enumerate(processes[jump-1:]):                      #-1 because pop...
      if(process.arrivalTime < p.arrivalTime + p.nextBurst):
        if(process.nextBurst < p.nextBurst-(process.arrivalTime-p.arrivalTime)):
          shorter  = True
          print("Run", p.name)
          t, ioInfo = p.run(t, io, process.arrivalTime - p.arrivalTime)
          p.calcApprox(alpha)
          io = ioInfo[0]
          ioSched += ioInfo[1]

          for proc in processes[0:jump - 1 + i]:
            print("CHANGE!")
            proc.arrivalTime = process.arrivalTime
          insertByArrival(processes, p)
          break
      else:
        break

    if(not shorter):
      t, ioInfo = p.run(t, io)
      p.calcApprox(alpha)
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

  printStats(finishedProcesses, processes)


if __name__ == '__main__':
  infile = open("in.txt")

  alpha = float(input("Initial actual burst weight? "))
  tau_naught = int(input("Initial prediction? "))
  processes = []
  for line in infile:
    line = line.strip()
    p = Process(line)
    processes.append(p)

  SJFApprox(copy.deepcopy(processes), 20, alpha, tau_naught)

  infile.close()