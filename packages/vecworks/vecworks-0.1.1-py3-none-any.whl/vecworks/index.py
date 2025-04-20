# ##################################################################################################
#
#  Title
#
#   vecworks.index.py
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
#    Part of the Vecworks framework, implementing the Index class, used to specify how retrievers
#    may access indices of vector stores.
#
# ##################################################################################################

# ##################################################################################################
# Dependencies
# ##################################################################################################

# Python standard library ##########################################################################

# Utilities
import re


# Local ############################################################################################

# vecworks.enums
from vecworks.enums import (
    DENSITY,
    DISTANCES
)

# vecworks.vectorizers.generic
from vecworks.vectorizers.generic import (
    Vectorizer
)


# ##################################################################################################
# Classes
# ##################################################################################################

# Index ############################################################################################

class Index:

    """
    Data class specifying how a :py:class:`~vecworks.retrievers.generic.Retriever` may access an 
    index associated with a vector store.
    """

    # ##############################################################################################
    # Class fundamentals
    # ##############################################################################################

    # __init__ #####################################################################################

    def __init__(
            
        self,

        name               : str,
        distance           : DISTANCES    ,
        vectorizer         : Vectorizer | None = None,
        density            : DENSITY | None    = None,

        max_distance       : float | None      = None,
        top_k              : int   | None      = None,

        bind               : str | None        = None,
        return_distance_as : str | None        = None

    ):

        """
        Initializes the dataclass.

        Parameters
        ----------

        name
            Name of the vector index to access.

        distance
            Distance function, specified using :py:class:`~vecworks.enums.DISTANCES`, to
            calculate the similarity of the (vectorized) input passed to the retriever with the 
            indexed vectors.

        vectorizer
            Vectorizer used to vectorize input passed to the retriever. If no vectorizer is
            specified, the input will be kept as-is.

        density
            The density of the vectors stored in the index, as classified using 
            :py:class:`~vecworks.enums.DENSITY`.

        max_distance
            Maximum distance under which indices are still considered for selection. This value
            depends on the distance function applied. Refer to 
            :py:class:`~vecworks.enums.DISTANCES` for guidance.

        top_k
            Maximum number of hits to retrieve from the vector index. If neither `threshold` nor
            `top_k` are set, this parameter is automatically set to `10`.

        bind
            Name of the argument passed to the :py:class:`~vecworks.retrievers.Retriever`, which
            contents should be vectorized and compared with the index. If no name is passed, it is
            set to the contents of `name`.

        return_distance_as
            Name of the return variable holding the calculate distance. If no name is specified,
            the distance is not included in the output.
        """

        # ##########################################################################################
        # Argument handling
        # ##########################################################################################

        # name #####################################################################################

        # Validate input.
        if not isinstance(name, str):

            raise ValueError(
                f"Object op type '{type(name)}' was passed for 'name' where string was expected;"
            )
        
        # Store input.
        self.name : str = name


        # distance #################################################################################

        # Validate input.
        if not isinstance(distance, DISTANCES):

            raise ValueError(
                f"Object of type '{type(distance)}' was passed for 'distance' where object of type"
                f" 'vecworks.functions.DISTANCES' was expected;"
            )
        
        # Store input.
        self.distance : DISTANCES = distance


        # vectorizer ###############################################################################

        # Validate input
        if vectorizer is not None and not isinstance(vectorizer, Vectorizer):

            raise ValueError(
                f"Object of type '{type(vectorizer)}' was passed for 'vectorizer' where object of"
                f" type 'vecworks.vectorizer.Vectorizer' or 'None' was expected;"
            )
        
        # Store input.
        self.vectorizer : Vectorizer | None = vectorizer


        # density ##################################################################################

        # Validate input.
        if density is not None and not isinstance(density, DENSITY):

            raise ValueError(
                f"Object of type '{type(density)}' was passed for 'density' where object of type"
                f" 'vecworks.enums.DENSITY' or 'None' was expected;"
            )
        
        # Store input.
        self.density : DENSITY = density


        # max_distance, top_k ######################################################################

        # Fall back to default value top_k=10 in case neither max_distance or top_k are specified.
        if max_distance is None and top_k:
            top_k = 10
        
        # Store input.
        self.max_distance : float = max_distance
        self.top_k        : int   = top_k


        # bind #####################################################################################

        # Validate (optional) input.
        if bind is None:
            bind = name

        if isinstance(bind, str):

            # Validate that a valid name was passed.
            if re.match(r"^[^\d\W]", bind) is None:

                raise ValueError(
                    f"Name provided for 'bind', '{bind}', is invalid, not starting with letters"
                    f" (a-z, A-Z, unicode) or underscores;"
                )

            elif re.match(r"^\w+$", bind) is None:

                raise ValueError(
                    f"Name provided for 'bind', '{bind}', is invalid, containing characters other"
                    f" than letters (a-z, A-Z, unicode), numbers (0-9) or underscores;"
                )

        else:

            raise ValueError(
                f"Object of type 't{ype(bind)}' was passed for 'bind' where string or None was"
                f" expected;"
            )
        
        # Store input.
        self.bind : str = bind
        

        # return_distance_as #######################################################################

        # Validate (optional) input.
        if isinstance(return_distance_as, str):

            # Validate that a valid name was passed.
            if re.match(r"^[^\d\W]", return_distance_as) is None:

                raise ValueError(
                    f"Name provided for 'return_distance_as', '{return_distance_as}', is invalid,"
                    f" not starting with letters (a-z, A-Z) or underscores;"
                )

            elif re.match(r"^\w+$", return_distance_as) is None:

                raise ValueError(
                    f"Name provided for 'return_distance_as', 'return_distance_as', is invalid,"
                    f" containing characters other than letters (a-z, A-Z), numbers (0-9) or"
                    f" underscores;"
                )
            
        elif return_distance_as is None:
            pass # The argument is optional

        else:

            raise ValueError(
                f"Object of type '{type(return_distance_as)}' was passed for 'return_distance_as'"
                f" where string or None was expected;"
            )
        
        # Store input.
        self.return_distance_as : str | None = return_distance_as


        # End of 'init' ############################################################################

    # End of class 'Index' #########################################################################

# End of File ######################################################################################