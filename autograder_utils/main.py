import pytest
import contextlib
import os
from backends import get_edstem_json
from plugin import AutograderPlugin


autograder_plugin = AutograderPlugin()
with contextlib.redirect_stdout(open(os.devnull, "w")):
    pytest.main(
        ["-vv", "-q", "--strict-markers", "--tb=line"], plugins=[autograder_plugin]
    )
print(get_edstem_json(autograder_plugin.autograder_reports))
