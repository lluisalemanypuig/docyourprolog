# Document Your Prolog

This project intends to offer a stable tool to generate html documentation for
[SWI-Prolog](http://www.swi-prolog.org/) code automatically by parsing the source
files.

The documentation generated is extracted from so-called _block comments_. There are
several types of block comments and each start with a particular string of characters,
all of them ignored by the SWI-Prolog compiler. Likewise for JavaDoc, inside these
blocks the programmer will write the documentation using tags starting with '@'.

## Block comments

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
        
## Usage

This software needs a configuration file containing control variables in order to generate
the documentation. To generate this file, issue the command:


