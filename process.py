class Process:
  def __init__(self, line):
    p = line.split(" ")
    while("" in p):
      p.remove("")

    self.name = p[0]
    self.arrivalTime = int(p[1])


    self.repeating = (p[-1] == '-1')
    if(self.repeating):
      self.bursts = [int(i) for i in p[2:-1]]
    else:
      self.bursts = [int(i) for i in p[2:]]
    self.nextBurst = int(p[2])

    self.new = True
    self.stats = [int(p[1]), 0, 0]

  def __str__(self):
    return ("Name: " + self.name + 
    "  Arrival: " + str(self.arrivalTime) + 
    "  Bursts " + str(self.bursts) + 
    "  Next Burst " + str(self.nextBurst) + 
    "  New? " + str(self.new))

  def run(self, start, timeSlice = 0):
    self.new = False

    if(timeSlice and self.nextBurst > timeSlice):
      end = start + timeSlice

      self.arrivalTime += timeSlice
      self.nextBurst -= timeSlice
    else:
      end = start + self.nextBurst

      if(len(self.bursts) > 1):
        self.arrivalTime += self.bursts[0]
        self.arrivalTime += self.bursts[1]

        if(self.repeating):
          if(len(self.bursts)%2 == 0):
            self.bursts = self.bursts[2:] + [self.bursts[0], self.bursts[1]]
          else:
            self.bursts = self.bursts[2:-1] + [self.bursts[0]+self.bursts[-1], self.bursts[1]]
        else:
          self.bursts = self.bursts[2:]

        self.nextBurst = self.bursts[0]
      else:
        self.arrivalTime = None
        self.nextBurst = None

    return end

def insertByArrival(processes, p):
  for i, process in enumerate(processes):
    if(p.arrivalTime < process.arrivalTime):
      processes.insert(i, p)
      return
  processes.append(p)

def printStats(finishedProcesses):
  turnaroundTimes = [process.stats[2]-process.stats[0] for process in finishedProcesses]
  responseTimes = [process.stats[1]-process.stats[0] for process in finishedProcesses]
  print("\tAverage Turnaround Time: " + str(float(sum(turnaroundTimes))/len(finishedProcesses)))
  print("\tAverage Response Time: " + str(float(sum(responseTimes))/len(finishedProcesses)))


if __name__ == '__main__':
  infile = open("in.txt")

  for line in infile:
    p = Process(line)
    print(p.name, p.bursts)

  infile.close()