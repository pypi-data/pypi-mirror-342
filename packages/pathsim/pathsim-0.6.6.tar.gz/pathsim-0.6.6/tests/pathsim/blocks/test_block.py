########################################################################################
##
##                                  TESTS FOR 
##                              'blocks._block.py'
##
##                              Milan Rother 2024
##
########################################################################################

# IMPORTS ==============================================================================

import unittest
import numpy as np

from pathsim.blocks._block import Block
from pathsim.utils.portreference import PortReference


# TESTS ================================================================================

class TestBlock(unittest.TestCase):
    """
    Test the implementation of the base 'Block' class
    """

    def test_init(self):

        B = Block()

        #test default inputs and outputs
        self.assertEqual(B.inputs, {0: 0.0})
        self.assertEqual(B.outputs, {0: 0.0})

        #test default engine
        self.assertEqual(B.engine, None)

        #is active
        self.assertTrue(B._active)

        #operators
        self.assertEqual(B.op_alg, None)
        self.assertEqual(B.op_dyn, None)


    def test_len(self):

        B = Block()

        #test default len method
        self.assertEqual(len(B), 1)
            

    def test_on_off_bool(self):
        
        B = Block()

        #default active
        self.assertTrue(B)

        #deactivate block
        B.off()
        self.assertFalse(B)

        #activate block
        B.on()
        self.assertTrue(B)


    def test_get_events(self):

        B = Block()

        #no internal events by default
        self.assertEqual(B.get_events(), [])


    def test_getitem(self):

        B = Block()

        #test default getitem method
        pr = B[0]
        self.assertTrue(isinstance(pr, PortReference))
        self.assertEqual(pr.block, B)
        self.assertEqual(pr.ports, [0])

        pr = B[2]
        self.assertEqual(pr.ports, [2])

        pr = B[30]
        self.assertEqual(pr.ports, [30])

        #test input validation
        with self.assertRaises(ValueError): B[0.2]
        with self.assertRaises(ValueError): B[1j]
        with self.assertRaises(ValueError): B["a"]


    def test_getitem_slice(self):

        B = Block()

        #test slicing in getitem
        pr = B[:1]
        self.assertTrue(isinstance(pr, PortReference))
        self.assertEqual(pr.ports, [0])

        pr = B[:2]
        self.assertTrue(isinstance(pr, PortReference))
        self.assertEqual(pr.ports, [0, 1])

        pr = B[1:2]
        self.assertTrue(isinstance(pr, PortReference))
        self.assertEqual(pr.ports, [1])

        pr = B[0:5]
        self.assertTrue(isinstance(pr, PortReference))
        self.assertEqual(pr.ports, [0, 1, 2, 3, 4])

        pr = B[3:7]
        self.assertTrue(isinstance(pr, PortReference))
        self.assertEqual(pr.ports, [3, 4, 5, 6])

        pr = B[3:7:2]
        self.assertTrue(isinstance(pr, PortReference))
        self.assertEqual(pr.ports, [3, 5])

        pr = B[:10:3]
        self.assertTrue(isinstance(pr, PortReference))
        self.assertEqual(pr.ports, [0, 3, 6, 9])

        pr = B[2:12:4]
        self.assertTrue(isinstance(pr, PortReference))
        self.assertEqual(pr.ports, [2, 6, 10])

        #slice input validation
        with self.assertRaises(ValueError): B[1:] #open ended
        with self.assertRaises(ValueError): B[:0] #starting at zero




    def test_reset(self):

        B = Block()

        B.inputs = {0:0, 2:2, 1:1}
        B.outputs = {1:1, 0:0, 2:2}

        B.reset()

        #test if inputs and outputs are reset correctly
        self.assertEqual(B.inputs, {0:0.0, 1:0.0, 2:0.0})
        self.assertEqual(B.outputs, {0:0.0, 1:0.0, 2:0.0})


    def test_set(self):

        B = Block()

        B.set(0, 1)
        self.assertEqual(B.inputs[0], 1)

        B.set(0, 2)
        self.assertEqual(B.inputs[0], 2)

        B.set(2, 3)
        self.assertEqual(B.inputs[2], 3)


    def test_get(self):

        B = Block()

        B.outputs = {0:0, 2:2, 1:1}

        self.assertEqual(B.get(0), 0)
        self.assertEqual(B.get(1), 1)
        self.assertEqual(B.get(2), 2)

        #undefined output -> defaults to 0.0
        self.assertEqual(B.get(100), 0.0)


    def test_update(self):

        B = Block()

        #test default implementation 
        self.assertEqual(B.update(None), 0.0)


    def test_solve(self):

        B = Block()

        #test default implementation 
        self.assertEqual(B.solve(None, None), 0.0)


    def test_step(self):

        B = Block()

        #test default implementation 
        self.assertEqual(B.step(None, None), (True, 0.0, 1.0))



# RUN TESTS LOCALLY ====================================================================

if __name__ == '__main__':
    unittest.main(verbosity=2)