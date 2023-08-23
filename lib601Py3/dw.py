# Embedded file name: /mit/6.01/mercurial/spring11/codeSandbox/lib601/dw.py
import tkinter
import tkinter.filedialog
import math
from . import tk

class DrawingWindow:

    def __init__(self, windowWidth, windowHeight, xMin, xMax, yMin, yMax, title):
        tk.init()
        self.title = title
        self.top = tkinter.Toplevel()
        self.top.wm_title(title)
        self.top.protocol('WM_DELETE_WINDOW', self.destroy)
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.canvas = tkinter.Canvas(self.top, width=self.windowWidth, height=self.windowHeight, background='white')
        self.canvas.pack()
        self.xMin = xMin
        self.yMin = yMin
        self.xMax = xMax if xMax else width
        self.yMax = yMax if yMax else height
        self.xScale = windowWidth / float(self.xMax - self.xMin)
        self.yScale = windowHeight / float(self.yMax - self.yMin)

    def destroy(self):
        self.top.destroy()

    def save(self):
        filename = tkinter.filedialog.asksaveasfilename(filetypes=[('PS', '*.ps')], defaultextension='.ps', title='Save Window to ...')
        if len(filename) == 0:
            return
        self.canvas.update()
        self.canvas.postcript(file=filename)

    def scaleX(self, x):
        return self.xScale * (x - self.xMin)

    def scaleY(self, y):
        return self.windowHeight - self.yScale * (y - self.yMin)

    def scaleYMag(self, y):
        return self.yScale * (y - self.yMin)

    def drawPoint(self, x, y, color = 'blue'):
        windowX = self.scaleX(x)
        windowY = self.scaleY(y)
        return self.canvas.create_rectangle(windowX - 1, windowY - 1, windowX + 1, windowY + 1, fill=color, outline=color)

    def drawRobotWithNose(self, x, y, theta, color = 'blue', size = 6):
        rawx = math.cos(theta)
        rawy = math.sin(theta)
        hx, hy = (0.15, 0.0)
        noseX = x + rawx * hx - rawy * hy
        noseY = y + rawy * hx + rawx * hy
        return self.drawRobot(x, y, noseX, noseY, color=color, size=size)

    def drawRobot(self, x, y, noseX, noseY, color = 'blue', size = 8):
        windowX = self.scaleX(x)
        windowY = self.scaleY(y)
        hsize = int(size) / 2
        return (self.canvas.create_rectangle(windowX - hsize, windowY - hsize, windowX + hsize, windowY + hsize, fill=color, outline=color), self.canvas.create_line(windowX, windowY, self.scaleX(noseX), self.scaleY(noseY), fill=color, width=2, arrow='last'))

    def drawSquare(self, x, y, size, color = 'blue'):
        windowX = self.scaleX(x)
        windowY = self.scaleY(y)
        xhsize = size * self.xScale / 2
        yhsize = size * self.yScale / 2
        return self.canvas.create_rectangle(windowX - xhsize, windowY - yhsize, windowX + xhsize, windowY + yhsize, fill=color, outline=color)

    def drawText(self, x, y, label, color = 'blue'):
        windowX = self.scaleX(x)
        windowY = self.scaleY(y)
        return self.canvas.create_text(windowX, windowY, text=label, fill=color)

    def drawRect(self, xxx_todo_changeme, xxx_todo_changeme1, color = 'black'):
        (x1, y1) = xxx_todo_changeme
        (x2, y2) = xxx_todo_changeme1
        return self.canvas.create_rectangle(self.scaleX(x1), self.scaleY(y1), self.scaleX(x2), self.scaleY(y2), fill=color)

    def drawLineSeg(self, x1, y1, x2, y2, color = 'black', width = 2):
        return self.canvas.create_line(self.scaleX(x1), self.scaleY(y1), self.scaleX(x2), self.scaleY(y2), fill=color, width=width)

    def drawUnscaledLineSeg(self, x1, y1, xproj, yproj, color = 'black', width = 1):
        return self.canvas.create_line(self.scaleX(x1), self.scaleY(y1), self.scaleX(x1) + xproj, self.scaleY(y1) - yproj, fill=color, width=width)

    def drawUnscaledRect(self, x1, y1, xproj, yproj, color = 'black'):
        return self.canvas.create_rectangle(self.scaleX(x1) - xproj, self.scaleY(y1) + yproj, self.scaleX(x1) + xproj, self.scaleY(y1) - yproj, fill=color)

    def drawLine(self, xxx_todo_changeme2, color = 'black'):
        (a, b, c) = xxx_todo_changeme2
        if abs(b) < 0.001:
            startX = self.scaleX(-c / a)
            endX = self.scaleX(-c / a)
            startY = self.scaleY(self.yMin)
            endY = self.scaleY(self.yMax)
        else:
            startX = self.scaleX(self.xMin)
            startY = self.scaleY(-(a * self.xMin + c) / b)
            endX = self.scaleX(self.xMax)
            endY = self.scaleY(-(a * self.xMax + c) / b)
        return self.canvas.create_line(startX, startY, endX, endY, fill=color)

    def delete(self, thing):
        self.canvas.delete(thing)

    def clear(self):
        self.canvas.delete('all')