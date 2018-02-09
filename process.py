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

  def __str__(self):
    return self.name + "\t" + str(self.arrivalTime) + "\t" + str(self.bursts)

  def run(self, start):
    end = start + self.nextBurst
    if(len(self.bursts) > 1):
      self.arrivalTime += self.burst[0]
      self.arrivalTime += self.bursts[1]

      if(self.repeating):
        if(len(self.bursts)%2 == 0):
          self.bursts = self.bursts[2:] + [self.bursts[0], self.bursts[1]]
        else:
          self.bursts = self.bursts[2:-1] + [self.bursts[0]+self.bursts[-1], self.bursts[1]]
      else:
        self.bursts = self.bursts[2:]
    else:
      self.arrivalTime = None

    if(len(self.bursts) > 0):
      self.nextBurst = self.bursts[0]
    else:
      self.nextBurst = None

    return end

def insertByArrival(processes, p):
  for i, process in enumerate(processes):
    if(process.nextBurst < p.nextBurst):
      processes.insert(i, p)
      return


if __name__ == '__main__':
  infile = open("in.txt")

  for line in infile:
    p = Process(line)
    print(p.name, p.bursts)

  infile.close()