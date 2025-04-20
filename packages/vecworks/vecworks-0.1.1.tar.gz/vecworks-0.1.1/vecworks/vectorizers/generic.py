# ##################################################################################################
#
#  Title
#
#   vecworks.vectorizers.generic.py
#
#  License
#
#    Copyright 2025 Rosaia B.V.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file 
#    except in compliance with the License. You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software distributed under the 
#    License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, 
#    either express or implied. See the License for the specific language governing permissions and 
#    limitations under the License.
#
#    [Apache License, version 2.0]
#
#  Description
#
#    Part of the Vecworks framework, implementing various generic classes specifying interfaces
#    for vectorizers.
#
# ##################################################################################################

# ##################################################################################################
# Dependencies
# ##################################################################################################

# Python standard library ##########################################################################

# Fundamentals
from typing import (
    Any,
    Iterable
)


# Third-party ######################################################################################

# NumPy
import numpy as np

# SciPy
import scipy.sparse

# Sparse
import sparse


# ##################################################################################################
# Classes
# ##################################################################################################

class Vectorizer:

    """
    Interface to a 'vectorizer', a processing unit that converts input to vector data.
    """

     ###############################################################################################
    # Methods
    # ##############################################################################################

    # transform ####################################################################################

    def transform(
        self, 
        input : Any | Iterable[Any]
    ) -> np.ndarray | scipy.sparse.sparray | sparse.SparseArray:

        """
        Vectorizes the given data.

        Parameters
        ----------

        input
            Data to vectorize.
        """

        raise NotImplementedError(
            f"Sub-class does not implement transform method.;"
        )
    
        # End of method 'transform' ################################################################

    # End of class 'Vectorizer' ####################################################################

# End of File ######################################################################################