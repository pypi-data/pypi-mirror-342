# ##################################################################################################
#
#  Title
#
#    vecworks.vectorizers.fasttext.py
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
#    Part of the Vecworks framework, implementing a wrapper for fastText-based vectorizers.
#
# ##################################################################################################

# ##################################################################################################
# Dependencies
# ##################################################################################################

# Python standard library ##########################################################################

# Fundamentals
from types import (
    ModuleType
)

from typing import (
    Iterable,
    Literal
)

# Utilities
import os
import re


# Third-party ######################################################################################

# NumPy
import numpy as np


# Local ############################################################################################

# vecworks.generic
from . import (
    generic
)


# ##################################################################################################
# Classes
# ##################################################################################################

# fastTextModel ####################################################################################

class fastTextModel:

    """
    Placeholder class to typehint FastText models without needing to import a specific FastText
    package.
    """

    pass

    # End of class 'fastTextModel' #################################################################


# fastTextVectorizer ###############################################################################

class fastTextVectorizer(generic.Vectorizer):

    """
    Wrapper class to ease use of fastText-based vectorizers in Vecworks.
    """

    # ##############################################################################################
    # Class fundamentals
    # ##############################################################################################

    # __init__ #####################################################################################

    def __init__(
        self,
        model   : str | fastTextModel,
        backend : Literal["fasttext", "compress-fasttext"] = "fasttext",
        output  : Literal["word", "sentence"]              = "sentence"
    ):
        
        """
        Initializes the vectorizer.

        Parameters
        ----------

        model
            Either file path to a FastText model to load, or a loaded FastText model.

        backend
            The FastText implementation to use, one of:

            * `fasttext`, the `original fastText implementation <https://fasttext.cc/>`_ by 
              Facebook.

            * `compress-fasttext`, the implementation by `David Dale 
              <https://github.com/avidale/compress-fasttext>`_ developed to deploy compressed
              fastText models.

        output
            The kind of vector that needs to be generated, either a 'word' vector or a 'sentence'
            vector.
        """
        
        # ##########################################################################################
        # Argument handling
        # ##########################################################################################

        # backend ##################################################################################

        # Validate input.
        if backend not in ("fasttext", "compress-fasttext"):

            raise ValueError(
                f"Received '{backend}' for 'backend' where either 'fasttext' or 'compress-fasttext'"
                f" was expected;"
            )
        
        # Load backend.
        fasttext          : ModuleType = None
        compress_fasttext : ModuleType = None

        if backend == "fasttext":
            import fasttext

        else:
            import compress_fasttext
        
        # Store input.
        self.backend : Literal["fasttext", "compress-fasttext"] = backend
        

        # model ####################################################################################

        # Attempt to load the model if a string was passed.
        if isinstance(model, str):

            # Check if the string can be mapped to a file path.
            if not os.path.exists(model):

                raise FileNotFoundError(
                    f"No model found at '{model}';"
                )
            
            # Load the model using the assigned backend.
            if backend == "fasttext":
                self.model = fasttext.load_model(model)

            else:
                self.model = compress_fasttext.CompressedFastTextKeyedVectors.load(model)

        # Otherwise check that a valid model was passed, and store it if it is.
        else:

            # Validate the model.
            if backend == "fasttext":

                if not isinstance(model, fasttext.FastText._FastText):

                    raise ValueError(
                        f"Object of type '{type(model)}' was passed for 'model' where either a"
                        f" string or a fastText model was expected;"
                    )
                
            else:

                if not isinstance(model, compress_fasttext.CompressedFastTextKeyedVectors):

                    raise ValueError(
                        f"Object of type '{type(model)}' was passed for 'model' where either a"
                        f" string or a 'compress_fasttext.CompressedFastTextKeyedVectors' object"
                        f" was expected;"
                    )
                
            # Store the model.
            self.model = model


        # output ###################################################################################

        # Validate input.
        if output not in ("word", "sentence"):

            raise ValueError(
                f"Received '{output}' for 'output' where either 'word' or 'sentence' was expected;"
            )
        
        # Store input.
        self.output : Literal["word", "sentence"] = output

        # Adjust transform method based on desired output.
        if self.output == "word":
            self.transform = self.__ft_get_word_vector__

        else:

            if self.backend == "fasttext":
                self.transform = self.__ft_get_sentence_vector__

            else:
                self.transform = self.__cft_get_sentence_vector__


        # End of '__init__' ########################################################################


    # ##############################################################################################
    # Methods
    # ##############################################################################################

    # __ft_get_word_vector__ #######################################################################

    def __ft_get_word_vector__(
        self,
        input : str | Iterable[str]
    ) -> np.ndarray:
        
        """
        Calculates word vector for fastText models.

        This method is monkey patched as the `transform` method during initialization, depending on
        the settings chosen.
        """

        # Preparation ##############################################################################

        # Get direct reference to the vectorization function as to minimize execution time.
        vectorizer = self.model.__getitem__


        # Vectorization ############################################################################

        if isinstance(input, str):
            return vectorizer(input)
        
        elif hasattr(input, "__iter__"):
            return np.stack([vectorizer(i) for i in input])
        
        else:
            
            raise ValueError(
                f"Object of type '{type(input)}' was passed for 'input' where string or list of"
                f" string was expected;"
            )

        # End of method '__ft_get_word_vector__' ###################################################


    # __ft_get_sentence_vector__ ###################################################################

    def __ft_get_sentence_vector__(
        self,
        input : str | Iterable[str]
    ) -> np.ndarray:
        
        """
        Calculates word vector for fastText models.

        This method is monkey patched as the `transform` method during initialization, depending on
        the settings chosen.
        """

        # Preparation ##############################################################################

        # Get direct reference to the vectorization function as to minimize execution time.
        vectorizer = self.model.get_sentence_vector


        # Vectorization ############################################################################

        if isinstance(input, str):
            return vectorizer(input)
        
        elif hasattr(input, "__iter__"):
            return np.stack([vectorizer(i) for i in input])
        
        else:
            
            raise ValueError(
                f"Object of type '{type(input)}' was passed for 'input' where string or list of"
                f" string was expected;"
            )

        # End of method '__ft_get_word_vector__' ###################################################


    # __cft_get_sentence_vector__ ##################################################################

    def __cft_get_sentence_vector__(
        self,
        input     : str | Iterable[str],
        _splitter : re.Pattern          = re.compile(r"\s+") # Micro-optimization
    ) -> np.ndarray:
        
        """
        Calculates sentence vector for compress-fasttext models.

        This method is monkey patched as the `transform` method during initialization, depending on
        the settings chosen.
        """

        # Preparation ##############################################################################

        # Get direct reference to the vectorization function as to minimize execution time.
        vectorizer = self.model.get_sentence_vector


        # Vectorization ############################################################################

        if isinstance(input, str):
            return vectorizer(_splitter.split(input))
        
        elif hasattr(input, "__iter__"):
            return np.stack([vectorizer(_splitter.split(i)) for i in input])
        
        else:

            raise ValueError(
                f"Object of type '{type(input)}' was passed for 'input' where string or list of"
                f" string was expected;"
            )

        # End of method '__cft_get_sentence_vector__' ##############################################    

    # End of class 'fastTextVectorizer' ############################################################

# End of File ######################################################################################