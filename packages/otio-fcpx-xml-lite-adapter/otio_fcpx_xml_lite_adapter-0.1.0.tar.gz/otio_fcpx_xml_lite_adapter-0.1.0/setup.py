# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='otio-fcpx-xml-lite-adapter',
    version='0.1.0',
    description='OpenTimelineIO FCP X XML Lite Adapter',
    long_description='# otio-fcpx-xml-lite-adapter\n\n[![PyPI version](https://badge.fury.io/py/otio-fcpx-xml-lite-adapter.svg)](https://badge.fury.io/py/otio-fcpx-xml-lite-adapter) <!-- Placeholder - Update if published -->\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![Tests](https://github.com/allenday/otio-fcpx-xml-lite-adapter/actions/workflows/test.yml/badge.svg)](https://github.com/allenday/otio-fcpx-xml-lite-adapter/actions/workflows/test.yml) <!-- Placeholder - Update if using GH Actions -->\n\nAn [OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO) adapter for converting between OTIO timelines and a simplified interpretation of Final Cut Pro X XML (`.fcpxml`), focusing on marker and basic structure round-tripping.\n\n## Overview\n\nThis adapter provides basic read and write capabilities for FCPXML files (tested primarily with v1.9 and v1.13 structures), allowing interchange with OTIO. It is designed to be "lite", meaning it handles core timeline structures, clips, and markers but may not support all advanced FCPXML features.\n\nIts development has focused on specific use cases, such as:\n*   Transferring marker data (e.g., beat markers from JSON) onto placeholder clips within an FCPXML structure.\n*   Round-tripping timelines with basic audio/video clips and markers.\n\n## Features\n\n*   **Reader:**\n    *   Parses FCPXML v1.9+ (tested with v1.13).\n    *   Reads `<sequence>`, `<spine>`, `<gap>`, `<asset-clip>`, `<video>` (as placeholders), and `<marker>` elements.\n    *   Handles basic resources (`<format>`, `<asset>`, `<effect>`).\n    *   Interprets lanes for track mapping.\n    *   Creates OTIO `Timeline`, `Track`, `Clip`, `Gap`, `Marker`, `ExternalReference`, and `GeneratorReference` objects.\n*   **Writer:**\n    *   Generates FCPXML v1.9 structure.\n    *   Writes OTIO `Timeline`, `Track` (Video/Audio), `Clip`, `Gap`, `Marker`.\n    *   Maps OTIO tracks to FCPXML lanes.\n    *   Handles `ExternalReference` (creating `<asset-clip>`) and `GeneratorReference` (creating `<video>` or `<title>` placeholders using `<effect>` resources).\n    *   Supports placing markers on clips.\n    *   Includes logic for time quantization.\n    *   Creates necessary `<resources>` (format, asset, effect).\n*   **Utilities:** Includes functions for parsing and formatting FCPXML time strings (`N/Ds`).\n*   **Diagnostics:** Uses Python\'s `logging` module.\n\n## Limitations\n\n*   **Lite Scope:** This adapter intentionally does not aim to support the full FCPXML specification. Features like complex effects, transitions, audio adjustments beyond basic roles, multicam clips, detailed metadata mapping, etc., are likely **not** supported or may be handled in a simplified manner.\n*   **Simplifying Assumptions:** The reader and writer might make assumptions about the structure (e.g., expecting a main container gap in the spine for writing).\n*   **Metadata:** Minimal metadata transfer beyond basic names and resource links.\n\n## Installation\n\nYou can install the adapter from PyPI (if published):\n\n```bash\npip install otio-fcpx-xml-lite-adapter\n```\n\nOr, for development, clone the repository and install in editable mode:\n\n```bash\ngit clone https://github.com/allenday/otio-fcpx-xml-lite-adapter.git\ncd otio-fcpx-xml-lite-adapter\npip install -e .\n```\n\n## Usage\n\nUse the adapter like any other standard OTIO adapter via the `opentimelineio.adapters` module. The adapter name is `otio_fcpx_xml_lite_adapter`.\n\n```python\nimport opentimelineio as otio\n\n# --- Reading ---\ntry:\n    # Specify the adapter name if it\'s not automatically detected\n    timeline = otio.adapters.read_from_file(\n        "input_sequence.fcpxml",\n        adapter_name="otio_fcpx_xml_lite_adapter"\n    )\n    print(f"Successfully read timeline: {timeline.name}")\n    # ... process the timeline ...\n\nexcept otio.exceptions.OTIOError as e:\n    print(f"Error reading FCPXML: {e}")\n\n# --- Writing ---\n# Assume \'my_timeline\' is an existing otio.schema.Timeline object\noutput_path = "output_sequence.fcpxml"\ntry:\n    otio.adapters.write_to_file(\n        my_timeline,\n        output_path,\n        adapter_name="otio_fcpx_xml_lite_adapter"\n    )\n    print(f"Successfully wrote timeline to: {output_path}")\n\nexcept otio.exceptions.OTIOError as e:\n    print(f"Error writing FCPXML: {e}")\n\n# --- Reading/Writing Strings ---\n# fcpxml_string = otio.adapters.write_to_string(my_timeline, adapter_name="otio_fcpx_xml_lite_adapter")\n# timeline_from_string = otio.adapters.read_from_string(fcpxml_string, adapter_name="otio_fcpx_xml_lite_adapter")\n```\n\n*Note: Explicitly specifying `adapter_name="otio_fcpx_xml_lite_adapter"` might be necessary if the default OTIO plugin loading doesn\'t pick it up automatically or if other FCPXML adapters are present.*\n\n## Development\n\n### Setup\n\n1.  Clone the repository.\n2.  Create and activate a virtual environment (recommended).\n3.  Install in editable mode with test dependencies:\n    ```bash\n    pip install -e .[dev]\n    ```\n    *(Note: Define `[dev]` extras in `pyproject.toml` if needed for test dependencies like `pytest`)*\n\n### Running Tests\n\nTests are written using `unittest` and can be run with `pytest`:\n\n```bash\npytest\n```\n\nOr run specific files:\n\n```bash\npytest tests/test_writer.py\npytest tests/test_roundtrip.py\n```\n\n## Contributing\n\nContributions are welcome! Please feel free to open issues or submit pull requests.\n\n## License\n\nThis project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details. ',
    author_email='Allen Day <allenday@allenday.com>',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Multimedia :: Video',
        'Topic :: Multimedia :: Video :: Display',
        'Topic :: Multimedia :: Video :: Non-Linear Editor',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'opentimelineio>=0.17.0',
    ],
    entry_points={
        'opentimelineio.plugins': [
            'otio_fcpx_xml_adapter = otio_fcpx_xml_lite_adapter',
        ],
    },
    packages=[
        'otio_fcpx_xml_lite_adapter',
    ],
)
