# ##################################################################################################
#
#  Title
#
#    vecworks.vectorizers.sbert.py
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
#    Part of the Vecworks framework, implementing a wrapper for sentence-transformers.
#
# ##################################################################################################

# ##################################################################################################
# Dependencies
# ##################################################################################################

# Python standard library ##########################################################################

# Fundamentals
from typing import (
    Any,
    Iterable,
    Literal
)


# Third-party ######################################################################################

# NumPy
import numpy as np

# scikit-learn
import sentence_transformers as sbert


# Local ############################################################################################

# vecworks.generic
from . import (
    generic
)


# ##################################################################################################
# Classes
# ##################################################################################################

# sbertVectorizer ##################################################################################

class sbertVectorizer(generic.Vectorizer):

    """
    Wrapper class to ease use of sentence-transformers vectorizers in Vecworks.
    """

    # ##############################################################################################
    # Class fundamentals
    # ##############################################################################################

    # __init__ #####################################################################################

    def __init__(
            
        self,

        # Transformer
        transformer          : sbert.SentenceTransformer,
            
        # Encoding parameters    ,
        prompt_name          : str | None = None,
        batch_size           : int        = 32,

        precision            : Literal["float32", "int8", "uint8", "binary", "ubinary"] = "float32",
        normalize            : bool       = False,

        device               : str        = None,
    ):
        
        """
        Initializes the vectorizer.

        Parameters
        ----------

        transformer
            `SentenceTransformer <https://sbert.net/docs/package_reference/sentence_transformer/SentenceTransformer.html>`_
            to be used to vectorize the data. 

        prompt_name
            The name of prompt to use for encoding, as specified using the `prompts` parameters
            during the initialization of the transformer.

        batch_size
            The number of sentences to pass simultaneously to the transformer.

        precision
            The precision to use during the vectorization process. Generally, the more accurate,
            the better the accuracy, but at the cost of slower execution.

        normalize
            Whether to normalize the vectors output by the transformer.

        device
            `torch.device` to use for computation.
        """
        
        # ##########################################################################################
        # Argument handling
        # ##########################################################################################

        # transformer ##############################################################################

        # Store a reference to the transformer.
        self.transformer : sbert.SentenceTransformer = transformer


        # prompt_name, batch_size, precision, normalize_embeddings #################################

        # Argument passthrough.
        self.prompt_name : str   = prompt_name
        self.batch_size  : int   = batch_size
        self.precision   : float = precision
        self.normalize   : bool  = normalize
        self.device      : str   = device


        # End of '__init__' ########################################################################


    # ##############################################################################################
    # Methods
    # ##############################################################################################

    # transform ####################################################################################

    def transform(
        self, 
        input : Any | Iterable[Any]
    ) -> np.ndarray:

        """
        Vectorizes the given data.

        Also see: :py:class:`~vecworks.vectorizers.generic.Vectorizer`.
        """

        # Delegate to transformer.
        return (
            self.transformer.encode(
                sentences            = input if isinstance(input, str) else list(input),
                prompt_name          = self.prompt_name,
                batch_size           = self.batch_size,
                output_value         = "sentence_embedding",
                precision            = self.precision,
                normalize_embeddings = self.normalize,
                convert_to_numpy     = True,
                device               = self.device
            )
        )
    
        # End of method 'transform' ################################################################


    # ##############################################################################################
    # Static methods
    # ##############################################################################################

    # create_from_string ###########################################################################

    @staticmethod
    def create_from_string(

        model_name_or_path   : str,

        # Encoding parameters    ,
        prompt_format        : str | None = None,
        batch_size           : int        = 32,

        precision            : Literal["float32", "int8", "uint8", "binary", "ubinary"] = "float32",
        normalize            : bool       = False,
        truncate_dim         : int | None = None,

        device               : str        = None,

        # Retrievel parameters
        local_files_only     : bool       = False,
        trust_remote_code    : bool       = False,
        token                : str | None = None,
        

    ) -> type["sbertVectorizer"]:
        
        """
        Initializes a SentenceTransformer from a string defining a file path or HuggingFace model,
        and uses this transformer to initialise an instance of `sbertVectorizer`.

        Parameters
        ----------

        model_name_or_path
            File path to the on-disk model, or otherwise the name of a HuggingFace model.

        prompt_format
            Prompt format to apply to queries.

        batch_size
            The number of sentences to pass simultaneously to the transformer.

        precision
            The precision to use during the vectorization process. Generally, the more accurate,
            the better the accuracy, but at the cost of slower execution.

        normalize
            Whether to normalize the vectors output by the transformer.

        truncate_dim
            The dimensions to truncate vectors to.

        device
            `torch.device` to use for computation.

        local_files_only
            Whether or not to only look at local files for loading models.

        trust_remote_code
            Whether or not to allow any remotely downloaded models from executing local code.

        token
            HuggingFace authentication token to download gated models.
        """
        
        return sbertVectorizer(
        
            # Initialize the transformer.
            sbert.SentenceTransformer(

                model_name_or_path,

                prompts           = {"query": prompt_format} if prompt_format is not None else None,

                truncate_dim      = truncate_dim,

                device            = device,

                local_files_only  = local_files_only,
                trust_remote_code = trust_remote_code,
                token             = token

            ),

            # Initialize the vectorizer.
            prompt_name = "query",
            batch_size  = batch_size,

            precision   = precision,
            normalize   = normalize,

            device      = device

        )
        
        # End of static method 'create_from_string' ################################################


    # __init_cli__ #################################################################################

    # Constructor used by the server.
    __init_cli__ = create_from_string

    # End of class 'sbertVectorizer' ###############################################################

# End of File ######################################################################################