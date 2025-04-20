# ##################################################################################################
#
#  Title
#
#   vecworks.auth.py
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
#    Part of the Vecworks framework, implementing various utilities for dealing with 
#    authentication against external external resources.
#
# ##################################################################################################

# ##################################################################################################
# Dependencies
# ##################################################################################################

# Python standard library ##########################################################################

# Fundamentals
from dataclasses import (
    dataclass,
    field
)

from typing import (
    Callable
)


# Local ############################################################################################

# vecworks.retriever.
from vecworks.retrievers.generic import (
    Retriever
)

# vecworks.vectorizers
from vecworks.vectorizers.generic import (
    Vectorizer
)


# ##################################################################################################
# Classes
# ##################################################################################################

# AuthenticationDetails ############################################################################

@dataclass
class AuthenticationDetails:

    """
    Holds authentication details that may be retrieved by an :py:type:`Authenticator`.
    """

    username : str | None = field(default = None)
    """
    Username with which to authenticate against the external resource.
    """

    password : str | None = field(default = None)
    """
    Password with which to authenticate against the external resource.
    """

    token    : str | None = field(default = None)
    """
    Access token with which to authenticate against the external resource.
    """

    # End of dataclass 'AuthenticationDetails' #####################################################


# ##################################################################################################
# Types
# ##################################################################################################

# Authenticator ####################################################################################

type Authenticator = Callable[[Retriever | Vectorizer], AuthenticationDetails]
"""
Callable invoked by an :py:class:`~vecworks.retrievers.Retriever` or an 
:py:class`~vecworks.vectorizers.Vectorizer` when seeking access to an external resource.
"""


# ##################################################################################################
# Functions
# ##################################################################################################

# UsernameCredentials ##############################################################################

def UsernameCredentials(username : str, password : str | None = None) -> AuthenticationDetails:

    """
    Generates an :py:type:`Authenticator` that generates authentication details with the given
    username and password.

    Parameters
    ----------

    username
        Username with which to authenticate against the external resource.

    password
        Password with which to authenticate against the external resource.
    """

    return lambda _: AuthenticationDetails(username, password)

    # End of function 'UsernameCredentials' ########################################################


# TokenCredentials #################################################################################

def TokenCredentials(token : str = None)  -> AuthenticationDetails:

    """
    Generates an :py:type:`Authenticator` that generates authentication details with the given
    token

    Parameters
    ----------

    token
        Token with which to authenticate against the external resource.
    """

    return lambda _: AuthenticationDetails(token = token)

    # End of function 'TokenCredentials' ###########################################################

# End of File ######################################################################################