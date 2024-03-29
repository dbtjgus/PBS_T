class Schedule:
    def __init__(self,file):
        # initialize variables
        self.agent = []
        self.agent_dict = {}
        self.init_pos = {}
        self.readSchedule(file)

    def readSchedule(self, file):
        f = open(file, 'r')
        lines = f.readlines()
        lnum = 0 # line number
        t_dict = {}
        start_list = []
        goal_list = []
        self.a = '-1'
        while lnum < len(lines):
            self.a = lines[lnum].split(':')[0].split(' ')[1]
            self.agent.append(self.a)

            schedule_list = lines[lnum].split(':')[1].split('->')
            schedule_list.pop()
            t = 0
            for position in schedule_list:
                y = int(position.split(',')[0].split('(')[1])
                x = int(position.split(',')[1])
                d = int(position.split(',')[2].split(')')[0])
                t_dict[t] = {"x":x,"y":y, "d":d}
                t += 1
                if t == 1:
                    start_list = [x,y,d]
                elif t ==len(schedule_list):
                    goal_list = [x,y,d]
                    self.init_pos[self.a] = {"start":start_list,"goal":goal_list}
                    self.agent_dict[self.a] = t_dict
                    t_dict = {}
            lnum += 1
        f.close()

if __name__=="__main__":
    schedule = Schedule("paths.txt")


