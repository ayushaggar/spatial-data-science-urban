import osmnx as ox
import pandas as pd
import geopandas as gpd
import numpy as np
from osmnx import log
from model.tags import tags


def aggregate_classification(classification_list):
    """
    Aggregate into a unique classification given an input list of classifications

    Parameters
    ----------
    classification_list : list
            list with the input land use classifications

    Returns
    ----------
    string
            returns the aggregated classification
    """
    if ("other" in classification_list):  # other tag -> Non-interesting building
        classification = None
    elif (("activity" in classification_list) and ("residential" in classification_list)):  # Mixed
        classification = "mixed"
    elif ("mixed" in classification_list):  # Mixed
        classification = "mixed"
    elif ("activity" in classification_list):  # Activity
        classification = "activity"
    elif ("residential" in classification_list):  # Residential
        classification = "residential"
    elif ("infer" in classification_list):  # To infer
        classification = "infer"
    else:  # No valuable classification
        classification = None

    return classification


def classify_tag(tags, return_key_value=True):
    """
    Classify the land use of input OSM tag in `activity`, `residential`, `mixed`, None, or `infer` (to infer later)

    Parameters
    ----------
    tags : dict
            OpenStreetMap tags

    Returns
    ----------
    string, dict
            returns the classification, and a dict relating `key`:`value` defining its classification
    """
    # key_value: Dictionary of osm key : osm value
    classification, key_value = [], {}

    for key, value in tags.key_classification.items():
        # Get the corresponding key tag (without its land use)
        key_tag = key.replace(
            "activity_",
            "").replace(
            "residential_",
            "").replace(
            "other_",
            "").replace(
                "infer_",
            "")

        if tags.get(key_tag) in value:
            # First part of key defines the land use
            new_classification = key.split("_")[0]
            # Add the new classification
            classification.append(new_classification)
            # Associate the key-value
            key_value[key_tag] = tags.get(key_tag)

    classification = aggregate_classification(classification)

    if (return_key_value):
        return classification, key_value
    else:
        return classification

# Commercial type classification


def value_activity_category(x):
    """
    Classify the activity of input activity value

    Parameters
    ----------
    x : string
            activity value

    Returns
    ----------
    string
            returns the activity classification
    """
    for key, value in tags.activity_classification.items():
        if x in value:
            return key
    return None


def key_value_activity_category(key, value):
    """
    Classify the activity of input pair key:value

    Parameters
    ----------
    key : string
            key dict
    value : string
            value dict

    Returns
    ----------
    string
            returns the activity classification
    """
    # Note that some values repeat for different keys (e.g. shop=fuel and
    # amenity=fuel), but they do not belong to the same activity
    # classification
    return {
        'shop': 'commercial',
        'leisure': 'commercial',
        'amenity': 'commercial',
        'man_made': 'non_commercial',
        'industrial': 'non_commercial',
        'landuse': value_activity_category(value),
        # Inferred cases adopted land use values
        'inferred': value_activity_category(value),
        'building': value_activity_category(value),
        'building:use': value_activity_category(value),
        'building:part': value_activity_category(value)
    }.get(key, None)


def classify_activity_category(key_values):
    """
    Classify input activity category into `commercial`, `non commercial`

    Parameters
    ----------
    key_values : dict
            contain pairs of key:value relating to its usage

    Returns
    ----------
    string
            returns the activity classification
    """
    # Categories: `commercial`, `non commercial`
    categories = set([key_value_activity_category(key, value)
                      for key, value in key_values.items()])
    categories.discard(None)
    return list(categories)
