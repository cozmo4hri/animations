import cozmo
import getopt
#import msvcrt
import sys
import time
from datetime import datetime

LIST_TYPE_INDEX = 'index'
LIST_TYPE_NAME = 'name'

# where to start playing the animations in record from
start_anim_no = 1
start_anim_name = None
play_from_list = []
list_type = LIST_TYPE_INDEX

def anim_create_master_record(robot: cozmo.robot.Robot):  
    expressive_anim_keys = ['admire',
                            'ask',
                            'badword',
                            'bored',
                            'celebrat',
                            'dizzy',
                            'find',
                            'found',
                            'frustrated',
                            'giggle',
                            'guarddog',
                            'happy',
                            'hello',
                            'hiccup',
                            'highenergy',
                            'ideatoplay',
                            'like',
                            'lowenergy',
                            'match_no',
                            'newarea',
                            'playerno',
                            'petdetection',
                            'playeryes',
                            'request',
                            'reacttocube',
                            'reenrollment',
                            'struggle',
                            'sleep',
                            'stuck',
                            'turtleroll',
                            'thankyou',
                            'turbo',
                            'upgrade',
                            'upset',
                            'wheely',
                            'wiggle',
                            'fail',
                            'lose',
                            'succes',
                            'win',
                            'reacttoface',
                            'others'
                            ]
    all_animations = robot.conn.anim_names
    anim_record = {"others": []}
    
    print("There are %d animations" % len(all_animations))
    count = 0
    # Classify animations according to key
    try:
        for anim in all_animations:
            check_recorded =0
            for anim_key in expressive_anim_keys:
                if anim_key in anim:
                    continue;
                    count = count + 1
                    print("%d Record : %s" % (count, anim))
                    start_time = datetime.now()
                    time.sleep(2)
                    robot.play_anim(anim).wait_for_completed()
                    end_time = datetime.now()
                    anim_time = end_time -start_time
                    if anim_key in anim_record:
                        anim_record[anim_key].append((anim, anim_time))
                    else:
                        anim_record[anim_key] = [(anim, anim_time)]
                    break;
                
                else:
                    check_recorded += 1
                    
            if check_recorded >= len(expressive_anim_keys):
                count = count + 1
                print("%d Record : %s" % (count, anim))
                start_time = datetime.now()
                time.sleep(2)
                robot.play_anim(anim).wait_for_completed()
                end_time = datetime.now()
                anim_time = end_time -start_time
                anim_record['others'].append((anim, anim_time))
                
                    
    except:
        pass
    
    with open('all_anim_record.csv', "w") as fp:
        # record the anims
        fp.write("Animation id, Animation name, Animation group, Play time\n")
        count = 1
        for key, anim_list in sorted(anim_record.items()):
            for value in anim_list:
                fp.write("%s,%s,%s,%s\n" %(count, value[0], key, value[1]))
                count += 1
    fp.close()
    


def cozmo_behaviour_display(robot: cozmo.robot.Robot ):
    global start_anim_no
    global start_anim_name
    
    quit_classifier = False
    
    with open('anim_record.csv', "r") as fp:
        contents = fp.readlines()
    
    anim_index = 0
    if start_anim_name:
        for anim_record in contents:
            if anim_record.split(',')[1] == start_anim_name:
                break
            else:
                anim_index += 1
    elif start_anim_no >0 and start_anim_no < len(contents):
        id_at_position = int(str(contents[start_anim_no]).split(',')[0])
        if id_at_position == start_anim_no:
            # index matches
            anim_index = int(start_anim_no)
        else:
            raise(Exception, "Animation no %s does not match position index provided %s" % (id_at_position, 
                                                                                            start_anim_no))
    else:
        # No choise made start from beginning
        anim_index = 1
        
    if not anim_index or anim_index >= len(contents):
        # No choice match
        print("Exception: Cannot find animation start_point requested")
    # Note contentss[0] is the non animation header
    
    i = anim_index
    anim_index_count = len(contents)
    while i > 0 and i < anim_index_count:
        entry = str(contents[i]).strip().split(',')
        anim_name = entry[1]
        anim_no = entry[0]
        print("Playing animation %s: %s" % (anim_no, anim_name))
        time.sleep(2)
        robot.play_anim(anim_name).wait_for_completed()
        print("Select: r - repeat, b - go back a animation, n - next animation, q - quit program")
        i += 1
        while True:
            try:
                    expression_char = input("Select: r - repeat, b - go back a animation, n - next animation, q - quit program")
                    print("%s" % expression_char)
                    if expression_char in ['r','R']:
                        time.sleep(2)
                        robot.play_anim(anim_name).wait_for_completed()
                        print("Repeated animation %s : %s" % (anim_no, anim_name))
                    elif expression_char in ['b','B']:
                        if i > 2:
                            i -= 2
                        break
                    elif expression_char in ['q','Q']:
                        quit_classifier = True;
                        break
                    elif expression_char in ['n','N']:
                        break 
                    else:
                        print("Entry not valid")
            except:
                    #sometimes non characters throw error
                    print("Entry not valid")
                
            time.sleep(0.5)
        #end while
        if quit_classifier:
            break
    #end for

def cozmo_behaviour_from_list(robot: cozmo.robot.Robot ):
    global play_from_list
    global list_type
    play_list = []
    quit_classifier = False
    
    #prepare the play_lists
    if list_type == LIST_TYPE_NAME:
        for anim in play_from_list:
            play_list.append(anim.strip("'").strip('"').strip())
    elif list_type == LIST_TYPE_INDEX:
        with open('anim_record.csv', "r") as fp:
            contents = fp.readlines()
        for idx in play_from_list:
            try:
                anim_record = contents[int(idx)].split(',')
                if int(anim_record[0]) == int(idx):
                    play_list.append(anim_record[1])
                else:
                    print("Mismatched Animation No (%s) at position (%s) from list" % (idx, anim_record[0]))
            except (IndexError, AttributeError):
                print("No Animation with Animation No: %s" % id)
    print("Animation play-list:  %s" % play_list)
    i = 0
    while i>-1 and i < len(play_list):
        anim_name = play_list[i]
        try:
            print("Playing animation : %s" % (anim_name))
            time.sleep(2)
            robot.play_anim(anim_name).wait_for_completed()
        except:
            print("Animation '%s' is not available" % anim_name)
        i = i + 1
        while True:
            try:
                    expression_char = input("Select: r - repeat, b - go back a animation, n - next animation, q - quit program")
                    print("%s" % expression_char)
                    if expression_char in ['r','R']:
                        time.sleep(2)
                        robot.play_anim(anim_name).wait_for_completed()
                        print("Repeated animation : %s" % (anim_name))
                    elif expression_char in ['b','B']:
                        if i > 1:
                            i -= 2
                            break
                        else:
                            print('No previous behaviour')
                    elif expression_char in ['q','Q']:
                        quit_classifier = True;
                        break
                    elif expression_char in ['n','N']:
                        break 
                    else:
                        print("Entry not valid")
            except:
                    #sometimes non characters throw error
                    print("Entry not valid")
                
            time.sleep(0.5)
        #end while
        if quit_classifier:
            break
            
            

def handle_input(argv):    
    global start_anim_no
    global start_anim_name
    global play_from_list
    global list_type
    
    help_string = 'record_anim.py -h (--help) [-i (--index) -n (--name) --name_list= --index_list=]'
    try:
        opts, args = getopt.getopt(argv, "hi:n:",["help","index", "name", "name_list=", "index_list="])
    except getopt.GetoptError:
        print("%s" % help_string)
        sys.exit(2)
           
            
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("python 'record_anim.py -h (--help) [-i (--index) -n (--name) --name_list= --index_list=]'\n"\
                "-h (--help)           Show the help string\n\n"\
                "Play start from point:\n"\
                "-i= (--index=)      Play all animation starting from given id\n"\
                "                    e.g. python record_anim.py -i=8\n"\
                "                    <play animation starting from 'Animation number=8' from anim database\n\n"\
                "-n= (--name=)       Play all animation starting from given id\n"\
                "                    e.g. python record_anim.py -n=anim_hiccup_01\n"\
                "                    <play animation starting from 'Animation name=anim_hiccup_01' from anim database\n\n"\
                "Logging arguments:\n"\
                "--name_list=        Play only animation names provided. (Donot put space between animation names) \n" \
                "                    e.g. python record_anim.py -name_list=anim_hiccup_01,anim_dizzy_pickup_03,anim_keepaway_wingame_03 \n\n"\
                "--index_list=       Optional last argument to ignore logging to file\n"\
                "                     e.g. python record_anim.py -index_list=1,6,23,189,76")
            sys.exit()
        elif opt in ("-i", "--index"):
            try:
                start_anim_no = int(arg.strip('=').strip(' '))
            except:
                print("Animation index should be a integer")
                break
            cozmo.run_program(cozmo_behaviour_display)
        elif opt in ("-n", "--name"):
            start_anim_name = arg.strip('=').strip(' ')
            cozmo.run_program(cozmo_behaviour_display)
        elif opt in ("--name_list"):
            play_from_list = arg.strip().strip('=').split(',')
            list_type = LIST_TYPE_NAME
            print("This function is not yet ready")
            cozmo.run_program(cozmo_behaviour_from_list)
        elif opt in ("--index_list"):
            play_list = arg.strip().strip('=').split(',')
            for val in play_list:
                play_from_list.append(int(val))
            list_type = LIST_TYPE_INDEX
            print("This function is not yet ready")
            cozmo.run_program(cozmo_behaviour_from_list)
        else:
            print(help_string)
            break  


if __name__ == "__main__":
    #cozmo.run_program(anim_create_master_record)
    if len(sys.argv) != 2:
        print('record_anim.py -h (--help) [-i (--index) -n (--name) --name_list= --index_list=]')
    else: 
        handle_input(sys.argv[1:])



    
