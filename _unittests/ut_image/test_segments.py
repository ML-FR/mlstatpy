# -*- coding: utf-8 -*-
"""
@brief      test log(time=38s)
"""

import sys
import os
import unittest
import math


try:
    import pyquickhelper as skip_
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyquickhelper",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import pyquickhelper as skip_


try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src

from pyquickhelper.pycode import ExtTestCase, get_temp_folder
from src.mlstatpy.image.detection_segment.geometrie import Point
from src.mlstatpy.image.detection_segment.detection_segment_segangle import SegmentBord
from src.mlstatpy.image.detection_segment.detection_segment_bord import SegmentBord_Commun
from src.mlstatpy.image.detection_segment.detection_segment import detect_segments, plot_segments
from src.mlstatpy.image.detection_segment.detection_segment import _calcule_gradient, plot_gradient


class TestSegments(ExtTestCase):

    visual = False

    def test_segment_bord(self):
        s = SegmentBord(Point(3, 4))
        n = True
        res = []
        while n:
            res.append(s.copy())
            n = s.next()
        self.assertEqual(len(res), 279)
        self.assertEqual(res[-1].a, Point(0, 3))
        self.assertEqual(res[-1].b, Point(7, 2))
        self.assertEqual(res[-2].a, Point(0, 0))
        self.assertEqual(res[-2].b, Point(6, 0))

    def test_segment_bord2(self):
        """
        Ceci n'est execute que si ce fichier est le fichier principal,
        permet de verifier que tous les segments sont bien parcourus."""
        xx, yy = 163, 123

        if TestSegments.visual and __name__ == "__main__":

            def attendre_clic(screen):
                """attend la pression d'un clic de souris
                avant de continuer l'execution du programme,
                methode pour pygame"""
                color = 0, 0, 0
                pygame.display.flip()
                reste = True
                while reste:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP:
                            reste = False
                            break

            import pygame
            pygame.init()
            screen = pygame.display.set_mode((xx * 4, yy * 4))
            screen.fill((255, 255, 255))
            pygame.display.flip()

            for i in range(1, 4):
                pygame.draw.line(screen, (255, 0, 0),
                                 (0, i * yy), (xx * 4, i * yy))
                pygame.draw.line(screen, (255, 0, 0),
                                 (xx * i, 0), (xx * i, 4 * yy))

        s = SegmentBord(Point(xx, yy), math.pi / 6)
        s.premier()

        i = 0
        n = True
        angle = 0
        x, y = 0, 0
        couleur = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
                   (255, 0, 255), (0, 0, 0), (128, 128, 128)]
        segs = []
        c = 0
        while n:
            if TestSegments.visual and __name__ == "__main__" and i % 100 == 0:
                print("i={0} s={1}".format(i, s))

            x = s.bord1
            y = s.calcul_bord2()
            a = (int(s.a.x) + x * xx, int(s.a.y) + y * yy)
            b = (int(s.b.x) + x * xx, int(s.b.y) + y * yy)

            if TestSegments.visual and __name__ == "__main__":
                pygame.draw.line(screen, couleur[c % len(couleur)], a, b)
                pygame.display.flip()

            n = s.next()
            if angle != s.angle:
                if TestSegments.visual and __name__ == "__main__":
                    print("changement angle = ", angle,
                          " --> ", s.angle, "   clic ", s)
                    pygame.draw.line(screen, couleur[c % len(couleur)], a, b)
                    pygame.display.flip()
                    # attendre_clic(screen)
                c += 1
            angle = s.angle
            segs.append(s.copy())
            i += 1

        if TestSegments.visual and __name__ == "__main__":
            pygame.display.flip()
            attendre_clic(screen)

        self.assertEqual(len(segs), 2852)
        seg = segs[-1]
        self.assertEqual(seg.a.x, 0)
        self.assertEqual(seg.a.y, 122)
        self.assertEqual(seg.b.x, 286)
        self.assertEqual(seg.b.y, 122)

    def test_gradient(self):
        temp = get_temp_folder(__file__, "temp_segment_gradient")
        img = os.path.join(temp, "..", "data", "eglise_zoom2.jpg")
        grad = _calcule_gradient(img)
        self.assertEqual(grad.shape, (308, 408))
        for d in [-2, -1, 0, 1, 2]:
            imgrad = plot_gradient(img, grad, direction=d)
            grfile = os.path.join(temp, "gradient-%d.png" % d)
            imgrad.save(grfile)
            self.assertExists(grfile)

        with open(os.path.join(temp, "..", "data", "gradient--2.png"), 'rb') as f:
            c1 = f.read()
        with open(os.path.join(temp, "gradient--2.png"), 'rb') as f:
            c2 = f.read()
        self.assertEqual(c1, c2)

    def _test_segment_detection(self):
        temp = get_temp_folder(__file__, "temp_segment_detection")
        img = os.path.join(temp, "..", "data", "eglise_zoom2.jpg")
        outfile = os.path.join(temp, "seg.png")
        seg = detect_segments(img, stop=1000)
        plot_segments(img, seg, outfile=outfile)
        self.assertIsInstance(seg, list)
        self.assertEqual(len(seg), 2099)
        seg.sort()
        for s in seg[:50]:
            print(s)
        for s in seg[-50:]:
            print(s)


if __name__ == "__main__":
    unittest.main()
