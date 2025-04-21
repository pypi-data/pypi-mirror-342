# elbbarcs 

Find Scrabble™ letter distributions for a corpus.

## Usage

###  Library
```python
from elbbarcs import Estimator

e = Estimator()				# Create a new Estimator object
s = e.estimate('english.txt')		# Estimate the scores for the corpus
e.table(s) 				# Print out a table
```

```python
from elbbarcs import Estimator

e = Estimator(digraphs="ch c'h zh")	# Create a new Estimator object
s = e.estimate('brezhoneg.txt')		# Estimate the scores for the corpus
e.table(s) 				# Print out a table
```

The constructor takes the following arguments:
* `digraphs`: A string containing the space-separated digraphs in the language
* `tiles`: The number of tiles
* `buckets`: The number of buckets 

### Command line program

The library functionality is also exposed via the `elbbarcs` command-line utility.

```
$ elbbarcs brezhoneg.txt --digraph "ch zh c'h"
              ×1            ×2   ×3      ×4   ×5   ×6      ×7   ×12   ×14
0                      [blank]                                           
1                                              I    T   N O R     A     E
2                            G    S   D L U                              
3              H   B K M P V Z                                           
4   C'H W ZH Ñ Ù                                                         
5              F                                                         
6         C CH J                                                         
7              Y                                                         
9              É                            
```

This table indicates that for Breton, there should be 2 tiles for `K`, which will have a score of `3`.

## History

This library was developed by [Daniel Swanson](https://github.com/mr-martian/) at the request of Francis Tyers for calculating the number 
of scrabble letters needed and their distribution for a given language. The objective was to make a 
scrabble set for San Mateo Huave from combinations of other scrabble sets.

In the end it required one set of each of English, Spanish and German to create the set for Huave.

![Scrabble for San Mateo Huave](https://github.com/ftyers/scrabble/blob/master/img/huv.jpg?raw=true)


