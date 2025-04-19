# Phystool

This package is there to help managing physics lecture notes, exercises,
tests... It is based on four complementary elements:

1. **phystool**: Manages a database of LaTeX documents with additional metadata
2. **physnoob**: Provides some the of **phystool**'s functionalities in a GUI
3. **physvim**: [optional] Implements vim commands to interact with
   **phystool**
4. **phystex**: [optional] LaTeX classes and packages that are compatible with
   **phystool**


Among other things, **phystool** provides:

+ a clean way to compile LaTeX documents without cluttering your directories
+ a neat and user-friendly log LaTeX compilation messages
+ an automatic LaTeX recompilation when/if required


## Physnoob

A Qt GUI that lets you interact with **phystool**. It is automatically installed
at the same time as **phystool**.


## Physvim

Defines a set of commands that allows vim to interact with **phystool**. Simply
add the following line in your `~/.vimrc` file and update **Vundle**:

    Plugin 'https://bitbucket.org/jdufour/physvim.git'


## Phystex

The LaTeX classes and packages can be fully customised as long as the
`~/.phystool/phystool.conf` is correctly set. To get started, it is possible
to use the classes and packages available in:

    git clone git@bitbucket.org:jdufour/phystex.git
