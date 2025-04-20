# ##################################################################################################
#
#  Title
#
#   vecworks.retrievers.generic.py
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
#    Part of the Vecworks framework, implementing various generic classes for querying
#    vector indices.
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

import warnings

# Utilities
import re


# Third-party ######################################################################################

# NumPy
import numpy as np

# SciPy
import scipy.sparse


# First-party ######################################################################################

# pypeworks
from pypeworks import (
    Node
)

from pypeworks.typing import (
    Args,
    Param
)


# Local ############################################################################################

# vecworks.enums
from vecworks.enums import (
    ENSEMBLERS
)

# vecworks.index
from vecworks.index import (
    Index
)


# ##################################################################################################
# Classes
# ##################################################################################################

# Retriever ########################################################################################

class Retriever(Node):

    """
    Pypeworks Node providing access to a single vector index for similarity search.
    """

    # ##############################################################################################
    # Class fundamentals
    # ##############################################################################################

    # __init__ #####################################################################################

    def __init__(
            
        self,

        # Index specification
        index              : Index | list[Index],

        # Node
        **kwargs

    ):
        
        """
        Initializes the retriever. This must be invoked by an sub-class as part of initialization.

        Parameters
        ----------

        index
            Index to query for similarity.

        kwargs
            Any additional arguments to pass to the underlying Pypeworks `Node`.
        """
        
        # ##########################################################################################
        # Argument handling
        # ##########################################################################################

        # index ####################################################################################

        # Validate and store input, but only if that has not been done before.
        if not hasattr(self, "index"):

            # Validate input.
            if not isinstance(index, Index):
                
                raise ValueError(
                    f"Object op type '{type(index)}' was passed for 'index' where object of type"
                    f" 'vecworks.index.Index' was expected."
                )
            
            # Store input.
            self.index : Index = index


        # ##########################################################################################
        # Initialization
        # ##########################################################################################

        # Delegate to super class.
        super().__init__(self.exec, **kwargs)
        

        # End of '__init__' ########################################################################


    # ##############################################################################################
    # Methods
    # ##############################################################################################

    # exec #########################################################################################

    def exec(self, input : Any | Iterable, **kwargs):

        """
        Search the index for content similar to the given input.

        Parameters
        ----------

        input
            Input(s) to compare the index with for similarity.

        kwargs
            Any other arguments passed as part of the invocation of the method.
        """

        # Wrap scalars.
        wrapped : bool = False
        if np.isscalar(input):

            input = [input]
            wrapped = True

        # Vectorize as needed, and pass input to query to retrieve results.
        if self.index.vectorizer is not None:
            results = self.query(self.index.vectorizer.transform(input), **kwargs)

        else:
            results = self.query(input, **kwargs)

        # Add original input.
        results["input"] = input if wrapped is False else input[0]

        # Construct and return a pypeworks.Args object to annotate the result.
        return (
            Args(
                args = tuple(results.values()),
                params = Args.__class_getitem__(tuple([Param[Any, key] for key in results.keys()]))
            )
        )


        # End of method 'exec' #####################################################################

    
    # query ########################################################################################
        
    def query(
        self,
        input    : Iterable[np.ndarray | scipy.sparse.sparray | scipy.sparse.spmatrix],
        **kwargs
    ) -> dict[str, list[Any]]:
        
        """
        Search the index for a vector similar to the given vector(s). If the input is not yet
        vectorised, call :py:meth:`exec` instead.

        .. note::

            Any sub-class must re-implement this method to provide a fully functional retriever.

        Parameters
        ----------

        input
            Vectorized input(s).

        kwargs
            Any other arguments passed.
        """

        raise NotImplementedError(
            f"Interface '{self.__qualname__}' does not implement the 'query' method;"
        )
    
        # End of method 'query' ####################################################################

    # End of class 'Retriever' #####################################################################


# MultiIndexRetriever ##############################################################################

class MultiIndexRetriever(Retriever):

    """
    Interface implemented by all retrievers allowing to query multiple indices at the same time.
    """

    # ##############################################################################################
    # Class fundamentals
    # ##############################################################################################

    # __init__ #####################################################################################

    def __init__(
            
        self,

        # Index specification
        index          : Index | list[Index],

        # Return values
        return_rank_as : str | None           = None,
        
        # Filtering
        ensemble_by    : ENSEMBLERS | None    = None,         
        top_k          : int                  = 10,

        # Node
        **kwargs

    ):
        
        """
        Initializes the retriever. This must be invoked by an sub-class as part of initialization.

        Parameters
        ----------

        index
            Index or indices to query for similarity.

        return_rank_as
            Name to assign to the variable holding the rank.

        ensemble_by
            Ensembler to use to combine results from similarity queries. Refer to 
            :py:class:`vecworks.functions.ENSEMBLERS` for the available options.

        top_k
            Maximum number of results to retrieve per vector.

        kwargs
            Any additional arguments to pass to the underlying Pypeworks `Node`.
        """

        # ##########################################################################################
        # Argument handling
        # ##########################################################################################
        
        # index ####################################################################################

        # Predeclare member to hold index.
        self.index : list[Index] = None

        # Validate input.
        if isinstance(index, Index):
            self.index = [index]

        elif isinstance(index, list):

            # Check if list is not empty.
            if len(index) == 0:

                raise ValueError(
                    f"List passed to 'index' is empty; at least one index needs to be specified;" 
                )

            # Define variables to keep track of names already defined.
            idx_names   : set[str]       = set()
            idx_returns : dict[str, str] = dict()

            # Ensure that each list member refers to an Index object.
            for i, idx in enumerate(index):

                if not isinstance(idx, Index):

                    raise ValueError(
                        f"Object of type '{type(idx)}' was passed for 'index[{i}]' where object of"
                        f" type 'vecworks.index.Index' was expected;"
                    )
                
                # Check if there is no overlap with predefined names.
                if idx.name in idx_names:

                    raise ValueError(
                        f"Index with name '{idx.name}' is already defined;"
                    )
                
                idx_names.add(idx.name)

                # Register return name if it was specified (and unique).
                if idx.return_distance_as is None:
                    continue

                if idx.return_distance_as in idx_returns:

                    raise ValueError(
                        f"Return name '{idx.return_distance_as}' is already reserved by"
                        f" '{idx_returns[idx.return_distance_as]}'; specify another name;"
                    )
                
                idx_returns[idx.return_distance_as] = idx.name
                
            # Store input.
            self.index = index

        else:

            raise ValueError(
                f"Object of type '{type(index)}' was passed for 'index' where object of type"
                f" 'vecworks.index.Index' or 'list[vecworks.index.Index]' was expected;"
            )
        

        # return_rank_as ###########################################################################

        # Validate input.
        if isinstance(return_rank_as, str):

            # Validate that a valid name was passed.
            if re.match(r"^[^\d\W]", return_rank_as) is None:

                raise ValueError(
                    f"Name provided for 'return_rank_as', '{return_rank_as}', is invalid, not"
                    f" starting with letters (a-z, A-Z, unicode) or underscores;"
                )

            elif re.match(r"^\w+$", return_rank_as) is None:

                raise ValueError(
                    f"Name provided for 'return_rank_as', '{return_rank_as}', is invalid,"
                    f" containing characters other than letters (a-z, A-Z), numbers (0-9) or"
                    f" underscores;"
                )
            
        elif return_rank_as is not None:

            raise ValueError(
                f"Object of type '{type(return_rank_as)}' was passed for 'return_rank_as' where a"
                f" string was expected;" 
            )
        
        # Store input.
        self.return_rank_as : str | None = return_rank_as


        # ensemble_by ##############################################################################

        # Validate input.
        if isinstance(ensemble_by, ENSEMBLERS):
            pass

        elif ensemble_by is None:
            pass

        else:
            
            raise ValueError(
                f"Object of type '{type(ensemble_by)}' was passed for 'ensemble_by' where object of"
                f" type 'vecworks.functions.ENSEMBLERS' was expected;"
            )
        
        # Store input
        self.ensemble_by : ENSEMBLERS | None = ensemble_by
        

        # top_k ####################################################################################

        # Validate input.
        if not isinstance(top_k, int):

            raise ValueError(
                f"Expected integer for 'top_k', but '{type(top_k)}' was passed instead;"
            )

        # Store input.
        self.top_k : int = top_k


        # kwargs ###################################################################################

        # Block 'returns'.
        if "returns" in kwargs:

            warnings.warn(
                f"Argument was passed for 'returns'; argument is ignored as retrievers dynamically"
                f" generate return names;"
            )

            del kwargs["returns"]


        # ##########################################################################################
        # Initialization
        # ##########################################################################################

        # Super class ##############################################################################

        # Delegate to super class.
        super().__init__(
            index = index,
            **kwargs
        )


        # Set-up looku-up maps #####################################################################

        # Map to get index by bound name.
        self.bound_indices : dict[str, Index] = {idx.bind: idx for idx in self.index}

        # Map to get index by position.
        self.indices_by_pos : dict[int, Index] = {i: idx for i, idx in enumerate(self.index)}

        # Map to bound name by index name.
        self.index_aliases : dict[str, str] = {idx.name: idx.bind for idx in self.index}


        # End of '__init__' ########################################################################


    # ##############################################################################################
    # Methods
    # ##############################################################################################

    # exec #########################################################################################

    def exec(self, *args, **kwargs):

        """
        Search the index for content similar to the given input.

        Parameters
        ----------

        args
            Input(s) to compare the index with for similarity, passed without a name.

        kwargs
            Input(s) to compare the index with for similarity, passed with a name. Any arguments
            with a name that may not be mapped to an index, are passed as key-value arguments for
            use at the discretion of the retriever.
        """

        # ##########################################################################################
        # Argument handling
        # ##########################################################################################

        # Predeclare dictionary to hold mapped arguments and vectorized input.
        inputs            : dict = dict()
        inputs_vectorized : dict = dict()


        # args #####################################################################################

        # Iterate over each unnamed argument passed.
        for i, arg in enumerate(args):

            # Attempt to get an index for the given position.
            idx : Index = self.indices_by_pos.get(i, None)

            if idx is None:

                raise LookupError(
                    f"More inputs were specified ({i+1}) than that there are indices available"
                    f" ({len(self.indices_by_pos)})to query."
                )
            
            # Wrap scalars.
            if np.isscalar(arg):
                arg = [arg]

            # Store plain input.
            inputs[idx.name] = arg
            
            # Vectorize input.
            if idx.vectorizer is not None:

                # Handle list-likes as batches.
                inputs_vectorized[idx.name] = idx.vectorizer.transform(arg)

            else:
                inputs_vectorized[idx.name] = arg


        # kwargs ###################################################################################

        # Predeclare dictionary to hold key-value not referencing any indices.
        new_kwargs : dict = dict()

        # Iterate over each key-value argument passed.
        for key, arg in kwargs.items():

            # Ensure that arguments are not redefined.
            if key in inputs:

                raise LookupError(
                    f"An input was already provided for index '{key}';"
                )
            
            # Attempt to get an index for the given bound name.
            idx : Index = self.bound_indices.get(key, None)

            # Only consider an input if an associated index can be found.
            if idx is not None:

                # Wrap scalars.
                if np.isscalar(arg):
                    arg = [arg]

                # Store plain data.
                inputs[idx.name] = arg

                # Vectorize input.
                if idx.vectorizer is not None:
                    inputs_vectorized[idx.name] = idx.vectorizer.transform(arg)

                else:
                    inputs_vectorized[idx.name] = arg

            # Otherwise, keep the key-value pair separate.
            else:
                new_kwargs[key] = arg


        # ##########################################################################################
        # Delegation
        # ##########################################################################################

        # Retrieve results by delegating to query.
        results = self.query(inputs_vectorized, **new_kwargs)

        # Add original inputs.
        results = {

            **{
                self.index_aliases.get(key, key): value
                for key, value in inputs.items()
            }, 

            **results
        }

        # Construct and return a pypeworks.Args object to annotate the result.
        return (
            Args(
                args = tuple(results.values()),
                params = Args.__class_getitem__(tuple([Param[Any, key] for key in results.keys()]))
            )
        )
                

        # End of method 'exec' #####################################################################
        

    # query ########################################################################################
        
    def query(
        self,
        input    : dict[str, Iterable[np.ndarray | scipy.sparse.sparray | scipy.sparse.spmatrix]],
        **kwargs
    ) -> dict[str, list[list[Any]]]:
        
        """
        Search the index for a vector similar to the given vector(s). If the input is not yet
        vectorised, call :py:meth:`exec` instead.

        .. note::

            Any sub-class must re-implement this method to provide a fully functional retriever.

        Parameters
        ----------

        input
            Vectorized input(s) indexed by name.

        kwargs
            Any other arguments passed.
        """

        raise NotImplementedError(
            f"Interface '{self.__qualname__}' does not implement the 'query' method;"
        )
    
        # End of method 'query' ####################################################################

    # End of class 'MultiIndexRetriever' ###########################################################

# End of File ######################################################################################