# -*- coding: utf-8 -*-
import os
import typing
import enum

import mpmath

import fractalshades as fs
import fractalshades.gui as fsgui 
import fractalshades.colors as fscolors 


def manual_test_func_widget():
    """
    This is not a real automated test however
    It can be run manually and used to check behavior of the "func Editor":
      - non-regression in the allowable paramters
      - development of new parameters
    """
    
    realpath = os.path.realpath(__file__)
    test_dir = os.path.splitext(realpath)[0]

    fractal = fs.Fractal(test_dir)
    x = '-1.0'
    y = '-0.0'
    dx = '5.0'
    nx = 800
    theta_deg = 0.
    calc_name = 'test'
    
    xy_ratio = 1.0
    dps = 16
    shade_kind = "glossy"
    
    colormap = fscolors.cmap_register["classic"] # argon
    lighting = fscolors.lighting_register["glossy"]
    numpy_expr = fs.numpy_utils.Numpy_expr("y", "np.sin(y)")

    my_enum = enum.Enum(
        "my_enum",
        ("value1", "value2", "value3"),
        module=__name__
    )

    enum_type = typing.Literal[my_enum]

    def func(
         fractal: fs.Fractal=fractal,
         calc_name: str=calc_name,

         _0: fsgui.collapsible_separator="Mandatory parameters",
         x: mpmath.mpf=x,
         y: mpmath.mpf=y,
         dx: mpmath.mpf=dx,
         xy_ratio: float=xy_ratio,
         theta_deg: float=theta_deg,
         dps: int=dps,
         nx: int=nx,


         _1: fsgui.collapsible_separator="First param list",
         mpf1: mpmath.mpf="3.14156",
         float1: float=3.14159,


         _2: fsgui.collapsible_separator="Second param list",
         mpf2: mpmath.mpf="3.14156",
         float2: float=3.14159,
         colormap: fscolors.Fractal_colormap=colormap,
         lighting: fscolors.Blinn_lighting=lighting,
         masked_color: fscolors.Color=(0.1, 0.9, 0.1, .5),
         rgb_color: fscolors.Color=(0.5, 0.1, 0.1),
         shade_kind: typing.Literal["None", "standard", "glossy"]=shade_kind,
         invert_cmap: bool=False,
         enum_val: enum_type="value1",
         test_expr: fs.numpy_utils.Numpy_expr=numpy_expr
    ):
        pass
    
    gui = fsgui.Fractal_GUI(func)
    gui.connect_image(image_param="calc_name")
    gui.connect_mouse(x="x", y="y", dx="dx", xy_ratio="xy_ratio", dps="dps")
    gui.show()

if __name__ == "__main__":
     manual_test_func_widget()
