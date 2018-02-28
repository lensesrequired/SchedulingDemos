from SimpleBurst import *
from ComplexBurst import *
from Lottery import *
from Approximation import *
from MLFQueues import *

import copy

def simpleBurstDemo():
  print("Example of FCFS superior turn around time:")
  infile1 = open("simpleIn1.txt")
  processes1 = []
  print("Here are out processes:")
  for line in infile1:
    line = line.strip()
    print(line)
    p = Process(line)
    processes1.append(p)

  FCFS(copy.deepcopy(processes1))
  RR(copy.deepcopy(processes1))
  infile1.close()

  print("\n==============================================================\n")
  print("Example of RR superior turn around time:")
  infile2 = open("simpleIn2.txt")
  print("Here are out processes:")
  processes2 = []
  for line in infile2:
    line = line.strip()
    print(line)
    p = Process(line)
    processes2.append(p)

  FCFS(copy.deepcopy(processes2))
  RR(copy.deepcopy(processes2))
  infile2.close()

  print("\n==============================================================\n")
  print("Example of SJF superior turn around time:")
  SJF(copy.deepcopy(processes1))
  SJF(copy.deepcopy(processes2))

def complexBurstDemo():
  print("SJF is a pre-emptive algorithm:")
  maxSwitch = int(input("How many context switches? "))
  infile1 = open("complexIn1.txt")
  processes1 = []
  print("Processes:")
  for line in infile1:
    line = line.strip()
    print(line)
    p = Process(line)
    processes1.append(p)

  SJFComplex(copy.deepcopy(processes1), maxSwitch)
  infile1.close()

  print("\n==============================================================\n")
  print("Starvation Example:")
  maxSwitch = int(input("How many context switches? "))
  infile2 = open("complexIn2.txt")
  processes2 = []
  print("Processes:")
  for line in infile2:
    line = line.strip()
    print(line)
    p = Process(line)
    processes2.append(p)

  SJFComplex(copy.deepcopy(processes2), maxSwitch)
  infile2.close()

  print("\n==============================================================\n")
  print("FCFS and RR don't starve:")
  FCFSComplex(copy.deepcopy(processes2), maxSwitch)
  RRComplex(copy.deepcopy(processes2), maxSwitch)

def approxDemo():
  print("Various alpha and initial taus:")
  maxSwitch = int(input("How many context switches? "))
  infile1 = open("approxIn1.txt")
  processes1 = []
  print("Processes:")
  for line in infile1:
    line = line.strip()
    print(line)
    p = Process(line)
    processes1.append(p)
  infile1.close()

  # alpha = float(input("Initial actual burst weight? "))
  # tau = int(input("Initial prediction? "))
  # alpha = 0.8
  # tau = 1
  # print("Actual burst weight?", alpha)
  # print("Initial prediction?", tau)
  # SJFApprox(copy.deepcopy(processes1), maxSwitch, alpha, tau)

  # print()
  # alpha = 0.2
  # tau = 1
  # print("IActual burst weight?", alpha)
  # print("Initial prediction?", tau)
  # SJFApprox(copy.deepcopy(processes1), maxSwitch, alpha, tau)

  # print()
  alpha = 0.8
  tau = 5
  print("Actual burst weight?", alpha)
  print("Initial prediction?", tau)
  SJFApprox(copy.deepcopy(processes1), maxSwitch, alpha, tau)

  # print()
  # alpha = 0.2
  # tau = 3
  # print("Actual burst weight?", alpha)
  # print("Initial prediction?", tau)
  # SJFApprox(copy.deepcopy(processes1), maxSwitch, alpha, tau)

  # print()
  # alpha = 0.8
  # tau = 7
  # print("Actual burst weight?", alpha)
  # print("Initial prediction?", tau)
  # SJFApprox(copy.deepcopy(processes1), maxSwitch, alpha, tau)

  # print()
  # alpha = 0.2
  # tau = 7
  # print("Actual burst weight?", alpha)
  # print("Initial prediction?", tau)
  # SJFApprox(copy.deepcopy(processes1), maxSwitch, alpha, tau)

  print("\n==============================================================\n")
  
def lotteryDemo():
  print("No more starvation!")
  maxSwitch = int(input("How many context switches? "))
  infile2 = open("complexIn2.txt")
  processes2 = []
  print("Processes:")
  for line in infile2:
    line = line.strip()
    print(line)
    p = Process(line)
    processes2.append(p)

  alpha = float(input("Initial burst weight? "))
  tau = int(input("Initial prediction? "))
  SJFLottery(copy.deepcopy(processes2), maxSwitch, alpha, tau)
  infile2.close()

  print("\n==============================================================\n")
  print("Lottery out performs FCFS and RR:")
  maxSwitch = int(input("How many context switches? "))
  infile1 = open("lotteryIn1.txt")
  processes1 = []
  print("Processes:")
  for line in infile1:
    line = line.strip()
    print(line)
    p = Process(line)
    processes1.append(p)

  FCFSComplex(copy.deepcopy(processes1), maxSwitch)
  RRComplex(copy.deepcopy(processes1), maxSwitch)
  alpha = float(input("Initial burst weight? "))
  tau = int(input("Initial prediction? "))
  SJFLottery(copy.deepcopy(processes1), maxSwitch, alpha, tau)
  infile1.close()

def mlfQDemo():
  print("SJF is a pre-emptive algorithm:")
  maxSwitch = int(input("How many context switches? "))
  processes = []
  for i in range(1,6):
    infile1 = open("mlfIn"+str(i)+".txt")
    processes1 = []
    for line in infile1:
      line = line.strip()
      p = Process(line)
      processes1.append(p)
    processes.append(processes1)
    infile1.close()

  for processList in processes:
    print("Processes:")
    for p in processList:
      print(p)
    SJFComplex(copy.deepcopy(processList), maxSwitch)
    MLF(copy.deepcopy(processList), maxSwitch)
    print()



if __name__ == '__main__':
  approxDemo()