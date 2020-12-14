from pathlib import Path

from clld.web.assets import environment

import mixezoqueanvoices


environment.append_path(
    Path(mixezoqueanvoices.__file__).parent.joinpath('static').as_posix(),
    url='/mixezoqueanvoices:static/')
environment.load_path = list(reversed(environment.load_path))
