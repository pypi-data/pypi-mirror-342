# ##################################################################################################
#
#  Title
#
#    vecworks.vectorizers.remote.py
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
#    Part of the Vecworks framework, implementing a client for interfacing with vectorizers
#    served using Vecworks' vectorizer server.
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

# Utilities
import base64


# Third-party ######################################################################################

# NumPy
import numpy as np

# Requests
import requests

# SciPy
import scipy.sparse

# Sparse
import sparse


# Local ############################################################################################

# vecworks.enums
from vecworks.enums import (
    DENSITY
)

# vecworks.servers.vectorizer.server
from vecworks.servers.vectorizer.server import (
    TransformRequest,
    TransformResponse
)

# vecworks.vectorizers.generic
from . import (
    generic
)


# ##################################################################################################
# Classes
# ##################################################################################################

# RemoteVectorizer ##################################################################################

class RemoteVectorizer(generic.Vectorizer):

    """
    Client for vectorizers served with Vecworks' vectorizer server.
    """

    # ##############################################################################################
    # Class fundamentals
    # ##############################################################################################

    # __init__ #####################################################################################

    def __init__(
            
        self,

        # Connection
        url           : str,
        vectorizer    : str | None = None
    ):
        
        """
        Initializes the vectorizer.

        Parameters
        ----------

        url
            URL of the service providing Vecworks' remote vectorizer API.

        vectorizer
            Alias of the vectorizer to access. If no alias is specified, the alias must be passed
            when :py:meth:`transform` is called.
        """
        
        # ##########################################################################################
        # Argument handling
        # ##########################################################################################

        # url, vectorizer ##########################################################################

        # Argument passthrough
        self.url           : str        = url
        self.vectorizer    : str | None = vectorizer


        # End of '__init__' ########################################################################


    # ##############################################################################################
    # Methods
    # ##############################################################################################

    # transform ####################################################################################

    def transform(
        self, 
        input      : Any | Iterable[Any],
        vectorizer : str | None = None
    ) -> np.ndarray | scipy.sparse.sparray | sparse.SparseArray:

        """
        Vectorizes the given data.

        Also see: :py:class:`~vecworks.vectorizers.generic.Vectorizer`.
        """

        # ##########################################################################################
        # Retrieve and parse response from remote server
        # ##########################################################################################

        # Retrieve response.
        http_response : requests.Response = (
            
            requests.post(
            
                f"{self.url}/v1/transform", 
                
                json = TransformRequest(
                    vectorizer = vectorizer or self.vectorizer,
                    input      = input,
                    kwargs     = dict()
                ).model_dump()
                
            )

        )

        # Check status of response.
        if http_response.status_code != 200:

            raise ConnectionError(
                f"Request to {self.url}/v1/transform failed with code"
                f" '{http_response.status_code}': {http_response.content};"
            )
        
        # Parse response.
        response : TransformResponse = TransformResponse(**http_response.json())


        # ##########################################################################################
        # Decode data
        # ##########################################################################################

        # Handle decoding differently based on density of the data.
        if response.density == DENSITY.dense:

            return (
                # Convert to NumPy array.
                np.frombuffer(
                    base64.b64decode(response.data), dtype = getattr(np, response.precision)
                )
                # Reshape into multi-dimensional array as needed.
                .reshape(response.shape)
            )
        
        elif response.density == DENSITY.sparse:

            # Decode to NumPy array.
            data : np.ndarray = (
                # Convert back to NumPy array.
                np.frombuffer(
                    base64.b64decode(response.data), dtype = getattr(np, response.precision)
                )
                # Reshape into original shape.
                .reshape(len(response.shape), -1)
            )

            # Restore sparse matrix.
            if len(response.shape) <= 2:

                # Convert to SciPy sparse array, and return.
                return scipy.sparse.coo_array((data[-1], data[:-1]), shape = response.shape)
            
            else:

                # Convert to Sparse COO array.
                return sparse.COO(data[:-1], data[-1], shape = response.shape)
    
        # End of method 'transform' ################################################################

    # End of class 'RemoteVectorizer' ##############################################################

# End of File ######################################################################################