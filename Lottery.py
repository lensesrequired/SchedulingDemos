from process import *
import operator
import copy
import random

def find_lcm(num1,num2):
    if(num1>num2):
        num=num1
        den=num2
    else:
        num=num2
        den=num1
    rem=num%den
    while(rem!=0):
        num=den
        den=rem
        rem=num%den
    gcd=den
    lcm=int(int(num1*num2)/int(gcd))
    return lcm

def SJFLottery(processes, maxSwitch, alpha, tau_naught):
  print("Lottery results:")
  processes.sort(key = operator.attrgetter('arrivalTime'))

  for p in processes:
    p.approx = tau_naught

  finishedProcesses = []
  cpuSched = ""
  ioSched = ""

  t = 0
  io = 0
  while(len(processes) > 0 and maxSwitch > 0):
    nextProcesses = []
    nextApproxs = []
    a = processes[0].arrivalTime

    end = False
    p = processes.pop(0)
    while(p.arrivalTime == a):
      nextProcesses.append(p)
      nextApproxs.append(p.approx)
      if(len(processes) > 0):
        p = processes.pop(0)
      else:
        end = True
        break
    if not end:
      processes = [p] + processes

    if(len(nextProcesses) > 1):
      num1=nextApproxs[0]
      num2=nextApproxs[1]
      lcm=find_lcm(num1,num2)
       
      for i in range(2,len(nextApproxs)):
        lcm=find_lcm(lcm,nextApproxs[i])
    else:
      lcm = nextApproxs[0]

    lottery = []
    for i,p in enumerate(nextProcesses):
      lottery += [i]*int(lcm/p.approx)

    p = nextProcesses.pop(random.randint(0, len(nextProcesses)-1))
    if(t < p.arrivalTime):
      t = p.arrivalTime
      maxSwitch -= 1
      cpuSched += (str(t) + ":" + p.name + "  ")
    else:
      maxSwitch -= 1
      cpuSched += (str(t) + ":" + p.name + "  ")

    if(p.new):
      p.stats[1] = t

    cutShort = False
    if(len(processes) > 0):
      if(processes[0].arrivalTime < p.arrivalTime + p.nextBurst):
        cutShort = True
        t, ioInfo = p.run(t, io, processes[0].arrivalTime - p.arrivalTime)
        p.calcApprox(alpha)
        io = ioInfo[0]
        ioSched += ioInfo[1]

        insertByArrival(processes, p)

    if(not cutShort):
      t, ioInfo = p.run(t, io)
      p.calcApprox(alpha)
      io = ioInfo[0]
      ioSched += ioInfo[1]

      if(p.nextBurst):
        insertByArrival(processes, p)
      else:
        p.stats[2] = t
        finishedProcesses.append(p)

    for proc in nextProcesses:
      proc.arrivalTime = t

    processes = nextProcesses + processes

  
  cpuSched += (str(t) + ":END")
  print("\t" + cpuSched)
  ioSched += (str(io) + ":END")
  print("\t" + ioSched)

  printStats(finishedProcesses, processes)


if __name__ == '__main__':
  infile = open("in.txt")

  #alpha = float(input("Initial actual burst weight? "))
  #tau_naught = int(input("Initial prediction? "))
  alpha = 0.5
  tau_naught = 2
  processes = []
  for line in infile:
    line = line.strip()
    p = Process(line)
    processes.append(p)
  for p in processes:
    p.approx = tau_naught

  SJFLottery(copy.deepcopy(processes), 20, alpha, tau_naught)

  infile.close()