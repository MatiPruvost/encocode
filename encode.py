from __future__ import division
import math
import random
import re
import string
import struct
import sys
import textwrap
import Image


class Message(object):
    def __init__(self, text, file_name):
        self.text = text
        self.file_name = file_name
        self.text_hex = None
        self.aspect = 4/3
        self.width = None
        self.height = None

    def _triads(self, text):
        """Triads generator. Need a text string. 
        Return a list of triads elements"""
        triads = list(self._split(text, 3))
        triads[-1] = triads[-1].ljust(3, " ")
        return triads

    def _split(self, text, size):
        """Text string splitter. Need a text string and a wize splitter"""
        for start in xrange(0, len(text), size):
            yield text[start:start + size]

    def _lines(self, text):
        """Three new text string generator. Need a text string.
        Return three new text string from the text string"""
        triads = self._triads(text)
        r = []
        g = []
        b = []
        for triad in triads:
            r.append(triad[0])
            g.append(triad[1])
            b.append(triad[2])
        return r, g, b

    def _interlaced_basic(self, pi, rho):
        """Lists interleaver. Need two list.
        Return """
        pirho = []
        for p, r in zip(pi, rho):
            pirho.append(p)
            pirho.append(r)
        len_pirho = int(len(pirho)/2)
        pi = pirho[:len_pirho]
        rho = pirho[len_pirho:]
        return pi[::-1], rho

    def _interlaced(self, text):
        alfa, beta, gamma = self._lines(text)
        alfa = alfa[::-1]
        beta = beta[::-1]
        alfa2, beta2 =self._interlaced_basic(alfa, beta)
        alfa3, gamma2 =self._interlaced_basic(alfa2, gamma)
        beta3, gamma3 =self._interlaced_basic(beta2, gamma2)
        return alfa3[::-1], beta3, gamma3[::-1]

    def _tuple_generate(self, list_):
        tuple_ = {}
        for element in list_:
            tuple_[len(tuple_)] = element

    def _get_size(self, n):
        height = math.sqrt(n / self.aspect)
        self.height = self._round(height)
        width = self.height * self.aspect
        self.width = self._round(width)

    def _round(self, n):
        return int(math.ceil(n))

    def _letter_to_hex(self, letter):
        return int(letter.encode('hex'), 16)

    def to_hex(self, text):
        line_hex = []
        for letter in text:
            letter_hex = self._letter_to_hex(letter)
            line_hex.append(letter_hex)
        return line_hex

    def _position(self, i):
        column = int(i / self.width)
        files = i % self.width
        return files, column

    def make_image(self):
        R, G, B = self._interlaced(self.text)
        R = self.to_hex(R)
        G = self.to_hex(G)
        B = self.to_hex(B)
        self._get_size(len(self.text))
        size = self.width*self.height
        image = Image.new('RGB', (self.width, self.height))
        pixels = image.load()
        for n, triad in enumerate(zip(R, G, B)):
            x, y = self._position(n)
            pixels[x, y] = tuple(triad)
        image.save(self.file_name + ".png")


if __name__ == "__main__":
    text = sys.argv[1]
    if len(sys.argv) == 2:
        file_name = "encoded"
    else:
        file_name = sys.argv[2]
    message = Message(text, file_name)
    message.make_image()