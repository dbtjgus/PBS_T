#!/usr/bin/env python3
import yaml
import matplotlib
# matplotlib.use("Agg")
from matplotlib.patches import Circle, Rectangle, Arrow
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
import matplotlib.animation as manimation
import argparse
import math
from map_parse.MapMOS import MapMOS
from Schedule import Schedule

Colors = ['orange', 'blue', 'green']


class Animation:
  def __init__(self, map, schedule):
    self.map = map
    self.schedule = schedule

    self.map.draw_map()

    self.fig = self.map.fig #plt.figure(frameon=False, figsize=(4 * aspect, 4))
    self.ax = self.map.ax #self.fig.add_subplot(111, aspect='equal')
    #self.fig.subplots_adjust(left=0,right=1,bottom=0,top=1, wspace=None, hspace=None)
    # self.ax.set_frame_on(False)

    self.patches = []
    self.artists = []
    self.agents = dict()
    self.agents_dir = dict()
    self.agent_names = dict()
    # create boundary patch


    # create agents:
    self.T = 0
    # draw goals first
    for name in self.schedule.agent:
      self.patches.append(Rectangle((self.schedule.init_pos[name]["goal"][0] + 0.25,
                                    self.map.height - (self.schedule.init_pos[name]["goal"][1]) - 0.75)
                                    , 0.5, 0.5, facecolor=Colors[0], edgecolor='black', alpha=0.5))
    for name in self.schedule.agent:
      self.agents[name] = Circle((self.schedule.init_pos[name]["start"][0] + 0.5,
                                  self.map.height - self.schedule.init_pos[name]["start"][1] - 0.5),
                                  0.3, facecolor=Colors[0], edgecolor='black')
      self.agents_dir[name] = Circle((self.schedule.init_pos[name]["start"][0] + 0.5 + 0.5*math.cos(math.radians(self.schedule.init_pos[name]["start"][2])),
                                    self.map.height - self.schedule.init_pos[name]["start"][1] - 0.5 - 0.5*math.sin(math.radians(self.schedule.init_pos[name]["start"][2]))),
                                  0.1, facecolor=Colors[2], edgecolor='black')
      self.agents[name].original_face_color = Colors[0]
      self.patches.append(self.agents[name])
      self.patches.append(self.agents_dir[name])
      self.T = max(self.T, len(self.schedule.agent_dict[name]))
      self.agent_names[name] = self.ax.text(self.schedule.init_pos[name]["start"][0] + 0.5,
                                            self.map.height - self.schedule.init_pos[name]["start"][1] - 0.5,
                                            name.replace('agent', ''))
      self.agent_names[name].set_horizontalalignment('center')
      self.agent_names[name].set_verticalalignment('center')
      self.artists.append(self.agent_names[name])

    self.anim = animation.FuncAnimation(self.fig, self.animate_func,
                               init_func=self.init_func,
                               frames=int(self.T+1) * 10,
                               interval=10,
                               blit=True)
  def save(self, file_name, speed):
    self.anim.save(
      file_name,
      "ffmpeg",
      fps=10 * speed,
      dpi=200),
      # savefig_kwargs={"pad_inches": 0, "bbox_inches": "tight"})

  def show(self):
    plt.show()

  def init_func(self):
    for p in self.patches:
      self.ax.add_patch(p)
    for a in self.artists:
      self.ax.add_artist(a)
    return self.patches + self.artists

  def animate_func(self, i):
    for agent in self.schedule.agent:
      pos = self.getState(i / 10, self.schedule.agent_dict[agent],agent)
      p1 = (pos[0], pos[1])
      p2 = (pos[2], pos[3])
      self.agents[agent].center = p1
      self.agents_dir[agent].center = p2

      self.agent_names[agent].set_position(p1)

    # reset all colors
    for _,agent in self.agents.items():
      agent.set_facecolor(agent.original_face_color)

    # check drive-drive collisions
    agents_array = [agent for _,agent in self.agents.items()]
    for i in range(0, len(agents_array)):
      for j in range(i+1, len(agents_array)):
        d1 = agents_array[i]
        d2 = agents_array[j]
        pos1 = np.array(d1.center)
        pos2 = np.array(d2.center)
        if np.linalg.norm(pos1 - pos2) < 0.7:
          d1.set_facecolor('red')
          d2.set_facecolor('red')
          print("COLLISION! (agent-agent) ({}, {})".format(i, j))

    return self.patches + self.artists


  def getState(self, t, d, agent):
    idx = 0
    while idx < len(d) and idx < t:
      idx += 1
    if idx == 0:
      return np.array([float(d[0]["x"]+0.5), float(self.map.height - d[0]["y"]-0.5),
                        float(d[0]["x"]+0.5+0.5*math.cos(math.radians(d[0]["d"]))),
                        float(self.map.height - d[0]["y"]-0.5 - 0.5*math.sin(math.radians(d[0]["d"])))])
    elif idx < len(d):
      posLast = np.array([float(d[idx-1]["x"]+0.5), float(self.map.height - d[idx-1]["y"]-0.5),
                          float(d[idx-1]["x"]+0.5+0.5*math.cos(math.radians(d[idx-1]["d"]))),
                          float(self.map.height - d[idx-1]["y"]-0.5 - 0.5*math.sin(math.radians(d[idx-1]["d"])))])
      posNext = np.array([float(d[idx]["x"]+0.5), float(self.map.height - d[idx]["y"]-0.5),
                          float(d[idx]["x"]+0.5+0.5*math.cos(math.radians(d[idx]["d"]))),
                          float(self.map.height - d[idx]["y"]-0.5 - 0.5*math.sin(math.radians(d[idx]["d"])))])
    else:
      return np.array([float(self.schedule.init_pos[agent]["goal"][0]+0.5),
                        float(self.map.height - self.schedule.init_pos[agent]["goal"][1]-0.5),
                        float(self.schedule.init_pos[agent]["goal"][0]+0.5+0.5*math.cos(math.radians(self.schedule.init_pos[agent]["goal"][2]))),
                        float(self.map.height - self.schedule.init_pos[agent]["goal"][1]-0.5 - 0.5*math.sin(math.radians(self.schedule.init_pos[agent]["goal"][2])))])
    dt = 1 #d[idx] - d[idx-1]
    t = (t - (idx-1)) / dt
    pos = (posNext - posLast) * t + posLast
    return pos



if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("map", help="input file containing map")
  parser.add_argument("schedule", help="schedule for agents")
  parser.add_argument('--video', dest='video', default=None, help="output video file (or leave empty to show on screen)")
  parser.add_argument("--speed", type=int, default=20, help="speedup-factor")
  args = parser.parse_args()

  map = MapMOS(args.map)
  schedule = Schedule(args.schedule)
  
  animation = Animation(map, schedule)

  if args.video:
    animation.save(args.video, args.speed)
  else:
    animation.show()
