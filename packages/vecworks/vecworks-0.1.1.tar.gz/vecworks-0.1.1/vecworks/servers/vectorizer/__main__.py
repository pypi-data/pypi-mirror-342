# ##################################################################################################
#
#  Title
#
#   vecworks.remote.server.py
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
#    Part of the Vecworks framework, implementing the CLI front-end for the vectorizer server.
#
# ##################################################################################################

# ##################################################################################################
# Dependencies
# ##################################################################################################

# Python standard library ##########################################################################

# Fundamentals
import collections
import dataclasses
import importlib
import types

import typing
from typing import (
    Any
)

# Utilities
import argparse
import ast
import re


# Local ############################################################################################

# vecworks.vectorizers
from vecworks.vectorizers import (
    Vectorizer
)

# vecworks.servers.vectorizer.server
from .server import (
    CLIArgument,
    Server,
    ServerConfig,
    VectorizerInitializationDetails
)


# ##################################################################################################
# Main entry point
# ##################################################################################################

if __name__ == "__main__":

    # ##############################################################################################
    # Parse arguments
    # ##############################################################################################

    # Set-up parser ################################################################################

    # Initialize parser.
    argparser : argparse.ArgumentParser = (
        argparse.ArgumentParser(
            prog        = "vecworks.remote.vectorizer",
            description = "Microservice to remotely serve vectorizers over HTTP" 
        )
    )

    ### Configuration of vectorizers ###############################################################

    argparser.add_argument(

        "-v", "--vectorizer",

        help = (
            "Qualified name of the Python class to deploy as vectorizer, including alias, and any"
            " arguments to pass to the class."
        ),

        nargs    = "+",
        dest     = "vectorizers",

        action   = "append",
        required = True

    )


    ### Server configuration #######################################################################

    # Iterate over all server configuration options.
    for arg in dataclasses.fields(ServerConfig):

        # Retrieve hints. 
        arg_type = typing.get_args(arg.type)[0]
        cli_hints : CLIArgument = typing.get_args(arg.type)[1]
        
        # Select a 'safe type' in case multiple types are selected, or if a sequence is expected,
        # the primitive that is being accumulated.
        if typing.get_origin(arg_type) is not None:
            safe_type = next((t for t in typing.get_args(arg_type) if t is not types.NoneType))

        else:
            safe_type = arg_type

        # Dynamically add argument to the parser.
        argparser.add_argument(

            *cli_hints.aliases,

            dest     = arg.name,
            type     = safe_type,
            default  = arg.default,

            help     = cli_hints.help,

            nargs    = "+" if typing.get_origin(arg_type) == collections.abc.Sequence else None,

            action   = (
                "append" if typing.get_origin(arg_type) == collections.abc.Sequence else None
            ),

            required = not (types.NoneType in typing.get_args(arg_type) or arg.default is not None)

        )


    # Parse ########################################################################################

    # Run main program parser ######################################################################

    # Parse arguments
    args = argparser.parse_args()


    # Parse vectorizer arguments ###################################################################

    # Predeclare variable to hold gathered vectorizer initialization details.
    initializers : dict[str, VectorizerInitializationDetails] = dict()

    # Iterate over each vectorizer specified.
    for vectorizer_args_unparsed in args.vectorizers:

        # Check if signature was matched ###########################################################

        if len(vectorizer_args_unparsed) < 2:

            raise ValueError(
                f"Insufficient arguments were passed for vectorizer;"
            )
        

        # Retrieve vectorizer class ################################################################

        # Retrieve qualified name.
        qualname : str = vectorizer_args_unparsed[0]

        # Validate qualified name.
        for component in qualname.split("."):

            if not component.isidentifier():

                raise ValueError(
                    f"Qualified name '{qualname}' is invalid;"
                )
            
        qualname_components : list[str] = qualname.rsplit(".", maxsplit = 1)

        if len(qualname_components) < 2:

            raise ValueError(
                f"Qualified name '{qualname}' is invalid; consisting of a single qualifier, while"
                f" both a module and class name need to be specified;"

            )
        
        # Retrieve module and class name from qualified name.
        qualname_module : str = qualname_components[0]
        qualname_cls    : str = qualname_components[1]

        # Access module.
        vectorizer_module = importlib.import_module(qualname_module)

        # Retrieve class.
        vectorizer_cls = getattr(vectorizer_module, qualname_cls, None)

        if vectorizer_cls is None:

            raise ValueError(
                f"Could not retrieve class '{qualname_cls}' from module '{qualname_module}';"
            )
        
        if not issubclass(vectorizer_cls, Vectorizer):

            raise ValueError(
                f"Class '{qualname_cls}' is not a sub-class of"
                f" 'vecworks.vectorizers.Vectorizer';"
            )
        

        # Retrieve initializer #####################################################################
        
        # Retrieve initializer.
        vectorizer_initializer : callable = (
            getattr(vectorizer_cls, "__init_cli__", None) or
            vectorizer_cls
        )
        

        # Retrieve alias ###########################################################################

        # Store alias.
        vectorizer_alias = vectorizer_args_unparsed[1]


        # Retrieve initialization arguments ########################################################

        # Set-up dictionary to hold the vectorizer's initialization arguments.
        vectorizer_init_args : dict[str, Any] = dict()

        # Iterate over unparsed arguments.
        for arg_i, arg_unparsed in enumerate(vectorizer_args_unparsed[2:]):

            # Separate argument name and assigned value.
            m = re.match(r"^(?P<name>[^\d\W]\w+)\=(?P<value>.+)$", arg_unparsed)

            if m is None:

                raise ValueError(
                    f"Invalid argument was passed at index '{arg_i}' for vectorizer"
                    f" '{vectorizer_alias}': {arg_unparsed};"
                )

            # Iterpret the argument, and store it.        
            try:
                vectorizer_init_args[m.group("name")] = ast.literal_eval(m.group("value"))
            except:
                vectorizer_init_args[m.group("name")] = m.group("value")
            

        # Store vectorizer initializations details #################################################

        initializers[vectorizer_alias] = VectorizerInitializationDetails(
            initializer = vectorizer_initializer,
            kwargs       = vectorizer_init_args
        )

    
    # ##############################################################################################
    # Operate service
    # ##############################################################################################

    # Initialize the server.
    server : Server = Server(
        
        initializers, 

        config = ServerConfig(

            host                   = args.host,
            port                   = args.port,

            ssl_keyfile            = args.ssl_keyfile,
            ssl_keyfile_password   = args.ssl_keyfile_password,
            ssl_certfile           = args.ssl_certfile,
            ssl_ca_certs           = args.ssl_ca_certs,
            ssl_cert_reqs          = args.ssl_cert_reqs,
            ssl_ciphers            = args.ssl_ciphers,

            cors_allowed_origins   = args.cors_allowed_origins,
            cors_allow_credentials = args.cors_allow_credentials,
            cors_allowed_methods   = args.cors_allowed_methods,
            cors_allowed_headers   = args.cors_allowed_headers
        )
        
    )

    # Run the server.
    server.run()

    # End of main entry point ######################################################################


# End of File ######################################################################################