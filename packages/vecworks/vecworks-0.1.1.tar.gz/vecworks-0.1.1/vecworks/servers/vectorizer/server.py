# ##################################################################################################
#
#  Title
#
#   vecworks.servers.vectorizer.server.py
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
#    Part of the Vecworks framework, implementing a server to remotely service vectorizers.
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

import threading

from typing import (
    Annotated,
    Any,
    Callable,
    Literal,
    Sequence
)

# Utilities
import base64
import os
import ssl



# Third-party ######################################################################################

# FastAPI
import fastapi
import fastapi.middleware
import fastapi.middleware.cors

# NumPy
import numpy as np

# Pydantic
import pydantic

# SciPy
import scipy.sparse

# Sparse
import sparse

# Uvicorn
import uvicorn


# Local ############################################################################################

# vecworks.enums
import vecworks.enums

# vecworks.vectorizers
from vecworks.vectorizers import (
    Vectorizer
)


# ##################################################################################################
# Classes
# ##################################################################################################

# Utilities ########################################################################################

### CLIArgument ####################################################################################

@dataclass
class CLIArgument:

    """
    Utility class used to specify CLI arguments for server configuration optinos. 
    """

    aliases  : Sequence[str] = field(default = None)
    help     : str           = field(default = None)

    # End of dataclass 'CLIArgument' ###############################################################


### ServerConfig ###################################################################################

@dataclass
class ServerConfig:

    """
    Details how the vectorizer service should be configured.
    """

    # ##############################################################################################
    # Connection
    # ##############################################################################################

    # host #########################################################################################

    # Definition
    host : Annotated[
        
        str,

        CLIArgument(

            ("--host", ),

            help = (
                "Host to bind to"
            )
        )

    ] = field(default = "127.0.0.1")

    # Documentation
    """
    Host to bind to.
    """


    # port #########################################################################################

    # Definition
    port : Annotated[

        int,

        CLIArgument(

            ("-p", "--port"),

            help = (
                "Port to bind to"
            )
        )
    ] = field(default = 8000)

    # Documentation
    """
    Port to bind to.
    """


    # SSL ##########################################################################################

    # ssl_keyfile ##################################################################################

    # Definition
    ssl_keyfile : Annotated[
        
        str | None,

        CLIArgument(

            ("--ssl-keyfile", ),

            help = (
                "Path to the SSL key file"
            )
        )
    ] = field(default = None)

    # Documentation
    """
    Path to the SSL key file.
    """


    # ssl_keyfile_password #########################################################################

    # Definition
    ssl_keyfile_password : Annotated[
        
        str | None,

        CLIArgument(

            ("--ssl-keyfile-password", ),

            help = (
                "Password with which the SSL key file may be decrypted"
            )
        )

    ] = field(default = None)

    # Documentation
    """
    Password with which the SSL key file may be decrypted.
    """


    # ssl_certfile #################################################################################

    # Definition
    ssl_certfile : Annotated[
        
        str | os.PathLike | None,

        CLIArgument(

            ("--ssl-certfile", ),

            help = (
                "Path to the SSL cert file"
            )
        )
         
     ] = field(default = None)
    
    # Documentation
    """
    Path to the SSL cert file.
    """


    # ssl_ca_certs #################################################################################

    # Definition
    ssl_ca_certs : Annotated[
        
        str | None,

        CLIArgument(

            ("--ssl-ca-certs", ),

            help = (
                "Path to file containing list of root certificates issued by certification"
                " authorities"
            )
        )
                       
    ]  = field(default = None)

    # Documentation
    """
    Path to file containing list of root certificates issued by certification authorities.
    """


    # ssl_cert_reqs ################################################################################

    # Definition
    ssl_cert_reqs : Annotated[
        
        int,
                              
        CLIArgument(

            ("--ssl-cert-reqs", ),

            help = (
                "Specifies whether peers' certificates are validated, and how to behave if"
                " verification fails"
            )
        )

    ] = field(default = ssl.CERT_NONE)

    # Documentation
    """
    Specifies whether peers' certificates are validated, and how to behave if verification fails.
    """


    # ssl_ciphers ##################################################################################

    # Definition
    ssl_ciphers : Annotated[
        
        str, 

        CLIArgument(

            ("--ssl-ciphers", ),

            help = (

            )
        )
                              
    ] = field(default = "TLSv1")

    # Documentation
    """
    Ciphers available for the socket to use
    """


    # CORS #########################################################################################

    # cors_allowed_origins #########################################################################

    # Definition
    cors_allowed_origins : Annotated[
        
        Sequence[str],
                    
        CLIArgument(

            ("--cors-allowed-origins", ),

            help = (
                "A list of origins that should be permitted to make cross-origin requests"
            )
        )
                    
    ] = field(default = ())

    # Documentation
    """
    A list of origins that should be permitted to make cross-origin requests.
    """


    # cors_allow_credentials #######################################################################

    # Definition
    cors_allow_credentials : Annotated[
        
        bool,
        
        CLIArgument(

            ("--cors-allow-credentials", ),

            help = (
                "Whether cookies are supported for cross-origin requests"
            )
        )
        
    ] = field(default = False)

    # Documentation
    """
    Whether cookies are supported for cross-origin requests.
    """


    # cors_allowed_methods #########################################################################

    # Definition
    cors_allowed_methods : Annotated[
        
        Sequence[str],
                    
        CLIArgument(

            ("--cors-allowed-methods", ),

            help = (
                "A list of HTTP methods that should be allowed for cross-origin requests"
            )
        )
                    
    ] = field(default = ("GET",))

    # Documentation
    """
    A list of HTTP methods that should be allowed for cross-origin requests.
    """


    # cors_allowed_headers #########################################################################

    # Definition
    cors_allowed_headers : Annotated[
        
        Sequence[str],
                    
        CLIArgument(

            ("--cors-allowed-headers", ),

            help = (
                "A list of HTTP request headers that should be supported for cross-origin requests"
            )
        )
                    
    ] = field(default = ())

    # Documentation
    """
    A list of HTTP request headers that should be supported for cross-origin requests
    """


    # ##############################################################################################
    # System
    # ##############################################################################################

    # log_level ####################################################################################

    # Definition
    log_level : Annotated[

        str | int | None,

        CLIArgument(

            ("--log-level", ),

            help = (
                "The minimal event level that should be logged."
            )

        )

    ] = field(default = "info")

    # Documentation
    """
    The minimal event level that should be logged.
    """

    # End of dataclass 'ServerConfig' ##############################################################


### VectorizerInitializationDetails ################################################################

@dataclass
class VectorizerInitializationDetails:

    """
    Provides guidance on how to initialize vectorizers.
    """

    initializer : Callable[[Any], Vectorizer] = field(default = None)
    """
    Callable to invoke to initialize the vectorizer.
    """

    kwargs : dict[str, Any] = field(default_factory = dict)
    """
    Arguments to pass to the initializer when the vectorizer needs to be initialized.
    """

    # End of typed dictionary 'VectorizerInitializationDetails' ####################################

# Protocol #########################################################################################

### ErrorResponse ##################################################################################

class ErrorResponse(pydantic.BaseModel):

    """
    Response given by the server when it encouters an error.
    """

    message : str
    """
    Description of the error encountered.
    """

    # End of class 'ErrorResponse' #################################################################


### TransformRequest ###############################################################################

class TransformRequest(pydantic.BaseModel):

    """
    Details arguments taken by the `/v1/transform` endpoint.
    """

    vectorizer : str
    """
    Alias of the vectorizer to which the input should be passed.
    """

    input      : str | list[str]
    """
    Input(s) to compare the index with for similarity.
    """

    kwargs     : dict[str, Any]
    """
    Any other arguments passed as part of the invocation of the method.
    """

    # End of class 'TransformRequest' ##############################################################


### TransformResponse ##############################################################################

class TransformResponse(pydantic.BaseModel):

    """
    Details contents of response generate by the `/v1/transform` endpoint.
    """

    data      : bytes
    """
    Vectorized data, returned in base64.
    """

    density   : vecworks.enums.DENSITY
    """
    Density of the vectors returned, as described using :py:class:`vecworks.enums.DENSITY`.
    """

    precision : Literal["float64", "float32", "int8", "uint8", "binary", "ubinary"]
    """
    The precision of the vectors returned.
    """

    shape     : tuple[int, ...]
    """
    The dimensions of the vectors returned.
    """

    # End of class 'TransformResponse' #############################################################


# Server ###########################################################################################

class Server:

    """
    Server to remotely service vectorizers implementing the interface defined by 
    :py:class:`vecworks.vectorizers.generic.Vectorizer`.
    """

    # ##############################################################################################
    # Class fundamentals
    # ##############################################################################################

    def __init__(
        self,
        initializers : dict[str, VectorizerInitializationDetails],
        config       : ServerConfig                               = ServerConfig()
    ):
        
        """
        Initializes the server. To run it invoke :py:meth:`run`.

        Parameters
        ----------
        
        initializers
            Provides initialization details of the vectorizers to service, each indexed using an
            alias.

        config
            Specifies how to configure the server.
        """
        
        # ##########################################################################################
        # Argument handling
        # ##########################################################################################

        # Argument passthrough #####################################################################

        self.config       : ServerConfig                               = config
        self.initializers : dict[str, VectorizerInitializationDetails] = initializers


        # ##########################################################################################
        # Initialization
        # ##########################################################################################

        # Set-up resources #########################################################################

        ### Vectorizer cache #######################################################################

        # Create cache to hold initialized vectorizers.
        self.vectorizers : dict[str, Vectorizer] = dict() # TODO: preinit

        # Create locks to govern access to the cache.
        self.vectorizers_lock      : threading.Lock = threading.Lock()

        self.vectorizers_init_lock : dict[str, threading.Lock] = {
            alias: threading.Lock() for alias in self.initializers.keys()
        }


        # Set-up API routes ########################################################################

        # Initialize router.
        self.router : fastapi.APIRouter = fastapi.APIRouter()

        # Add routes.
        self.router.add_api_route("/v1/transform", self.v1_transform, methods = {"POST"})
        
        
        # Set-up FastAPI app #######################################################################

        # Initialize the app instance.
        self.app : fastapi.FastAPI = fastapi.FastAPI(
            title = "Vecworks remote vectorizer"
        )

        # Add routes.
        self.app.include_router(self.router)

        # Add middlewares
        self.app.add_middleware(
            fastapi.middleware.cors.CORSMiddleware,
            allow_origins     = config.cors_allowed_origins,
            allow_credentials = config.cors_allow_credentials,
            allow_methods     = config.cors_allowed_methods,
            allow_headers     = config.cors_allowed_headers
        )
    
        # End of '__init__' ########################################################################


    # ##############################################################################################
    # Methods
    # ##############################################################################################

    # run ##########################################################################################

    def run(self):
        
        """
        Runs the server.
        """

        # ##########################################################################################
        # Preparation
        # ##########################################################################################

        # Prepare server configuration.
        config : uvicorn.Config = (
            
            uvicorn.Config(

                self.app,

                log_level            = self.config.log_level,

                host                 = self.config.host,
                port                 = self.config.port,

                ssl_keyfile          = self.config.ssl_keyfile,
                ssl_keyfile_password = self.config.ssl_keyfile_password,
                ssl_certfile         = self.config.ssl_certfile,
                ssl_ca_certs         = self.config.ssl_ca_certs,
                ssl_cert_reqs        = self.config.ssl_cert_reqs,
                ssl_ciphers          = self.config.ssl_ciphers
            )

        )

        # Initialize the server.
        server : uvicorn.Server = uvicorn.Server(config)

        # ##########################################################################################
        # Run the server
        # ##########################################################################################

        server.run()


        # End of method 'run' ######################################################################


    # ##############################################################################################
    # API
    # ##############################################################################################

    # /v1/transform (transform) ####################################################################

    async def v1_transform(
        self, 
        request : TransformRequest
    ) -> ErrorResponse | TransformResponse:

        """
        Maps to `/v1/transform`.
        
        Vectorizes the given data.

        Analog to :py:meth:`vecworks.vectorizers.generic.Vectorizer.transform`.
        """

        # ##########################################################################################
        # Retrieve vectorizer
        # ##########################################################################################

        # Check if a vectorizer with the given alias was registered.
        if request.vectorizer not in self.initializers:

            return fastapi.responses.JSONResponse(

                ErrorResponse(
                    message = f"Vectorizer with alias '{request.vectorizer}' is not available;"
                ).model_dump(),

                status_code = 400
            )

        # Predeclare variable to hold reference to vectorizer.
        vectorizer             : Vectorizer = None

        # Predeclare variable to keep track of whether the vectorizer has been initialized.
        vectorizer_initialized : bool = True

        # Attempt to retrieve the vectorizer from the cache.
        with self.vectorizers_lock:

            try:

                # Retrieve the vectorizer.
                vectorizer = self.vectorizers[request.vectorizer]

            except:

                # If the vectorizer cannot be retrieved, it needs to be initialized. As that can
                # take time, we only flag that the vectorizer is not initialized, leaving the
                # initialization to a later moment as to not block access to the cache.
                vectorizer_initialized = False

        # Initialize the vectorizer if it is not initialized.
        if vectorizer_initialized == False:

            # Acquire lock on initialization as to ensure the vectorizer is not doubly initialized.
            with self.vectorizers_init_lock[request.vectorizer]:

                # Double check if the vectorizer was not initialized in another thread.
                with self.vectorizers_lock:

                    try:
                        vectorizer = self.vectorizers[request.vectorizer]
                        vectorizer_initialized = True

                    except:
                        pass

                # If the vectorizer truly has not been initialized, do so here.
                if vectorizer_initialized == False:

                    # Initialize the vectorizer.
                    details = self.initializers[request.vectorizer]
                    vectorizer = details.initializer(**details.kwargs)

                    # Cache the vectorizer.
                    with self.vectorizers_lock:
                        self.vectorizers[request.vectorizer] = vectorizer
                

        # ##########################################################################################
        # Generate response
        # ##########################################################################################

        # Vectorize the input.
        vectors = vectorizer.transform(request.input, **request.kwargs)

        # Create different response objects, depending on the density of the vectors generated.
        if isinstance(vectors, np.ndarray):
            
            return TransformResponse(
                data      = base64.b64encode(vectors),
                density   = vecworks.enums.DENSITY.dense,
                precision = str(vectors.dtype),
                shape     = vectors.shape
            )
        
        elif isinstance(vectors, (scipy.sparse.sparray, sparse.SparseArray)):

            # Convert sparse arrays to COO format.
            if isinstance(vectors, scipy.sparse.sparray):
                vectors = vectors.tocoo()

            else:
                vectors = vectors.asformat("coo")

            return TransformResponse(
                data      = base64.b64encode(np.stack((*vectors.coords, vectors.data))),
                density   = vecworks.enums.DENSITY.sparse,
                precision = str(vectors.dtype),
                shape     = vectors.shape
            )
        
        else:

            return fastapi.responses.JSONResponse({
                    "message": f"Vectorizer produced unsupported output of type '{type(vectors)}';"
                }, status_code = 500)
        
        # End of method 'transform' ################################################################

    # End of class 'Server' ########################################################################

# End of File ######################################################################################