__version__ = "2.0"

from meshroom.core import desc


class PanoramaInit(desc.CommandLineNode):
    commandLine = 'aliceVision_panoramaInit {allParams}'
    size = desc.DynamicNodeSize('input')

    documentation = '''
This node allows to setup the Panorama:

1/ Enables the initialization the cameras from known position in an XML file (provided by
["Roundshot VR Drive"](https://www.roundshot.com/xml_1/internet/fr/application/d394/d395/f396.cfm) ).

2/ Enables to setup Full Fisheye Optics (to use an Equirectangular camera model).

3/ To automatically detects the Fisheye Circle (radius + center) in input images or manually adjust it.

'''

    inputs = [
        desc.File(
            name='input',
            label='Input',
            description="SfM Data File",
            value='',
            uid=[0],
        ),
        desc.File(
            name='config',
            label='Xml Config',
            description="XML Data File",
            value='',
            uid=[0],
        ),
        desc.ListAttribute(
            elementDesc=desc.File(
                name='dependency',
                label='',
                description="",
                value='',
                uid=[],
            ),
            name='dependency',
            label='Dependency',
            description="Folder(s) in which computed features are stored. (WORKAROUND for valid Tractor graph submission)",
            group='forDependencyOnly', # not a command line argument
        ),
        desc.BoolParam(
            name='useFisheye',
            label='Full Fisheye',
            description='To declare a full fisheye panorama setup',
            value=False,
            uid=[0],
        ),
        desc.BoolParam(
            name='estimateFisheyeCircle',
            label='Estimate Fisheye Circle',
            description='Automatically estimate the Fisheye Circle center and radius instead of using user values.',
            value=True,
            uid=[0],
            enabled=lambda node: node.useFisheye.value,
        ),
        desc.GroupAttribute(
            name="fisheyeCenterOffset",
            label="Fisheye Center",
            description="Center of the Fisheye circle (XY offset to the center in pixels).",
            groupDesc=[
                desc.FloatParam(
                    name="fisheyeCenterOffset_x", label="x", description="X Offset in pixels",
                    value=0.0,
                    uid=[0],
                    range=(-1000.0, 10000.0, 1.0)),
                desc.FloatParam(
                    name="fisheyeCenterOffset_y", label="y", description="Y Offset in pixels",
                    value=0.0,
                    uid=[0],
                    range=(-1000.0, 10000.0, 1.0)),
                ],
            group=None, # skip group from command line
            enabled=lambda node: node.useFisheye.value and not node.estimateFisheyeCircle.value,
        ),
        desc.FloatParam(
            name='fisheyeRadius',
            label='Radius',
            description='Fisheye visibillity circle radius (% of image shortest side).',
            value=96.0,
            range=(0.0, 150.0, 0.01),
            uid=[0],
            enabled=lambda node: node.useFisheye.value and not node.estimateFisheyeCircle.value,
        ),
        desc.ChoiceParam(
            name='verboseLevel',
            label='Verbose Level',
            description='Verbosity level (fatal, error, warning, info, debug, trace).',
            value='info',
            values=['fatal', 'error', 'warning', 'info', 'debug', 'trace'],
            exclusive=True,
            uid=[],
        ),
    ]

    outputs = [
        desc.File(
            name='outSfMData',
            label='Output SfMData File',
            description='Path to the output sfmdata file',
            value=desc.Node.internalFolder + 'sfmData.sfm',
            uid=[],
        )
    ]
