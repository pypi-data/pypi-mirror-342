#########################################################################################
##
##                        TIME DOMAIN DELAY BLOCK (blocks/delay.py)
##
##                                Milan Rother 2024
##
#########################################################################################

# IMPORTS ===============================================================================

import numpy as np

from ._block import Block
from ..utils.adaptivebuffer import AdaptiveBuffer


# BLOCKS ================================================================================

class Delay(Block):
    """Delays the input signal by a time constant 'tau' in seconds
    using an adaptive rolling buffer.

    Mathematically this block creates a time delay of the input signal like this:

    .. math::
    
        y(t) = 
        \\begin{cases}
        x(t - \\tau) & , t \\geq \\tau \\\\
        0            & , t < \\tau
        \\end{cases}


    Example
    -------
    The block is initialized like this:

    .. code-block:: python
        
        #5 time units delay
        D = Delay(tau=5)

    
    Parameters
    ----------
    tau : float
        delay time constant


    Attributes
    ----------
    _buffer : AdaptiveBuffer
        internal interpolatable adaptive rolling buffer

    """

    def __init__(self, tau=1e-3):
        super().__init__()

        #time delay in seconds 
        self.tau = tau

        #create adaptive buffer
        self._buffer = AdaptiveBuffer(self.tau)


    def __len__(self):
        #no passthrough by definition
        return 0


    def reset(self):
        #reset inputs and outputs
        self.inputs  = {0:0.0}  
        self.outputs = {0:0.0}

        #clear the buffer
        self._buffer.clear()


    def update(self, t):
        """Evaluation of the buffer at different times.

        Parameters
        ----------
        t : float
            evaluation time

        Returns
        -------
        error : float
            deviation to previous iteration for convergence control
        """

        #retrieve value from buffer
        _out, self.outputs[0] = self.outputs[0], self._buffer.get(t)
        return abs(_out - self.outputs[0])


    def sample(self, t):
        """Sample input values and time of sampling 
        and add them to the buffer.

        Parameters
        ----------
        t : float
            evaluation time for sampling
        """

        #add new value to buffer
        self._buffer.add(t, self.inputs[0])