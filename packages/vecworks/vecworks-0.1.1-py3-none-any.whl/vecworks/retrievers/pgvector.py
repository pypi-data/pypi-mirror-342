# ##################################################################################################
#
#  Title
#
#   vecworks.retrievers.pgvector.py
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
#    Part of the Vecworks framework, implementing a retriever using pgvector as the back-end.
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
import re
import urllib.parse


# Third-party ######################################################################################

# NumPy
import numpy as np

# SciPy
import scipy.sparse

# SqlAlchemy
import sqlalchemy
import sqlalchemy.event


# Local ############################################################################################

# vecworks.auth
from vecworks.auth import (
    Authenticator,
    AuthenticationDetails,
    UsernameCredentials
)

# vecworks.enums
from vecworks.enums import (
    DENSITY,
    DISTANCES,
    ENSEMBLERS
)

# vecworks.index
from vecworks.index import (
    Index
)

# vecworks.retrievers
from vecworks.retrievers.generic import (
    MultiIndexRetriever
)


# ##################################################################################################
# Classes
# ##################################################################################################

# Query ############################################################################################

class Query(str):

    """
    Companion class to :py:class:`pgVector`, used to annotate the contents of the `table` argument
    as representing a SQL query. 
    """

    pass

    # End of class 'Query' #########################################################################


# Retriever ########################################################################################

class pgvectorRetriever(MultiIndexRetriever):

    """
    Retriever using `pgvector <https://github.com/pgvector/pgvector>`_ as the backend.
    """

    # ##############################################################################################
    # Class fundamentals
    # ##############################################################################################

    # __init__ #####################################################################################

    def __init__(
        self,

        # Connection
        url                : str                                      ,
        table              : str | Query                              ,

        # Index specification
        index              : Index | list[Index]                      ,

        # Return values
        return_columns     : list[str] | dict[str, str] | None = None ,
        return_rank_as     : str | None                        = None ,

        # Filtering
        ensemble_by        : ENSEMBLERS | None                 = None ,
        top_k              : int                               = 10   ,

        # Miscellaneous
        authenticator      : Authenticator | None = None              ,

        **kwargs
    ):
        
        """
        Initializes the retriever.

        Parameters
        ----------

        url
            Connection URL of the PostgreSQL database to connect.

            Refer to the `SQLAlchemy documentation <https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls>`_
            for documentation on how to specify this URL.

        table
            Table against which similarity matching should be performed, defined either by the
            qualified name of the table, or a non-terminated SQL query. In case of the latter,
            annotate the argument with :py:class:`Query`.

        index
            Index or indices to query for similarity.

        return_columns
            Columns of the table specified by `table` to include in the results. If a dictionary is
            passed, the dictionaries values are treated as aliases, to be used when converting back
            to Python. If no columns are specified, all columns are returned.

        return_rank_as
            Name to assign to the return variable holding the similarity rank.

        ensemble_by
            Ensembler to use to combine results from similarity queries. Refer to 
            :py:class:`vecworks.functions.ENSEMBLERS` for the available options.

        top_k
            Maximum number of results to retrieve per vector.

        authenticator
            :py:class:`vecworks.auth.Authenticator` to use for authenticating against the
            database

        kwargs
            Any additional arguments to pass to the underlying Pypeworks `Node`.
        """
        
        # ##########################################################################################
        # Argument handling
        # ##########################################################################################        

        # url ######################################################################################

        # Parse URL.
        parsed_url = urllib.parse.urlparse(url, scheme = "postgresql")

        # Validate URL.
        if re.match(r"^postgresql(?:\+\w+)?$", parsed_url.scheme) is None:

            raise ValueError(
                f"URL with scheme '{parsed_url.scheme}' was passed, where 'postgresql' and"
                f" derivatives are allowed;"
            )
        
        if parsed_url.path.count("/") > 1:

            raise ValueError(
                f"URL specifies database name incorrectly: '{parsed_url.path[1:]}';"
            )
        
        # Store components.
        self.scheme   : str = parsed_url.scheme
        self.host     : str = parsed_url.hostname
        self.port     : int = parsed_url.port
        self.database : str = parsed_url.path[1:]


        # table -> table_query #####################################################################

        # Predeclare variable to hold the query to select the table.
        table_query : str = None
            
        # Handle input.
        if isinstance(table, str):

            # Check for queries.
            if isinstance(table, Query):

                # Ensure that queries do not terminate.
                if ";" in table:

                    raise ValueError(
                        "Query provided to 'table' contains ';' character;"
                    )
                
                # Store the query as-is, to be reused later.
                table_query = table

            # Check for names.
            else:

                # Ensure the name is valid.
                if re.match(

                    r"^"
                    r"(?:(?:\"[^\d\W][^\"]*?\")|(?:[^\d\W][^\.\"]*?))"
                    r"(?:\.(?:(?:\"[^\d\W][^\"]*?\")|(?:[^\d\W][^\.\"]*?)))?"
                    r"$", 
                    
                    table
                    
                ) is None:

                    raise ValueError(
                        f"Table name provided, '{table}', is invalid;"
                    )
                
                # Generate a query to select from the table with the given name.
                table_query = f"SELECT * FROM {table}"

        else:

            raise TypeError(
                f"Object of type {type(table)} was passed for 'table', where string or object of"
                " type 'Query' was expected;"
            )


        # return_columns ###########################################################################

        # Validate contents of any lists and dictionaries passed.
        if isinstance(return_columns, (list, dict)):

            # Ensure the names are valid.
            wrong_col : re.Match | None = next(
                (col for col in return_columns if re.match(r"^[^\d\W]", col) is None), None
            )

            if wrong_col is not None:

                raise ValueError(
                    f"Passed column with name '{wrong_col}' is invalid, not starting with letters"
                    f" (a-z, A-Z, unicode) or underscores;"
                )
            
            if isinstance(return_columns, list):
            
                # Check for odd symbols.
                wrong_col = next(
                    (col for col in return_columns if re.match(r"\W", col) is not None), None
                )

                if wrong_col is not None:

                    raise ValueError(
                        f"Passed column with name '{wrong_col}' contains characters that may not be"
                        f" used in Python; consider supplying a dictionary to provide an"
                        f" appropriate alias;"
                    )
                
            else:

                # Check for odd symbols.
                wrong_col = next(

                    (
                        name for name in return_columns.values() 
                        if re.match(r"\W", name) is not None
                    )
                    , 
                    None
                )

                if wrong_col is not None:

                    raise ValueError(
                        f"Passed alias with name '{wrong_col}' contains characters that may not be"
                        f" used in Python;"
                    )
                
        # Empty values are allowed.
        elif return_columns is None:
            pass

        else:

            raise TypeError(
                f"Object of type {type(return_columns)} was passed for 'return_columns', where a"
                f" list of strings, a dictionary, or None was expected;"
            )
        
        # Store input.
        self.return_columns : dict[str, str] = None

        if isinstance(return_columns, list):
            self.return_columns = {col:col for col in return_columns}

        elif isinstance(return_columns, dict):
            self.return_columns = return_columns

        else:
            self.return_columns = dict()
        

        # authenticator ############################################################################

        # Check if a callable was passed as authenticator.
        if authenticator is not None:
            
            if not callable(authenticator):

                raise ValueError(
                    f"Object of type '{type(authenticator)} was passed where callable was expected;"
                )

        # If no authenticator was specified, check if an authenticator needs to be created.
        else:
            
            if parsed_url.username is not None:
                authenticator = UsernameCredentials(parsed_url.username, parsed_url.password)


        # ##########################################################################################
        # Initialization
        # ##########################################################################################

        # Initialize super class ###################################################################

        # Delegate to MultiIndexRetriever.
        super().__init__(
            index          = index, 
            return_rank_as = return_rank_as,
            ensemble_by    = ensemble_by,
            top_k          = top_k,
            **kwargs
        )


        # Generate escaped names ###################################################################

        self.sql_names : dict[str, str] = {
            idx.name: re.sub(r"\W", "_", idx.name).lower()
            for idx in self.index
        }


        # Generate URL to connect with database ####################################################

        # Note: the URL is generated as to pass a safe URL to SQLAlchemy.

        # Generate access URL.
        url : str = (
            sqlalchemy.engine.URL.create(
                drivername = self.scheme,
                host       = next(iter(re.findall(r".+(?=\:)", self.host)), None),
                port       = next(iter(re.findall(r"(?<=\:)\d+$", self.host)), None),
                database   = self.database
            )
        )

        # Acquire database connection ##############################################################

        # Establish connection with database.
        self.db_engine = sqlalchemy.create_engine(url)

        # Monitor reconnections as to reinvoke the authenticator if needed.
        if authenticator is not None:

            @sqlalchemy.event.listens_for(self.db_engine, "do_connect")
            def receive_do_connect(
                dialect  : sqlalchemy.Dialect, 
                conn_rec : sqlalchemy.pool.ConnectionPoolEntry, 
                cargs    : tuple[Any, ...], 
                cparams  : dict[str, Any]
            ):

                # Retrieve authentication details by invoking the authenticator.
                new_credentials : AuthenticationDetails = authenticator(self)

                if new_credentials.username is not None:
                    cparams["user"] = new_credentials.username or cparams.get("user", None)

                # Replace connection parameters with newly retrieved authentication details.
                if new_credentials.token is not None:
                    cparams["token"] = new_credentials.token or cparams.get("token", None)

                if new_credentials.password is not None:

                    cparams["password"] = (
                        new_credentials.password
                        or new_credentials.token
                        or cparams.get("password", None)
                    )

                # End of inner function 'receive_do_connect' #######################################


        # Prepare query ############################################################################

        # Prepare conversion map to convert distance function names to operators used by pgvector.
        OPS : dict[DISTANCES, str] = {
            DISTANCES.cosine    : "<=>",
            DISTANCES.hamming   : "<~>",
            DISTANCES.jaccard   : "<%>",
            DISTANCES.l1        : "<+>",
            DISTANCES.l2        : "<->",
            DISTANCES.nip       : "<#>"
        }

        # Set-up conversion map to convert DENSITY enums to type definitions used by pgvector.
        DENSITY_MAP : dict[DENSITY, str] = {
            DENSITY.dense  : "vector",
            DENSITY.sparse : "sparsevec"
        }

        # Compose query.
        self.__query__ : sqlalchemy.TextClause = sqlalchemy.text(

            # CTEs #################################################################################

            f"WITH"

            # Table query
            f" docs AS ({table_query}),"

            # Index table query.
            f" indexed_docs AS (SELECT row_number() OVER () AS __vw_doc_idx__, * FROM docs),"

            # Vectors
            f" vectors AS ("
            f" SELECT __vw_vec_idx__::int, "
            +
            (
                ",".join((
                        # Handle inter-mixing of dense and sparse vectors.
                        f" (CASE "
                        f" WHEN {self.sql_names[idx.name]}__vec__::text ~ '^\\['"
                        f" THEN {self.sql_names[idx.name]}__vec__::vector"
                        f" ELSE {self.sql_names[idx.name]}__vec__::sparsevec"
                        f" END)::{DENSITY_MAP.get(idx.density, "vector")}"
                        f" AS {self.sql_names[idx.name]}__vec__" 
                        for idx in self.index
                ))
            )
            +
            f" FROM unnest(:vectors_idx,"
            +
            (
                ",".join((f":{self.sql_names[idx.name]}__vec__" for idx in self.index))
            )
            +
            f") AS t(__vw_vec_idx__,"
            +
            (
                ",".join((f"{self.sql_names[idx.name]}__vec__" for idx in self.index))
            )
            +
            f")"
            f"),"

            # Distances
            f" distances AS ("
            f" SELECT * FROM (" # filtered_by_distance
            f" SELECT *, "
            +
            (
                ", ".join((
                    f"rank() OVER ("
                    f" PARTITION BY __vw_vec_idx__"
                    f" ORDER BY {self.sql_names[idx.name]}__vw_dist__ ASC"
                    f") AS {self.sql_names[idx.name]}__vw_rank__"
                    for idx in self.index
                ))
            )
            +
            f" FROM (" # unfiltered_distances
            f" SELECT __vw_doc_idx__, __vw_vec_idx__, "
            +
            (
                ", ".join((
                    f"\"{idx.name}\" {OPS[idx.distance]} {self.sql_names[idx.name]}__vec__"
                    f" AS {self.sql_names[idx.name]}__vw_dist__"
                    for idx in self.index
                ))
            )
            +
            f" FROM indexed_docs, vectors"
            f") AS unfiltered_distances"
            +
            (
                " AND ".join(
                    f"{' WHERE ' if i == 0 else ''}"
                    f"{self.sql_names[idx.name]}__vw_dist__ <= {idx.max_distance}"
                    for i, idx in enumerate(
                        (idxx for idxx in self.index if idxx.max_distance is not None)
                    )
                )
            )
            +
            f") AS filtered_by_distance"
            +
            (
                " AND ".join(
                    f"{' WHERE ' if i == 0 else ''}"
                    f"{self.sql_names[idx.name]}__vw_rank__ <= {idx.top_k}"
                    for i, idx in enumerate(
                        (idxx for idxx in self.index if idxx.top_k is not None)
                    )
                )
            )
            +
            f")," # distances / filtered_by_rank

            # Selections
            f"selections AS (" 
            +
            (
                # Reciprocal Rank Fusion
                (
                    f" SELECT __vw_vec_idx__, __vw_doc_idx__"
                    f" FROM (" # rff_ranks
                    f" SELECT"
                    f" __vw_vec_idx__, __vw_doc_idx__,"
                    f" rank() OVER (PARTITION BY __vw_vec_idx__ ORDER BY rff DESC) AS rff_rank"
                    f" FROM (" # rff_scores
                    f" SELECT __vw_vec_idx__, __vw_doc_idx__,"
                    f" (" # rff
                    +
                    (
                        " + ".join((
                            f"(1 / (60 + {self.sql_names[idx.name]}__vw_rank__::float))"
                            for idx in self.index
                        ))
                    )
                    +
                    f") AS rff"
                    f" FROM distances"
                    f") AS rff_scores"
                    f") AS rff_ranks"
                    f" WHERE rff_rank <= {self.top_k}"
                ) 
                if self.ensemble_by == ENSEMBLERS.rrf else 
                # Default
                (
                    f"SELECT"
                    f" __vw_vec_idx__, __vw_doc_idx__,"
                    f" rank() OVER(PARTITION BY __vw_vec_idx__"
                    +
                    (
                        ", ".join(
                            f"{' ORDER BY ' if i == 0 else ''}"
                            f"{self.sql_names[idx.name]}__vw_rank__ ASC"
                            for i, idx in enumerate(self.index)
                        )
                    )
                    + 
                    f" ) AS __vw_rank__"
                    f" FROM distances"
                    f" ORDER BY __vw_rank__ ASC"
                ) 
                if self.ensemble_by is None else 
                (
                    ValueError
                )
            )
            +
            f") " # selections

            # Main query ###########################################################################

            f"("
            f" SELECT "

            # Vector index
            f" selections.__vw_vec_idx__,"

            # indexed_docs
            +
            (
                (
                    f"indexed_docs.*"
                )
                if return_columns is None else
                (
                    ",".join((f"indexed_docs.\"{col}\"" for col in return_columns))
                )
            )
            +

            # distances
            (
                (
                    ", ".join(
                        f"{', ' if i == 0 else ''}"
                        f"distances.{self.sql_names[idx.name]}__vw_dist__ AS {idx.return_distance_as}"
                        for i, idx in enumerate(
                            (idxx for idxx in self.index if idxx.return_distance_as is not None)
                        )
                    )
                )
            ) 
            +

            # ranking
            (
                (
                    f", selections.__vw_rank__ AS {return_rank_as}"
                )
                if return_rank_as is not None else
                (
                    ""
                )
            )

            +
            # Sources
            f" FROM selections"
            f" JOIN indexed_docs"
            f" ON selections.__vw_doc_idx__ = indexed_docs.__vw_doc_idx__"
            f" JOIN distances"
            f" ON selections.__vw_doc_idx__ = distances.__vw_doc_idx__"
            f" AND selections.__vw_vec_idx__ = distances.__vw_vec_idx__"
            f" ORDER BY selections.__vw_vec_idx__"
            +
            (
                ",".join(
                    f"{', ' if i == 0 else ''}"
                    f"{idx.return_distance_as}" 
                    for i, idx in enumerate(self.index)
                    if idx.return_distance_as is not None
                )
            )
            +
            f")" # Main query
        )

        # End of '__init__' ########################################################################


    # ##############################################################################################
    # Methods
    # ##############################################################################################

    # query ########################################################################################

    def query(
        self,
        input    : dict[str, Iterable[np.ndarray | scipy.sparse.sparray | scipy.sparse.spmatrix]],
        **kwargs
    ) -> dict[str, list[list[Any]]]:
        
        # ##########################################################################################
        # Retrieval
        # ##########################################################################################

        # Determine number of inputs.
        input_len : int = len(input[list(input.keys())[0]])

        # Prepare statement.
        statement = (
            
            self.__query__.bindparams(


                sqlalchemy.bindparam(
                    key   = "vectors_idx",
                    value = [i for i in range(0, input_len)],
                    type_ = sqlalchemy.ARRAY(sqlalchemy.Integer)
                ),

                # Stringified vector input.
                *[
                    sqlalchemy.bindparam(
                        
                        key = f"{self.sql_names[name]}__vec__",
                        
                        value = [
                            # Convert vector string.
                            to_str(vector)
                            # Using conversion function decided on by first vector in vector list.
                            for to_str in (

                                self.__generate_sparse_to_vec_converter__(vectors[0])
                                if scipy.sparse.issparse(vectors[0]) else 
                                self.__stringify_dense_vector__
                                
                                , # <- Keep comma
                            )
                            # Iterate over vectorized inputs.
                            for vector in vectors
                        ],

                        type_ = sqlalchemy.ARRAY(sqlalchemy.String)
                    )

                    for name, vectors in input.items()
                ],

                **kwargs

            )

        )

        # Begin a transaction.
        with self.db_engine.begin() as connection:
            sql_results : sqlalchemy.CursorResult = connection.execute(statement) 


        # ##########################################################################################
        # Processing
        # ##########################################################################################

        # Retrieve names of columns retrieved.
        columns    : list = [self.return_columns.get(key, key) for key in sql_results.keys()][1:]

        # Set-up lookup map to retrieve column name by column index.
        column_map : dict[int, str] = dict(enumerate(columns))

        # Reformat results into column like format.
        results : dict[str, list[list[Any]]] = {
            key: [list() for i in range(0, input_len)] for key in column_map.values()
        }

        for result in sql_results:
            for i, value in enumerate(result[1:]):
                results[column_map[i]][result[0]].append(value)

        # Return results.
        return results
        

        # End of method 'query' ####################################################################


    # __stringify_dense_vector__ ###################################################################

    def __stringify_dense_vector__(
        self,
        vector : np.ndarray
    ):
        
        """
        Converts a dense Numpy vector to a string representation as can be casted by pgvector into
        Postgres-native vector.
        """

        # If the vector includes any NaN-values, return a general NULL value.
        if np.isnan(np.sum(vector)):
            return None
        
        # Otherwise, stringify the vector.
        return "[" + (",".join(str(v) for v in vector)) + "]"
    
        # End of private method '__stringify_dense_vector__' #######################################

    
    # ___generate_stringify_sparse_vector_ #########################################################

    def __generate_stringify_sparse_vector__(
        self,
        sample : scipy.sparse.sparray | scipy.sparse.spmatrix
    ):
        
        """
        Generates a function to convert sparse matrices to strings based on given sample matrix.
        """

        # Convert matrix to COOrdinate format for consistent and fast processing.
        sample : scipy.sparse.coo_array | scipy.sparse.coo_matrix = sample.tocoo()
        
        # Only accept up to (semi-)one-dimensional matrices.
        if sample.ndim > 2 or (sample.ndim == 2 and sample.shape[0] != 1 and sample.shape[1] != 1):

            raise ValueError(
                f"Sparse matrix with shape '{sample.shape}' is not supported; only (1, x) and "
                f" (x, 1) matrices are supported;"
            )
        
        # Retrieve axis containing indices, and the maximum size of this axis.
        idx_dim : int = np.argmax(sample.shape)
        size    : int = int(sample.shape[idx_dim])

        # Generate function.
        return (
            lambda vector: (
                "{"
                +
                ",".join([
                    f"{int(i)+1}:{float(s)}" for i, s in zip(vector.coords[idx_dim], vector.data)
                ])
                +
                f"}}/{size}"
            ) if not np.isnan(np.sum(vector.data)) else None
        )
    
        # End of private method '__generate_stringify_sparse_vector_' ##############################

    # End of class 'pgvector' ######################################################################

# End of File ######################################################################################