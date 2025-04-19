import numpy as np
from utils import *
from graphics.texture import *


class MTLMeshMaterial:
    """
    Mesh Material loaded from a MTL file.

    Parameters
    ----------
    opacity : float between 0 and 1
        Mirrors 'Material.opacity' in threejs.
        Float in the range of 0.0 - 1.0 indicating how transparent the material is.
        A value of 0.0 indicates fully transparent, 1.0 is fully opaque.
        The attribute 'transparent' is set to true automatically if opacity<1.
        (default: 1).

    url : string
        The url that contains the mtl files.
        It must have one of the following formats: 'url'.


    """

    #######################################
    # Attributes
    #######################################



    @property
    def url(self):
        """The 3d model url."""
        return self._url

    @property
    def opacity(self):
        """The object opacity."""
        return self._opacity

    #######################################
    # Constructor
    #######################################

    def __init__(self, url="", opacity=1):

        # Error handling

        if not Utils.is_a_number(opacity) or opacity < 0 or opacity > 1:
            raise Exception(
                "The parameter 'opacity' should be a float between 0 (fully transparent) and 1 (fully opaque).")

        error = Utils.is_url_available(url, ['mtl'])
        if not (error == "ok!"):
            raise Exception("The parameter 'url' " + error)
        
        self._url = url
        self._opacity = opacity


    #######################################
    # Std. Print
    #######################################

    def __repr__(self):

        string = "MTL Mesh Material"

        return string

    #######################################
    # Methods
    #######################################

    def gen_code(self, name):

        string = "const material_"+ name + " = {"
        
        string+= "type: 'mtl',"
        string+= "opacity: "+str(self.opacity)+","
        string+= "url: '"+self.url+"'};\n\n"
        



        return string
