FAQ / Troubleshooting
======================


#### I get an error when doing `from fetchAZA import plotters`

This is because your code can't find the project `fetchAZA`.

**Option 1:** Install the package `fetchAZA` locally

Activate your environment.

```
micromamba activate template_env
```

then install your project from the terminal window in, e.g., `/Users/eddifying/github/fetchAZA` as
```
pip install -e .
```
This will set it up so that you are installing the package in "editable" mode.  Then any changes you make to the scripts will be taken into account (though you may need to restart your kernel).

**Option 2:** Add the path to the `fetchAZA` to the code

Alternatively, you could add to your notebook some lines so that your code can "find" the package.  This might look like
```
import sys
sys.path.append('/Users/eddifying/github/fetchAZA')
```
before the line where you try `from fetchAZA import plotters`.

#### Failing to install the package in a Github Action

```
× Getting requirements to build editable did not run successfully.
│ exit code: 1
╰─> See above for output.
```

To test the installation, you'll want a fresh environment.

**In a terminal window, at the root of your project** (for me, this is `/Users/eddifying/github/fetchAZA/`), run the following commands in order.
```
virtualenv venv
source venv/bin/activate && micromamba deactivate
pip install -r requirements.txt
pip install -e .
```

Then check and troubleshoot any errors.  When this runs, you are probably ready to try it with the GitHub Actions (where the workflows are in your repository in `.github/workflows/*.yml`)

#### What's the difference between the repository name and the python package name??

Here, they are both called fetchAZA, but the outer folder fetchAZA/ is the repository, while the inner folder `fetchAZA/fetchAZA/` contains the package modules (e.g. plotters.py).

Our repository is called `fetchAZA`.  You can have dashes in a repository name.

Within the repository, the code (`*.py` files) are located in a subdirectory called `fetchAZA`.  This is the package or module that we are creating and that will be installed, e.g., by `pip` when you do a `pip install -e .`.  Python packages should not have dashes in them!

