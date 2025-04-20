# ##################################################################################################
#
#  Title
#
#    vecworks.vectorizers.openai.py
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
#    Part of the Vecworks framework, implementing a vectorizer using the OpenAI embedding API.
#
# ##################################################################################################

# ##################################################################################################
# Dependencies
# ##################################################################################################

# Python standard library ##########################################################################

# Fundamentals
import operator

from typing import (
    Any,
    Iterable
)

# Utilities
import base64


# Third-party ######################################################################################

# NumPy
import numpy as np

# OpenAI
import openai


# Local ############################################################################################

# vecworks.auth
from vecworks.auth import (
    Authenticator
)

# vecworks.vectorizers.generic
from . import (
    generic
)


# ##################################################################################################
# Classes
# ##################################################################################################

#OpenAIVectorizer ##################################################################################

class OpenAIVectorizer(generic.Vectorizer):

    """
    Wrapper class to ease use of services implementing the OpenAI embedding API.
    """

    # ##############################################################################################
    # Class fundamentals
    # ##############################################################################################

    # __init__ #####################################################################################

    def __init__(
            
        self,

        # Connection
        url           : str,
        model         : str,
        authenticator : Authenticator | None = None,

        # Configuration
        dimensions    : int | None           = None
    ):
        
        """
        Initializes the vectorizer.

        Parameters
        ----------

        == Connection

        url
            URL of the service providing an OpenAI-compatible API.

        model
            Name of the model. If no name is passed, the name must be specified when
            :py:meth:`transform` is called.

        authenticator
            Authenticator that may be used to acquire an authentication key when the external
            service requests for authentication.

        == Configuration

        dimensions
            The number of embeddings the resulting vector should have.
        """
        
        # ##########################################################################################
        # Argument handling
        # ##########################################################################################

        # url, model, authenticator ################################################################

        # Argument passthrough
        self.url           : str                  = url
        self.model         : str | None           = model
        self.authenticator : Authenticator | None = authenticator


        # dimensions ###############################################################################

        # Validate input.
        if not (isinstance(dimensions, int) or dimensions is None):

            raise ValueError(
                f"Object of type '{type(dimensions)}' was passed for 'dimensions' where object of"
                f" type 'int' or 'None' was expected;"
            )
        
        # Store input.
        self.dimensions : int = dimensions


        # ##########################################################################################
        # Initialization
        # ##########################################################################################

        # Acquire a client to interact with the API.
        self.client : openai.OpenAI = (
                openai.OpenAI(
                base_url = self.url, 
                api_key = (
                    self.authenticator().token if (
                        self.authenticator is not None
                    ) else "EMPTY"
                )
            )
        )


        # End of '__init__' ########################################################################


    # ##############################################################################################
    # Methods
    # ##############################################################################################

    # transform ####################################################################################

    def transform(
        self, 
        input : Any | Iterable[Any],
        model : str | None = None
    ) -> np.ndarray:

        """
        Vectorizes the given data.

        Also see: :py:class:`~vecworks.vectorizers.generic.Vectorizer`.
        """

        # Retrieve a response from the API.
        response : openai.types.CreateEmbeddingResponse = (

            self.client.embeddings.create(
                input           = input,
                model           = model or self.model,
                dimensions      = self.dimensions,
                encoding_format = "base64"
            )

        )

        if response is None:

            raise ConnectionError(
                f"Response could not be acquired from '{self.url}';"
            )

        # Adapt to format required by Vecworks, and return result.
        return (
            np.array([

                np.frombuffer(base64.b64decode(embedding), dtype = np.float32)

                for _, embedding in sorted(
                    ((data.index, data.embedding) for data in response.data),
                    key = operator.itemgetter(0)
                )

            ])
        )
    
        # End of method 'transform' ################################################################

    # End of class 'OpenAIVectorizer' ##############################################################

# End of File ######################################################################################