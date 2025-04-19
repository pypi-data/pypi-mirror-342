import os
import numpy as np
import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = True

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("my_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "workout-builder",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:5174",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/dist")
    _component_func = components.declare_component("workout-builder", path=build_dir)

print("Build directory:", build_dir)
# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.

def _unpack_groups(data:dict):
    for group in data['groups']:
        length = len(group['blocks'])
        if group['repeats'] <= 1:
            continue
        for i in range(group['repeats']-1):
            for block in group['blocks']:
                idx = [x['id'] for x in data['blocks']].index(block)
                data['blocks'].insert(idx + length, data['blocks'][idx])
    return data

            




def _unpack_interval_blocks(data:dict, frequency:int):
    rv = []
    data = _unpack_groups(data) 
    for block in data['blocks']:
        if block['type'] == 'ramp':
            rv += np.linspace(block['startPower'], block['endPower'], block['duration'] * frequency).tolist()
        else:
            rv += [block['intensity']]* block['duration'] * frequency
    return rv


def workout_builder(return_list=True, frequency='s'):
    """Create a new instance of "my_component".

    Parameters
    ----------
    return_list: bool
        Whether to return a list of the power values. If False a `dict` is
        returned with the information about the workout blocks and different
        groups. 
        
    frequency: str
        The frequency of the power samples, default is 's'. Only applicable if
        `return_list` is True. The options are 's' for seconds, 'ms' for
        miliseonds. 

    Returns
    -------
    dict
        If `return_list` is False, a dict with the information about the
        workout blocks and different groups. 
        If `return_list` is True, a list of power values based on the workout blocks. 

    """
    if frequency not in ['s', 'ms']:
        raise ValueError("frequency must be either 's' or 'ms'")
    
    component_value = _component_func(default=[])
    if return_list and component_value != []:
        return _unpack_interval_blocks(component_value, 1 if frequency == 's' else 1000)
    return component_value
