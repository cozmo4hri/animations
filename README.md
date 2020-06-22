**Cozmo animations**

This repository contains all the recordings for the Cozmo animations (app version 1.5.0), as well as a script to run the animations. You can use these recordings for your experiments or use the code to run/call individual animations.

Recordings were made in two sessions (Summer 2017 and Summer 2020). The complete list of the animations can be found in the anim_record.csv file. 

*Set 1 (348 animations)*

The animation group name (e.g., ‘ask’, ‘badword’, ‘turtleroll’, ‘hiccup’) were used to subjectively classify the animation as either social or not social. These animations were then recorded and rated by independent raters (n = 264). 

*Set 2 (442 animations)*

The remaining 442 animations were recorded and rating by independent raters use the same procedure as for the first set. 

The code for these experiments can be found in the [emotion classification repository](https://github.com/cozmo4hri/emotion-classification/).

**Code**

Use the the code to call individual animations
1.	Turn Cozmo on
2.	Connect to the SDK
3.	Run a command, for example:

```python record_anim.py -index_list=97```

The full specification is:

```python record_anim.py -h (--help) [-i (--index) -n (--name) --name_list= --index_list=]```

For help add:
-h (--help)           Show the help string
                
To start from a specific point do:  
-i= (--index=)      Play all animation starting from given id  
```python record_anim.py -i=8```  
play animation starting from 'Animation number=8' from anim database  
                
-n= (--name=)       Play all animation starting from given id  
```python record_anim.py -n=anim_hiccup_01```  
play animation starting from 'Animation name=anim_hiccup_01' from anim database  

Logging arguments:  
--name_list=        Play only animation names provided. (Do not put space between animation names)   
```python record_anim.py -name_list=anim_hiccup_01,anim_dizzy_pickup_03,anim_keepaway_wingame_03```   

--index_list=       Optional last argument to ignore logging to file  
```python record_anim.py -index_list=1,6,23,189,76```  
