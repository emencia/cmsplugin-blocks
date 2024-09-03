"""
`Diskette <https://diskette.readthedocs.io/>`_ configuration that you can use in your
project.
"""

DISKETTE_DEFINITIONS = [
    [
        "cmsplugin_blocks",
        {
            "comments": "CMS Blocks",
            "natural_foreign": True,
            "models": [
                # Keep feature model on top since plugins depend on it
                "cmsplugin_blocks.Feature",
                "cmsplugin_blocks.Accordion",
                "cmsplugin_blocks.AccordionItem",
                "cmsplugin_blocks.Album",
                "cmsplugin_blocks.AlbumItem",
                "cmsplugin_blocks.Card",
                "cmsplugin_blocks.Container",
                "cmsplugin_blocks.Hero",
                "cmsplugin_blocks.Slider",
                "cmsplugin_blocks.SlideItem",
            ]
        }
    ],
]
"""
List of diskette definitions related to application.
"""
