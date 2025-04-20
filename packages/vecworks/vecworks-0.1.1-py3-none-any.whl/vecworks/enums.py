# ##################################################################################################
#
#  Title
#
#   vecworks.enums.py
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
#    Part of the Vecworks framework, providing various enumerations used through the framework.
#
# ##################################################################################################

# ##################################################################################################
# Dependencies
# ##################################################################################################

# Python standard library ##########################################################################

# Fundamentals
from enum import (
    Enum
)


# ##################################################################################################
# Enumerations
# ##################################################################################################

# DENSITY ##########################################################################################

class DENSITY(Enum):

    """
    Describes density of a vector.
    """

    # ##############################################################################################
    # Options
    # ##############################################################################################

    dense : int = 0
    """
    A vector representation storing both zero- and non-zero elements.
    """

    sparse : int = 1
    """
    A vector representation storing only non-zero elements.
    """

    # End of enumeration 'DENSITY' #################################################################
    

# DISTANCES ########################################################################################

class DISTANCES(Enum):

    """
    Specifies how the (dis)similarity between two vectors is calculated.
    """

    # ##############################################################################################
    # Options
    # ##############################################################################################

    cosine    : str = ("cosine")
    """
    Compares the orientation of two vectors by calculating the angle between two non-zero vectors.
    """

    hamming   : str = ("hamming")
    """
    Counts the number of positions at which two vectors' corresponding elements are different.
    """

    jaccard   : str = ("jaccard")
    """
    Considers vectors as sets, calculating the degree of overlap between both vectors/sets.
    """

    l1        : str = ("l1")
    """
    Takes two equal-length vectors, calculating pairwise the absolute difference between both
    vectors' elements, summing up the results to produce a single distance measure.
    """

    l2        : str = ("l2")
    """
    Takes two equal-length vectors, calculating pairwise the absolute difference between both
    vectors' elements, squaring up the results before them up into a single distance measure.
    """

    nip       : str = ("nip")
    """
    Takes two equal-length vectors, multiplying both vectors' elements pairwise, summing up the
    results. Multiplied with 1 to allow a higher inner product to represent greater similarity.
    """

    # End of enumeration 'DISTANCES' ###############################################################


# ENSEMBLERS #######################################################################################

class ENSEMBLERS(Enum):

    """
    Specifies the 'ensembler' to use to combine the results of multiple vector comparisons.
    """

    # ##############################################################################################
    # Options
    # ##############################################################################################

    rrf : str = ("rrf")
    """
    Reciprocal Rank Fusion (RRF) is a method for combining vector similarity measures based on rank.
    For each pair of vector indices it ranks the similarity, finally aggregating these rankings to
    produce a single similarity measure.
    """

    # End of enumeration 'ENSEMBLERS' ##############################################################

# End of File ######################################################################################