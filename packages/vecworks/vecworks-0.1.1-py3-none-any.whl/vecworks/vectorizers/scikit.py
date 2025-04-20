# ##################################################################################################
#
#  Title
#
#    vecworks.vectorizers.scikit.py
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
#    Part of the Vecworks framework, implementing a wrapper for scikit-learn vectorizers.
#
# ##################################################################################################

# ##################################################################################################
# Dependencies
# ##################################################################################################

# Python standard library ##########################################################################

from typing import (
    Any,
    Callable,
    Iterable
)


# Third-party ######################################################################################

# NumPy
import numpy as np

# scikit-learn
import sklearn
import sklearn.pipeline

# SciPy
import scipy.sparse


# Local ############################################################################################

# vecworks.generic
from . import (
    generic
)


# ##################################################################################################
# Classes
# ##################################################################################################

# sklearnVectorizer ################################################################################

class sklearnVectorizer(generic.Vectorizer):

    """
    Wrapper class to ease use of scikit-learn vectorizers in Vecworks.
    """

    # ##############################################################################################
    # Class fundamentals
    # ##############################################################################################

    # __init__ #####################################################################################

    def __init__(
        self,
        vectorizer : sklearn.base.TransformerMixin | sklearn.pipeline.Pipeline       ,
        fit        : Iterable[str] | None                                      = None
    ):
        
        """
        Initializes the vectorizer.

        Parameters
        ----------

        vectorizer
            Sci-kit learn transformer to be used to vectorize the data. 

        fit
            Optional, data with which the transformer may be fit.
        """
        
        # ##########################################################################################
        # Argument handling
        # ##########################################################################################

        # vectorizer ###############################################################################

        # Create a clone of the vectorizer as to prevent side-effects.
        self.vectorizer : sklearn.base.TransformerMixin | sklearn.pipeline.Pipeline = (
            sklearn.base.clone(vectorizer)
        )


        # fit ######################################################################################

        # Fit the vectorizer to the given data.
        if fit is not None:
            self.vectorizer.fit(fit)


        # ##########################################################################################
        # Initialization
        # ##########################################################################################

        # Replace 'transform' function with vectorizer's transform function.
        self.transform : Callable[
            [Any | Iterable[Any]], np.ndarray | scipy.sparse.sparray
        ] = self.vectorizer.transform


        # End of '__init__' ########################################################################


    # ##############################################################################################
    # Methods
    # ##############################################################################################

    # transform ####################################################################################

    def transform(
        self, 
        input : Any | Iterable[Any]
    ) -> np.ndarray | scipy.sparse.sparray:

        """
        Vectorizes the given data.

        Also see: :py:class:`~vecworks.vectorizers.generic.Vectorizer`.
        """

        raise NotImplementedError(
            f"Vectorizer was incorrectly initialized;"
        )
    
        # End of method 'transform' ################################################################

    # End of class 'sklearnVectorizer' #############################################################

# End of File ######################################################################################