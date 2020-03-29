# Document Your Prolog

This project intends to offer a stable tool to generate html documentation for [SWI-Prolog](http://www.swi-prolog.org/) code automatically by parsing the source files found inside a given directory.

## Documenting your code

The documentation generated is extracted from so-called _block comments_. There are several types of block comments and each start with a particular string of characters, all of them ignored by the SWI-Prolog compiler. Likewise for JavaDoc, inside these blocks the programmer will write the documentation using tags starting with '@'.

### Block comments

There are three types of block comments:
- File blocks: these blocks are used to indicate a general description of a given file. Also, the programmer can specify the author(s) and the date. This information is given as follows:
        
        /***
        @descr File containing a single predicate defining the concept of 'minimum'
        value of a list.
        @author Me, Myself and I
        @date July 16th, 2018
        */

    This block may be placed anywhere in the file, however it makes more sense to put
    it at the very beginning. If more than one is used, a warning will be issued and
    the last file block found will be used.

- Predicate blocks: these blocks contain the documentation for a particular predicate and should be placed just right above it. With this kind of blocks the programmer can specify the form of the predicate, a general description, and constraints on the parameters. The tags that should be used are explained using an example:
        
        /**
        @form min(List,Value)
        @descr Value is the minimum value in List
        @constrs [descr]
            @param List Cannot be empty and must contain elements comparable with @>
        */

    Just right after the _@constrs_ tag one may write an arbitrarily long general description
    of the constraints related to the parameters of the predicate, if necessary. This description
    is optional and is compatible with _@param_. The order of tags does not matter.

- Separator blocs: these blocks contain a description of the coming predicates, usually a description that categorises them. For example, one may write:
        
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

#### Description enrichment

Any description (anything after a @descr, or between the @constr and each @param, if there is any) can contain references to parameters and predicates. For example, we can have the following predicates documentation:

        /**
        @form min(List,Value)
        @descr @Value is the minimum value in @List.
        @constrs
            @param List Cannot be empty and must contain elements
        	comparable with @>
        */

        /**
        @form max(List,Value)
        @descr @Value is the maximum value in @List.
        @constrs
            @param List Likewise in ?min/2.
        */

The reference to the parameter, indicated with '@' will simply highlight the string following the '@'. The reference to the predicate, however, will add a hyperlink tied to the following string. The referenced predicate must be in the same source file as the block comment where the reference is put. That is, the reference '?min/2' can not be used if the corresponding predicate block is not in the same file as the predicate block documenting 'min/2'.

Moreover, any description can contain special strings to indicate formatted text.
- The simplest string is the blank line: a single blank line between two paragraphs.
        
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt
        ut labore et dolore magna aliqua.
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
        commodo consequat.
    
    This will generate both sentences one next to the other in the html file.

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt
        ut labore et dolore magna aliqua.
        
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
        commodo consequat.
    
    This will make the second sentence to be displayed in a new paragraph.
    
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt
        ut labore et dolore magna aliqua.
        
        
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
        commodo consequat.
    
    This will leave a blank line between both sentences (this also applies for three or more blank
    lines).

- Verbatim environments: if the programmer wants to display some formatted text "based on spaces", they can use the '\bverbatim' string to define a verbatim environment. It must be closed with '\everbatim' and anything in between will be displayed _as is_.

- Bullet lists: one can define bullet lists with '\blist'. A bullet list should be finished with a '\elist' and its items are defined with '\item'. Leave a blank space after each '\item'. The user may also leave blank lines between items of the list so as to make the html display them too. Furthermore, lists can be nested and contain other environments.

        Lorem ipsum dolor sit amet:
        \blist
        \item consectetur adipiscing elit, sed do eiusmod tempor incididunt
        \item ut labore et dolore magna aliqua.
                \blist
                \item Ut enim ad minim veniam,
                \item quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
                commodo consequat.
                        \elist
        \item Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
        fugiat nulla pariatur
        \elist
        
## Usage

### Generate the default configuration

This software needs a configuration file containing control variables in order to generate the documentation. Assume that _dyp_ is an alias of _python3 dyp.py_. To generate the configuration file, issue the commands:

        cd /path/to/the/project
        dyp -g dyfile/dyconf.py

### Edit the configuration

In that directory there should be another directory with all the sources (usually called _src/_). Now, edit the file appropriately depending on your needs. There are several variables to be edited. The most important variables are the following:
- SRC_DIR: relative path to the directory with all the source files
- DEST_DIR: relative path to the directory where all the files for the documentation will be saved.
- PROJECT_NAME: the name of your project.
- PROJECT_DESCRIPTION: a description of your project.
 
There are other variables related to the files generated and other characteristics of the documentation. There exists the possibility of generating graphs that show what files _include_ what files. These graphs are directed and there is a vertex for each file and one directed edge A -> B if file A includes B.
- FILE_INCLUSION_GRAPH: generate a graph for each file. This graph will have a single source vertex that represents the file.
- PROJECT_INCLUSION_GRAPH: generate a graph for the whole project. This graph may have several source vertices.
- FILE_GRAPH_MAX_DIAMETER: control the maximum diameter of each file's graph.
- PROJECT_GRAPH_MAX_DIAMETER: control the maximum diameter of the whole project's graph.
 
Since each source file may include other files, the programmer may be interested to generete documentation for those too. 
- FOLLOW_INCLUDES: tell _dyp_ to generate documentation for the files from other files.

Some source files may not be included by the files in the directory specified in _SRC_DIR_, although these files may still be found in the directory.
- RECURSIVE: tell _dyp_ to find source files in all the subdirectories in _SRC_DIR_.
- EXTENSIONS: document only those files with an extension in the list.

Since _dot_ is needed to generate the graphs, _dyp_ needs to know the path to the executable file:
- DOT_EXE_PATH: the absolute path to the executable file of the _dot_ software.

Cache system (efficiency options):
- CACHE_FILES: the user may want to check how the documentation looks after modifying a single file among the hundreds of files in the project. This variable tells the software to store information to avoid generating html code when it is not actually needed, that is, when a source file has not been modified (however, each file will be parsed regardless of the absence of modifications). Moreover, the graphs are generated using the _dot_ software (which is part of Graphviz). This variable is used to decide whether the _.dot_ files are kept or removed after generating the graphs in _.png_ format. These files are also used to avoid callid the _dot_ software if the graph has not changed. It is recommended to be set to _True_.

### Generate the documentation

In order to generate the html documentation issue the following command while being in the directory of the project.

        dyp -c dyfile/dyconf

Notice that the _.py_ is not in the command.

## Dependencies

- [Python](https://www.python.org/): this software has been tested only on python 2.7.
- [Graphviz](https://www.graphviz.org/): the _dot_ software is required to generate the inclusion graphs.

## Installation

Installing this project is simple: one can download the source and place it anywhere in their file system. Say it is downloaded to ~/Documents/software. One way to call the main file is to add an alias to your _.bashrc_ (or equivalent file):

        alias dyp='python3 ~/Documents/software/docyourprolog/dyp.py'

Alternatively, the code can also be copied and moved to the _/usr/bin/_ directory:

        sudo cp ~/Documents/software/docyourprolog/ /usr/bin/docyourprolog/
        alias dyp='python3 /usr/bin/docyourprolog/dyp.py'

## Example

[Here](https://github.com/lluisalemanypuig/docyourprolog/tree/master/example) one will find a minimal example of Prolog code and a configuration file. The documentation generated for that source code can be found in [this](https://github.com/lluisalemanypuig/docyourprolog/tree/master/example/docs) directory.

In particular, the reader is encouraged to check the file [arithmetic_evaluation.pl](https://github.com/lluisalemanypuig/docyourprolog/blob/master/example/src/number/arithmetic_evaluation.pl) to see some possibilities of _description enrichment_ explained before. The corresponding html file generated with this tool can be found in [arithmetic_evaluation.html](https://github.com/lluisalemanypuig/docyourprolog/blob/master/example/docs/number/arithmetic_evaluation.html).
