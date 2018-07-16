# Document Your Prolog

This project intends to offer a stable tool to generate html documentation for
[SWI-Prolog](http://www.swi-prolog.org/) code automatically by parsing the source
files.

## Documenting your code

The documentation generated is extracted from so-called _block comments_. There are
several types of block comments and each start with a particular string of characters,
all of them ignored by the SWI-Prolog compiler. Likewise for JavaDoc, inside these
blocks the programmer will write the documentation using tags starting with '@'.

### Block comments

There are three types of block comments:
- File blocks: these blocks are used to indicate a general description of a given file.
Also, the programmer can specify the author(s) and the date. This information is given
as follows:
        
        /***
        @descr File containing a single predicate defining the concept of 'minimum'
        value of a list.
        @author Me, Myself and I
        @date July 16th, 2018
        */

    These blocks may be placed anywhere in the file, however it makes more sense to put
    them at the very beginning.

- Predicate blocks: these blocks contain the documentation for a particular predicate
and are placed just right above it. With this kind of blocks the programmer can
specify the form of the predicate, a general description, and constraints on the
parameters. The tags that should be used are explained using an example:
        
        /**
        @form min(List,Value)
        @descr Value is the minimum value in List
        @constrs
            @param List cannot be empty and must contain elements comparable with @>
        */

    Just right after the _@constrs_ tag one may write an arbitrarily long general description
    of the constraints related to the parameters of the predicate, if necessary. This description
    is optional and is compatible with _@param_. The order of tags does not matter.

- Separator blocs: these blocks contain a description of the coming predicates, usually
a description that categorises them. For example, one may write:
        
        /*! These predicates are related to Quantum Physics */
        
        % Here are defined several predicates with their own
        % documentation using predicate blocks.
        
        qpred1(..):- ...
        qpred2(..):- ...
        
        /*! These predicates will prove that P = NP */
        
        % Here are defined more predicates, also with their own
        % documentation using predicate blocks.
        
        pnppred1(..):- ...
        pnppred2(..):- ...

    For every file, the documentation generated will have an itemised list of predicates
    containing the names of the predicates defined. The description contained in the separator
    blocks will be put between the appropriate items in the list, following the format:
    
        Predicates:
        
        These predicates are related to Quantum Physics
        - qpred1
        - qpred2
        
        These predicates will prove that P = NP
        - pnppred1
        - pnppred2
        
### Usage

#### Generate the default configuration

This software needs a configuration file containing control variables in order to generate
the documentation. Assume that _dyp_ is an alias of _python src/dyp.py_.
To generate the configuration file, issue the commands:

        cd /path/to/the/project
        dyp -g dyfile/dyconf.py

#### Edit the configuration

In that directory there should be another with all the sources (usually called _src/_).
Now, edit the file appropriately depending on your needs. There are several variables to be
edited. The most important variables are the following:
- SRC_DIR: relative path to the directory with all the source files
- DEST_DIR: relative path to the directory where all the files for the documentation will be
saved.
- PROJECT_NAME: the name of your project.
- PROJECT_DESCRIPTION: a description of your project.
 
There are other variables related to the files generated and other characteristics of
the documentation. There exists the possibility of generating graphs that show what files
_include_ what files. These graphs are directed and there is a vertex for each file and
one directed edge A -> B if file A includes B.
- FILE_INCLUSION_GRAPH: generate a graph for each file. This graph will have a single source
vertex that represents the file.
- PROJECT_INCLUSION_GRAPH: generate a graph for the whole project. This graph may have
several source vertices.
- KEEP_DOT: the graphs are generated using the _dot_ software which is part of Graphviz.
This variable is used to decide whether the _.dot_ files are kept or removed after generating
the graphs in _.png_ format.
- FILE_GRAPH_MAX_DIAMETER: control the maximum diameter of each file's graph.
- PROJECT_GRAPH_MAX_DIAMETER: control the maximum diameter of the whole project's graph.
 
Since each source file may include other files, the programmer may be interested to generete
documentation for those too. 
- FOLLOW_INCLUDES: tell _dyp_ to generate documentation for the files from other files.

Some source files may not be included by the files in the directory specified in _SRC_DIR_,
although these files may still be found in the directory.
- RECURSIVE: tell _dyp_ to find source files in all the subdirectories in _SRC_DIR_.
- EXTENSIONS: document only those files with an extension in the list.

Finally, since _dot_ is needed to generate the graphs, _dyp_ needs to know the path
to the executable file:
- DOT_EXE_PATH: the absolute path to the executable file of the _dot_ software.

#### Generate the documentation

In order to generate the html documentation issue the following command while being in the
directory of the project.

        dyc -c dyfile/dyconf

Notice that the _.py_ is not in the command.

## Dependencies

- [Python](https://www.python.org/): this software has been tested only on python 2.7.
- [Graphviz](https://www.graphviz.org/): the _dot_ software is required to generate the
inclusion graphs.
