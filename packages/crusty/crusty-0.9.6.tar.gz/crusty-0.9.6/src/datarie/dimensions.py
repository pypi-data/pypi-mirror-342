import numpy as np

def repeat_nd(array: np.ndarray,
              dims: int | list,
              repeats: dict,
              ndims: int =  2,) -> np.ndarray:
    
    if isinstance(dims, int): dims = [dims]

    ddims = [d for d in range(ndims) 
             if d not in dims]

    slx = [slice(0, None)] * ndims
    
    for d in ddims: slx[d] = None

    array = array[tuple(slx)]

    for d in ddims: 
        
        array = np.repeat(array, 
                          repeats[d], 
                          d)

    return array