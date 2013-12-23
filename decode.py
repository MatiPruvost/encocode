from __future__ import division
import sys
import Image


class Message(object):
    def __init__(self, path):
        self.image = Image.open(path)
        self.rgb = self.image.convert('RGB')
        self.width, self.height = self.image.size
        self.pixels_n = self.width*self.height
        
    def _position(self, number):
        column = int(number / self.width)
        files = number % self.width
        return self.rgb.getpixel((files, column))
    
    def _get_pixels(self):
        pixels = []
        for number in range(self.pixels_n):
            pixels.append(self._position(number))
        return pixels
        
    def to_char(self, hex_):
        hex_ = format(hex_, 'x')
        return hex_.decode('hex')
    
    def make_rgb(self):
        pixels = self._get_pixels()
        r = []
        g = []
        b = []
        for rr, gg, bb in pixels:
            if rr != 0 and gg != 0 and bb != 0:
                r.append(self.to_char(rr))
                g.append(self.to_char(gg))
                b.append(self.to_char(bb))
        return r, g, b

    def _interlaced_basic(self, pi, rho):
        pi = pi[::-1]
        pirho = pi + rho
        pi = []
        rho = []
        for p, r in zip(pirho[::2], pirho[1::2]):
            pi.append(p)
            rho.append(r)
        return pi, rho

    def _interlaced(self):
        alfa3, beta3, gamma3 = self.make_rgb()
        alfa3 = alfa3[::-1]
        gamma3 = gamma3[::-1]
        beta2, gamma2 = self._interlaced_basic(beta3, gamma3)
        alfa2, gamma =self._interlaced_basic(alfa3, gamma2)
        alfa, beta =self._interlaced_basic(alfa2, beta2)
        alfa = alfa[::-1]
        beta = beta[::-1]
        return alfa, beta, gamma

    def _lines(self, alfa, beta, gamma):
        text = []
        for r, g, b in zip(alfa, beta, gamma):
            text.append(r)
            text.append(g)
            text.append(b)
        return text

    def decode(self):
        r, g, b = self._interlaced()
        text = self._lines(r, g, b)
        return ''.join(text)


if __name__ == "__main__":
    message = Message(sys.argv[1])
    print message.decode()