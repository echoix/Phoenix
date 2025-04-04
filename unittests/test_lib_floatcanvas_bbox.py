import unittest
from unittests import wtc
import wx

from wx.lib.floatcanvas.Utilities.BBox import *

#---------------------------------------------------------------------------

class testCreator(wtc.WidgetTestCase):
    def testCreates(self):
        B = BBox(((0,0),(5,5)))
        self.assertTrue(isinstance(B, BBox))

    def testType(self):
        B = np.array(((0,0),(5,5)))
        self.assertFalse(isinstance(B, BBox))

    def testDataType(self):
        B = BBox(((0,0),(5,5)))
        self.assertTrue(B.dtype == float)

    def testShape(self):
        B = BBox((0,0,5,5))
        self.assertTrue(B.shape == (2,2))

    def testShape2(self):
        self.assertRaises(ValueError, BBox, (0,0,5) )

    def testShape3(self):
        self.assertRaises(ValueError, BBox, (0,0,5,6,7) )

    def testArrayConstruction(self):
        A = np.array(((4,5),(10,12)), np.float64)
        B = BBox(A)
        self.assertTrue(isinstance(B, BBox))

    def testMinMax(self):
        self.assertRaises(ValueError, BBox, (0,0,-1,6) )

    def testMinMax2(self):
        self.assertRaises(ValueError, BBox, (0,0,1,-6) )

    def testMinMax(self):
        # OK to have a zero-sized BB
        B = BBox(((0,0),(0,5)))
        self.assertTrue(isinstance(B, BBox))

    def testMinMax2(self):
        # OK to have a zero-sized BB
        B = BBox(((10.0,-34),(10.0,-34.0)))
        self.assertTrue(isinstance(B, BBox))

    def testMinMax3(self):
        # OK to have a tiny BB
        B = BBox(((0,0),(1e-20,5)))
        self.assertTrue(isinstance(B, BBox))

    def testMinMax4(self):
        # Should catch tiny difference
        self.assertRaises(ValueError, BBox, ((0,0), (-1e-20,5)) )

class testAsBBox(wtc.WidgetTestCase):

    def testPassThrough(self):
        B = BBox(((0,0),(5,5)))
        C = asBBox(B)
        self.assertTrue(B is C)

    def testPassThrough2(self):
        B = (((0,0),(5,5)))
        C = asBBox(B)
        self.assertFalse(B is C)

    def testPassArray(self):
        # Different data type
        A = np.array( (((0,0),(5,5))) )
        C = asBBox(A)
        self.assertFalse(A is C)

    def testPassArray2(self):
        # same data type -- should be a view
        A = np.array( (((0,0),(5,5))), np.float64 )
        C = asBBox(A)
        A[0,0] = -10
        self.assertTrue(C[0,0] == A[0,0])

class testIntersect(wtc.WidgetTestCase):

    def testSame(self):
        B = BBox(((-23.5, 456),(56, 532.0)))
        C = BBox(((-23.5, 456),(56, 532.0)))
        self.assertTrue(B.Overlaps(C) )

    def testUpperLeft(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        C = BBox( ( (0, 12),(10, 32.0) ) )
        self.assertTrue(B.Overlaps(C) )

    def testUpperRight(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        C = BBox( ( (12, 12),(25, 32.0) ) )
        self.assertTrue(B.Overlaps(C) )

    def testLowerRight(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        C = BBox( ( (12, 5),(25, 15) ) )
        self.assertTrue(B.Overlaps(C) )

    def testLowerLeft(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        C = BBox( ( (-10, 5),(8.5, 15) ) )
        self.assertTrue(B.Overlaps(C) )

    def testBelow(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        C = BBox( ( (-10, 5),(8.5, 9.2) ) )
        self.assertFalse(B.Overlaps(C) )

    def testAbove(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        C = BBox( ( (-10, 25.001),(8.5, 32) ) )
        self.assertFalse(B.Overlaps(C) )

    def testLeft(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        C = BBox( ( (4, 8),(4.95, 32) ) )
        self.assertFalse(B.Overlaps(C) )

    def testRight(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        C = BBox( ( (17.1, 8),(17.95, 32) ) )
        self.assertFalse(B.Overlaps(C) )

    def testInside(self):
        B = BBox( ( (-15, -25),(-5, -10) ) )
        C = BBox( ( (-12, -22), (-6, -8) ) )
        self.assertTrue(B.Overlaps(C) )

    def testOutside(self):
        B = BBox( ( (-15, -25),(-5, -10) ) )
        C = BBox( ( (-17, -26), (3, 0) ) )
        self.assertTrue(B.Overlaps(C) )

    def testTouch(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        C = BBox( ( (15, 8),(17.95, 32) ) )
        self.assertTrue(B.Overlaps(C) )

    def testCorner(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        C = BBox( ( (15, 25),(17.95, 32) ) )
        self.assertTrue(B.Overlaps(C) )

    def testZeroSize(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        C = BBox( ( (15, 25),(15, 25) ) )
        self.assertTrue(B.Overlaps(C) )

    def testZeroSize2(self):
        B = BBox( ( (5, 10),(5, 10) ) )
        C = BBox( ( (15, 25),(15, 25) ) )
        self.assertFalse(B.Overlaps(C) )

    def testZeroSize3(self):
        B = BBox( ( (5, 10),(5, 10) ) )
        C = BBox( ( (0, 8),(10, 12) ) )
        self.assertTrue(B.Overlaps(C) )

    def testZeroSize4(self):
        B = BBox( ( (5, 1),(10, 25) ) )
        C = BBox( ( (8, 8),(8, 8) ) )
        self.assertTrue(B.Overlaps(C) )



class testEquality(wtc.WidgetTestCase):
    def testSame(self):
        B = BBox( ( (1.0, 2.0), (5.0, 10.0) ) )
        C = BBox( ( (1.0, 2.0), (5.0, 10.0) ) )
        self.assertTrue(B == C)

    def testIdentical(self):
        B = BBox( ( (1.0, 2.0), (5.0, 10.0) ) )
        self.assertTrue(B == B)

    def testNotSame(self):
        B = BBox( ( (1.0, 2.0), (5.0, 10.0) ) )
        C = BBox( ( (1.0, 2.0), (5.0, 10.1) ) )
        self.assertFalse(B == C)

    def testWithArray(self):
        B = BBox( ( (1.0, 2.0), (5.0, 10.0) ) )
        C = np.array( ( (1.0, 2.0), (5.0, 10.0) ) )
        self.assertTrue(B == C)

    def testWithArray2(self):
        B = BBox( ( (1.0, 2.0), (5.0, 10.0) ) )
        C = np.array( ( (1.0, 2.0), (5.0, 10.0) ) )
        self.assertTrue(C == B)

    def testWithArray2(self):
        B = BBox( ( (1.0, 2.0), (5.0, 10.0) ) )
        C = np.array( ( (1.01, 2.0), (5.0, 10.0) ) )
        self.assertFalse(C == B)

class testInside(wtc.WidgetTestCase):
    def testSame(self):
        B = BBox( ( (1.0, 2.0), (5.0, 10.0) ) )
        C = BBox( ( (1.0, 2.0), (5.0, 10.0) ) )
        self.assertTrue(B.Inside(C))

    def testPoint(self):
        B = BBox( ( (1.0, 2.0), (5.0, 10.0) ) )
        C = BBox( ( (3.0, 4.0), (3.0, 4.0) ) )
        self.assertTrue(B.Inside(C))

    def testPointOutside(self):
        B = BBox( ( (1.0, 2.0), (5.0, 10.0) ) )
        C = BBox( ( (-3.0, 4.0), (0.10, 4.0) ) )
        self.assertFalse(B.Inside(C))

    def testUpperLeft(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        C = BBox( ( (0, 12),(10, 32.0) ) )
        self.assertFalse(B.Inside(C) )

    def testUpperRight(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        C = BBox( ( (12, 12),(25, 32.0) ) )
        self.assertFalse(B.Inside(C) )

    def testLowerRight(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        C = BBox( ( (12, 5),(25, 15) ) )
        self.assertFalse(B.Inside(C) )

    def testLowerLeft(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        C = BBox( ( (-10, 5),(8.5, 15) ) )
        self.assertFalse(B.Inside(C) )

    def testBelow(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        C = BBox( ( (-10, 5),(8.5, 9.2) ) )
        self.assertFalse(B.Inside(C) )

    def testAbove(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        C = BBox( ( (-10, 25.001),(8.5, 32) ) )
        self.assertFalse(B.Inside(C) )

    def testLeft(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        C = BBox( ( (4, 8),(4.95, 32) ) )
        self.assertFalse(B.Inside(C) )

    def testRight(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        C = BBox( ( (17.1, 8),(17.95, 32) ) )
        self.assertFalse(B.Inside(C) )

class testPointInside(wtc.WidgetTestCase):
    def testPointIn(self):
        B = BBox( ( (1.0, 2.0), (5.0, 10.0) ) )
        P = (3.0, 4.0)
        self.assertTrue(B.PointInside(P))

    def testUpperLeft(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        P = (4, 30)
        self.assertFalse(B.PointInside(P))

    def testUpperRight(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        P = (16, 30)
        self.assertFalse(B.PointInside(P))

    def testLowerRight(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        P = (16, 4)
        self.assertFalse(B.PointInside(P))

    def testLowerLeft(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        P = (-10, 5)
        self.assertFalse(B.PointInside(P))

    def testBelow(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        P = (10, 5)
        self.assertFalse(B.PointInside(P))

    def testAbove(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        P  = ( 10, 25.001)
        self.assertFalse(B.PointInside(P))

    def testLeft(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        P = (4, 12)
        self.assertFalse(B.PointInside(P))

    def testRight(self):
        B = BBox( ( (5, 10),(15, 25) ) )
        P = (17.1, 12.3)
        self.assertFalse(B.PointInside(P))

    def testPointOnTopLine(self):
        B = BBox( ( (1.0, 2.0), (5.0, 10.0) ) )
        P = (3.0, 10.0)
        self.assertTrue(B.PointInside(P))

    def testPointLeftTopLine(self):
        B = BBox( ( (1.0, 2.0), (5.0, 10.0) ) )
        P = (-3.0, 10.0)
        self.assertFalse(B.PointInside(P))

    def testPointOnBottomLine(self):
        B = BBox( ( (1.0, 2.0), (5.0, 10.0) ) )
        P = (3.0, 5.0)
        self.assertTrue(B.PointInside(P))

    def testPointOnLeft(self):
        B = BBox( ( (-10.0, -10.0), (-1.0, -1.0) ) )
        P = (-10, -5.0)
        self.assertTrue(B.PointInside(P))

    def testPointOnRight(self):
        B = BBox( ( (-10.0, -10.0), (-1.0, -1.0) ) )
        P = (-1, -5.0)
        self.assertTrue(B.PointInside(P))

    def testPointOnBottomRight(self):
        B = BBox( ( (-10.0, -10.0), (-1.0, -1.0) ) )
        P = (-1, -10.0)
        self.assertTrue(B.PointInside(P))

class testFromPoints(wtc.WidgetTestCase):

    def testCreate(self):
        Pts = np.array( ((5,2),
                (3,4),
                (1,6),
                ), np.float64 )
        B = fromPoints(Pts)
        #B = BBox( ( (1.0, 2.0), (5.0, 10.0) ) )
        self.assertTrue(B[0,0] == 1.0 and
                        B[0,1] == 2.0 and
                        B[1,0] == 5.0 and
                        B[1,1] == 6.0
                        )
    def testCreateInts(self):
        Pts = np.array( ((5,2),
                (3,4),
                (1,6),
                ) )
        B = fromPoints(Pts)
        self.assertTrue(B[0,0] == 1.0 and
                        B[0,1] == 2.0 and
                        B[1,0] == 5.0 and
                        B[1,1] == 6.0
                        )

    def testSinglePoint(self):
        Pts = np.array( (5,2), np.float64 )
        B = fromPoints(Pts)
        self.assertTrue(B[0,0] == 5.0 and
                        B[0,1] == 2.0 and
                        B[1,0] == 5.0 and
                        B[1,1] == 2.0
                        )

    def testListTuples(self):
        Pts = [ (3, 6.5),
                (13, 43.2),
                (-4.32, -4),
                (65, -23),
                (-0.0001, 23.432),
                ]
        B = fromPoints(Pts)
        self.assertTrue(B[0,0] == -4.32 and
                        B[0,1] == -23.0 and
                        B[1,0] == 65.0 and
                        B[1,1] == 43.2
                        )
class testMerge(wtc.WidgetTestCase):
    A = BBox( ((-23.5, 456), (56, 532.0)) )
    B = BBox( ((-20.3, 460), (54, 465  )) )# B should be completely inside A
    C = BBox( ((-23.5, 456), (58, 540.0)) )# up and to the right or A
    D = BBox( ((-26.5, 12), (56, 532.0)) )

    def testInside(self):
        C = self.A.copy()
        C.Merge(self.B)
        self.assertTrue(C == self.A)

    def testFullOutside(self):
        C = self.B.copy()
        C.Merge(self.A)
        self.assertTrue(C == self.A)

    def testUpRight(self):
        A = self.A.copy()
        A.Merge(self.C)
        self.assertTrue(A[0] == self.A[0] and A[1] == self.C[1])

    def testDownLeft(self):
        A = self.A.copy()
        A.Merge(self.D)
        self.assertTrue(A[0] == self.D[0] and A[1] == self.A[1])

class testWidthHeight(wtc.WidgetTestCase):
    B = BBox( ( (1.0, 2.0), (5.0, 10.0) ) )
    def testWidth(self):
        self.assertTrue(self.B.Width == 4.0)

    def testWidth(self):
        self.assertTrue(self.B.Height == 8.0)

    def attemptSetWidth(self):
        self.B.Width = 6

    def attemptSetHeight(self):
        self.B.Height = 6

    def testSetW(self):
        self.assertRaises(AttributeError, self.attemptSetWidth)

    def testSetH(self):
        self.assertRaises(AttributeError, self.attemptSetHeight)

class testCenter(wtc.WidgetTestCase):
    B = BBox( ( (1.0, 2.0), (5.0, 10.0) ) )
    def testCenter(self):
        self.assertTrue( (self.B.Center == (3.0, 6.0)).all() )

    def attemptSetCenter(self):
        self.B.Center = (6, 5)

    def testSetCenter(self):
        self.assertRaises(AttributeError, self.attemptSetCenter)


class testBBarray(wtc.WidgetTestCase):
    BBarray = np.array( ( ((-23.5, 456), (56, 532.0)),
                         ((-20.3, 460), (54, 465  )),
                         ((-23.5, 456), (58, 540.0)),
                         ((-26.5,  12), (56, 532.0)),
                       ),
                       dtype=float)
    BB = asBBox( ((-26.5,  12.), ( 58. , 540.)) )

    def testJoin(self):
        BB = fromBBArray(self.BBarray)
        self.assertTrue(BB == self.BB, "Wrong BB was created. It was:\n%s \nit should have been:\n%s"%(BB, self.BB))

class testNullBBox(wtc.WidgetTestCase):
    B1 = NullBBox()
    B2 = NullBBox()
    B3 = BBox( ( (1.0, 2.0), (5.0, 10.0) ) )

    def testValues(self):
        self.assertTrue( np.all(np.isnan(self.B1)) )

    def testIsNull(self):
        self.assertTrue( self.B1.IsNull )

    def testEquals(self):
        self.assertTrue( (self.B1 == self.B2) == True )

    def testNotEquals(self):
        self.assertTrue ( (self.B1 == self.B3) == False,
                          "NotEquals failed for\n%s,\n %s:%s"%(self.B1, self.B3, (self.B1 == self.B3)) )

    def testNotEquals2(self):
        self.assertTrue ( (self.B3 == self.B1) == False,
                          "NotEquals failed for\n%s,\n %s:%s"%(self.B3, self.B1, (self.B3 == self.B1))  )

    def testMerge(self):
        C = self.B1.copy()
        C.Merge(self.B3)
        self.assertTrue( C == self.B3,
                         "merge failed, got: %s"%C )

    def testOverlaps(self):
        self.assertTrue( self.B1.Overlaps(self.B3) == False)

    def testOverlaps2(self):
        self.assertTrue( self.B3.Overlaps(self.B1) == False)


class testInfBBox(wtc.WidgetTestCase):
    B1 = InfBBox()
    B2 = InfBBox()
    B3 = BBox( ( (1.0, 2.0), (5.0, 10.0) ) )
    NB = NullBBox()

    def testValues(self):
        self.assertTrue( np.all(np.isinf(self.B1)) )

#    def testIsNull(self):
#        self.assertTrue( self.B1.IsNull )

    def testEquals(self):
        self.assertTrue( (self.B1 == self.B2) == True )

    def testNotEquals(self):
        self.assertTrue ( (self.B1 == self.B3) == False,
                          "NotEquals failed for\n%s,\n %s:%s"%(self.B1, self.B3, (self.B1 == self.B3)) )

    def testNotEquals2(self):
        self.assertTrue ( (self.B3 == self.B1) == False,
                          "NotEquals failed for\n%s,\n %s:%s"%(self.B3, self.B1, (self.B3 == self.B1))  )

    def testMerge(self):
        C = self.B1.copy()
        C.Merge(self.B3)
        self.assertTrue( C == self.B2,
                         "merge failed, got: %s"%C )

    def testMerge2(self):
        C = self.B3.copy()
        C.Merge(self.B1)
        self.assertTrue( C == self.B1,
                         "merge failed, got: %s"%C )

    def testOverlaps(self):
        self.assertTrue( self.B1.Overlaps(self.B2) == True)

    def testOverlaps2(self):
        self.assertTrue( self.B3.Overlaps(self.B1) == True)

    def testOverlaps3(self):
        self.assertTrue( self.B1.Overlaps(self.B3) == True)

    def testOverlaps4(self):
        self.assertTrue( self.B1.Overlaps(self.NB) == True)

    def testOverlaps5(self):
        self.assertTrue( self.NB.Overlaps(self.B1) == True)


class testSides(wtc.WidgetTestCase):
    B = BBox( ( (1.0, 2.0), (5.0, 10.0) ) )

    def testLeft(self):
        self.assertTrue( self.B.Left == 1.0  )
    def testRight(self):
        self.assertTrue( self.B.Right == 5.0  )
    def testBottom(self):
        self.assertTrue( self.B.Bottom == 2.0  )
    def testTop(self):
        self.assertTrue( self.B.Top == 10.0  )


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
