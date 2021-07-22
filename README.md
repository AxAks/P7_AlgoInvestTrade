# P7_AlgoInvestTrade
Forcebrute -vs- Optimized Algorithms coded with python
***

## Chapters 
1. [Presentation](#presentation)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Execution](#execution)
5. [Bruteforce](#bruteforce)
6. [Optimized](#optimized)

## 1. Presentation <a name="presentation"></a>
These two scripts enable to create an acceptable portfolio of shares based upon a list of given shares.
***

## 2. Prerequisites <a name="prerequisites"></a>
These scripts run under python 3.9 in a virtual environment.  
Thus, it is usable on Windows, Unix-based operating systems
insofar as the followings are installed:
- python 3.9 (including pip3)
- virtualenv
***

## 3. Installation <a name="installation"></a>
__Download the project:__    
_Via Git_      
$ git clone https://github.com/AxAks/P7_AlgoInvestTrade.git    
    
_Via the Web_     
- Visit the page : https://github.com/AxAks/P7_AlgoInvestTrade      
- Click on the button "Code"     
- Download the project    


__Linux / Mac__       
in the project directory in a shell:       
_create the virtual environment_       
$ python3.9 -m virtualenv 'venv_name'        
_activate the environment:_        
$ source 'venv_name'/bin/activate         
_install project requirements:_       
$ pip install -r requirements.txt         
  
__Windows__    
in the project directory in a shell:        
_create the virtual environment_      
$ virtualenv 'venv_name'      
_activate the environment:_     
$ C:\Users\'Username'\'venv_name'\Scripts\activate.bat       
_install project requirements:_            
$ pip install -r requirements.txt
***

## 4. Execution <a name="execution"></a>
from the terminal, in the root directory of the project:

_activate the environment:_    
$ source 'venv_name'/bin/activate    
     
_launch the script_:       
$ python bruteforce.py [csv_filepath] [cost_limit]       
(cost limit is optional, set by default on 500)
or    
$ python optimized.py [csv_filepath] [cost_limit] 
(cost limit is optional, set by default on 500)  

-> the script is executed
***

## 5. Bruteforce Algorithm <a name="bruteforce"></a>
This script is linear and evaluates all options.
- It generates all possible fortfolios for the given list shares.
- It checks their cost acceptability
- It compares them with the previous one,
- It keeps the higher-profit portfolio.
- In the end, the best result is kept 
  
Extra options:
- secure mode: Boolean, default = False -> write the current best result in a buffer file
- scan segmentation (scan_start/scan_strength): Boolean, default = step 1 to 20 -> choose scan step to begin/end with
- replacement : Boolean, default = False -> can a share be bought several times
***

## 6. Optimized Algorithm <a name="optimized"></a>
This script (...)
- It sorts the shares of the given list by score (Return on Investment)
- It then fills the portfolio with the shares until the cost limit is reached and return the built portfolio
***