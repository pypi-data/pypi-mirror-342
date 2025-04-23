# Development

## Virtualenv settings

add the following to `postactivate`

    PHYSTOOL_DIR=/path/to/git/dir
    PHYSTOOL_SRC_DIR=$PHYSTOOL_DIR/src/phystool
    cd $PHYSTOOL_SRC_DIR
    export GIT_CLIFF_WORKDIR=$PHYSTOOL_DIR
    export QT_LOGGING_RULES="qt.pyside.libpyside.warning=true"
    alias pt="python -m phystool"

the phystool directory in the virtualenv must ba symlink of 

    ls -l ~/.virtualenvs/phystool/lib/python3.12/site-packages/phystool/static
    ~/.virtualenvs/phystool/lib/python3.12/site-packages/phystool/static -> phystool/src/phystool/static
