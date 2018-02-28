class Process:
  def __init__(self, line):
    p = line.split(" ")
    while("" in p):
      p.remove("")

    self.name = p[0]
    self.arrivalTime = int(p[1])
    self.priority = 0

    self.repeating = (p[-1] == '-1')
    if(self.repeating):
      self.bursts = [int(i) for i in p[2:-1]]
    else:
      self.bursts = [int(i) for i in p[2:]]
    self.nextBurst = int(p[2])
    self.lastBurst = 0

    self.new = True
    self.stats = [int(p[1]), 0, 0]

  def __str__(self):
    # return ("Name: " + self.name + 
    # "  Arrival: " + str(self.arrivalTime) + 
    # "  Bursts " + str(self.bursts) + 
    # "  Priority " + str(self.priority) +
    # "  Next Burst " + str(self.nextBurst) + 
    # "  New? " + str(self.new))
    b = ""
    for i in self.bursts:
      b += str(i)
      b += " "
    return (self.name + "   " + str(self.arrivalTime) + "   " + b)

  def ioNonsense(self, io, ioStr):
    if(self.arrivalTime < io):
      self.arrivalTime = io
    elif(self.arrivalTime > io):
      ioStr += (str(io) + ":IDLE  ")

    ioStr += (str(self.arrivalTime) + ":" + self.name + "  ")
    self.arrivalTime += self.bursts[1]
    io += self.bursts[1]

    return io, ioStr

  def repeatingNonsense(self):
    if(self.repeating):
      if(len(self.bursts)%2 == 0):
        self.bursts = self.bursts[2:] + [self.bursts[0], self.bursts[1]]
      else:
        self.bursts = self.bursts[2:-1] + [self.bursts[0]+self.bursts[-1], self.bursts[1]]
    else:
      self.bursts = self.bursts[2:]

  def calcApprox(self, alpha):
    self.approx = alpha*self.lastBurst + (1-alpha)*self.approx
    if(self.approx < 1):
      self.approx = 1
    else:
      self.approx = round(self.approx)

  def run(self, start, io, timeSlice = 0):
    ioStr = ""
    self.new = False

    if(timeSlice and self.nextBurst > timeSlice):
      end = start + timeSlice

      self.arrivalTime += timeSlice
      self.nextBurst -= timeSlice
      self.lastBurst = timeSlice
      self.priority += 1
    else:
      end = start + self.nextBurst

      if(len(self.bursts) > 1):
        self.arrivalTime += self.nextBurst

        io, ioStr = self.ioNonsense(io, ioStr)
        
        self.repeatingNonsense()

        self.lastBurst = self.nextBurst
        self.nextBurst = self.bursts[0]
      else:
        self.arrivalTime = None
        self.nextBurst = None

    return end, (io, ioStr)

def resetAllPriorities(priorities):
  for processes in priorities[1:]:
    for p in processes:
      p.priority = 0
      insertByArrival(priorities[0], p)

def insertByArrival(processes, p):
  for i, process in enumerate(processes):
    if(p.arrivalTime < process.arrivalTime):
      processes.insert(i, p)
      return
  processes.append(p)

def printStats(finishedProcesses, processes):
  # for p in finishedProcesses:
  #   print(p.stats)
  turnaroundTimes = [process.stats[2]-process.stats[0] for process in finishedProcesses]
  responseTimes = [process.stats[1]-process.stats[0] for process in finishedProcesses]
  
  finiteFinished = True
  for p in processes:
    finiteFinished = p.repeating
    if(not finiteFinished):
      break

  if(len(finishedProcesses) == 0):
    print("No finished processes")
  elif(not finiteFinished):
    print("Not all finite processes completed")
  else:
    print("\tAverage Turnaround Time: " + str(float(sum(turnaroundTimes))/len(finishedProcesses)))
    print("\tAverage Response Time: " + str(float(sum(responseTimes))/len(finishedProcesses)))


if __name__ == '__main__':
  infile = open("in.txt")

  for line in infile:
    p = Process(line)
    print(p.name, p.bursts)
    if(p):
      print("Hi")

  infile.close()