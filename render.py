import bpy
import math
from time import sleep
from math import tau
import mathutils
from enum import Enum
from random import random

parts = {}

class Lifestage(Enum):
    BABY = 0
    CHILD = 1
    ADOLESCENT = 2
    YOUTH = 3
    ADULT = 4
    AGED = 5
    SENIOR = 6

def lifestage_to_pathName(x):
    return {
        Lifestage.BABY: 'Baby-',
        Lifestage.CHILD: 'Child-',
        Lifestage.ADOLESCENT: 'Adolescent-',
        Lifestage.YOUTH: 'Youth-',
        Lifestage.ADULT: 'Adult-',
        Lifestage.AGED: 'Aged-',
        Lifestage.SENIOR: 'Senior-',
    }.get(x, 'ERROR-')

class Sex(Enum):
    FEMALE = 0
    MALE = 1

def sex_to_pathName(x):
    return {
        Sex.FEMALE: 'Female',
        Sex.MALE: 'Male',
    }.get(x, 'ERROR-')
#This script assumes all rendered objects are children of the 'body' object (the first object in the list).
#The 'body' object may have as many grandchildren and great-grandchildren etc. as you want as want.
#For each object in the body part list below, that object and all its children *which aren't also in the list* will be rendered.
#So in practice, when rendering the thigh, the object listed as 'thighLeft' will be rendered, along with all its children except the 'shinLeft'.

lifestage = Lifestage.ADULT

sex = Sex.MALE

#Begin body part list.
partNames = {
    'body':                         'norn_body',
    
    'body-pregnant1':                'norn_body',
    'body-pregnant2':                'norn_body',
    'body-pregnant3':                'norn_body',
    
    'head-neutral':                 'head',
    'eyelid-left-neutral-open':     'eyelid_l',
    'eyelid-right-neutral-open':    'eyelid_r',
    'eyelid-left-neutral-closed':   'eyelid_l',
    'eyelid-right-neutral-closed':  'eyelid_r',
    
    'head-happy':                   'head',
    'eyelid-left-happy-open':       'eyelid_l',
    'eyelid-right-happy-open':      'eyelid_r',
    'eyelid-left-happy-closed':     'eyelid_l',
    'eyelid-right-happy-closed':    'eyelid_r',
    
    'head-sad':                     'head',
    'eyelid-left-sad-open':         'eyelid_l',
    'eyelid-right-sad-open':        'eyelid_r',
    'eyelid-left-sad-closed':       'eyelid_l',
    'eyelid-right-sad-closed':      'eyelid_r',
    
    'head-angry':                    'head',
    'eyelid-left-angry-open':       'eyelid_l',
    'eyelid-right-angry-open':      'eyelid_r',
    'eyelid-left-angry-closed':     'eyelid_l',
    'eyelid-right-angry-closed':    'eyelid_r',
    
    'head-scared':                  'head',
    'eyelid-left-scared-open':      'eyelid_l',
    'eyelid-right-scared-open':     'eyelid_r',
    'eyelid-left-scared-closed':    'eyelid_l',
    'eyelid-right-scared-closed':   'eyelid_r',
    
    'head-tired':                   'head',
    'eyelid-left-tired-open':       'eyelid_l',
    'eyelid-right-tired-open':      'eyelid_r',
    'eyelid-left-tired-closed':     'eyelid_l',
    'eyelid-right-tired-closed':    'eyelid_r',
    
    'thigh-left':                   'thigh_l',
    'shin-left':                    'shin left',
    'foot-left-tipToes':            'foot left',
    'foot-left-toeDown':            'foot left',
    'foot-left-flat':               'foot left',
    'foot-left-heelDown':           'foot left',

    'thigh-right':                  'thigh_r',
    'shin-right':                   'shin_r',
    'foot-right-tipToes':           'foot_r',
    'foot-right-toeDown':           'foot_r',
    'foot-right-flat':              'foot_r',
    'foot-right-heelDown':          'foot_r',
    
    'humerus-left':                 'upper arm left',
    'radius-left':                  'lower arm left',
    
    'humerus-right':                'upper arm right',
    'radius-right':                 'lower arm right',
    
    'tailRoot':                     'tail base',
    'tailTip-level':                 'tail tuft',
    'tailTip-up':                   'tail tuft',
    'tailTip-straightUp':           'tail tuft',
    'tailTip-curved':               'tail tuft',
}
#End body part list.

#folder to save files in:
outputDir = 'python-script-output/'

#resolution
res_x = 70
res_y = res_x

#distance camera is from each object:
camera_distance = 7

#Begin script.
camera = None

class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    FORWARD = 2
    BACK = 3

def direction_to_pathName(x):
    return {
        Direction.RIGHT: 'Right-',
        Direction.LEFT: 'Left-',
        Direction.FORWARD: 'Forward-',
        Direction.BACK: 'Back-',
    }.get(x, 'ERROR-')

def direction_to_angle(x):
    return {
        Direction.LEFT: (0/4)*tau,
        Direction.BACK: (1/4)*tau,
        Direction.RIGHT: (2/4)*tau,
        Direction.FORWARD: (3/4)*tau,
    }.get(x)

class Emotion(Enum):
    NEUTRAL = 0
    HAPPY = 1
    SAD = 2
    ANGRY = 3
    SCARED = 4
    TIRED = 5

def emotion_to_pathName(x):
    return {
        Emotion.NEUTRAL: 'Neutral-',
        Emotion.HAPPY: 'Happy-',
        Emotion.SAD: 'Sad-',
        Emotion.ANGRY: 'Angry-',
        Emotion.SCARED: 'Scared-',
        Emotion.TIRED: 'Tired-',
    }.get(x, 'ERROR-')

class Eyelids(Enum):
    OPEN = 0
    CLOSED = 1

def eyelids_to_pathName(x):
    return {
        Eyelids.OPEN: 'Open-',
        Eyelids.CLOSED: 'Closed-',
    }.get(x, 'ERROR-')

class HeadAngle(Enum):
    DOWN = 0
    LEVEL = 1
    UP = 2
    UP_MORE = 3

def headAngle_to_pathName(x):
    return {
        HeadAngle.DOWN: 'Down',
        HeadAngle.LEVEL: 'Level',
        HeadAngle.UP: 'Up',
        HeadAngle.UP_MORE: 'UpMore',
    }.get(x, 'ERROR')

def headAngle_to_angle(x):
    return {
        HeadAngle.DOWN: (0.05)*tau,
        HeadAngle.LEVEL: (0)*tau,
        HeadAngle.UP: (-0.05)*tau,
        HeadAngle.UP_MORE: (-0.1)*tau,
    }.get(x)

#class Pregnant(Enum):
#    NOT = 0
#    ONE = 1
#    TWO = 2
#    THREE = 3

#def pregnant_to_pathName(x):
#    return {
#        Pregnant.NOT: 'NotPregnant-',
#        Pregnant.ONE: 'Pregnant1-',
#        Pregnant.TWO: 'Pregnant2-',
#        Pregnant.THREE: 'Pregnant3-',
#    }.get(x, 'ERROR-')

#class BodyAngle(Enum):
#    DOWN = 0
#    LEVEL = 1
#    UP = 2
#    UP_MORE = 3

#def bodyAngle_to_pathName(x):
#    return {
#        BodyAngle.DOWN: 'Down',
#        BodyAngle.LEVEL: 'Level',
#        BodyAngle.UP: 'Up',
#        BodyAngle.UP_MORE: 'UpMore',
#    }.get(x, 'ERROR')

#class ThighAngle(Enum):
#    BACK = 0
#    DOWN = 1
#    UP = 2
#    UP_MORE = 3

#def thighAngle_to_pathName(x):
#    return {
#        ThighAngle.BACK: 'Down',
#        ThighAngle.DOWN: 'Level',
#        ThighAngle.UP: 'Up',
#        ThighAngle.UP_MORE: 'UpMore',
#    }.get(x, 'ERROR')

#class ShinAngle(Enum):
#    UP_MOST = 0
#    UP_MORE = 1
#    UP = 2
#    DOWN = 3

#def shinAngle_to_pathName(x):
#    return {
#        ShinAngle.UP_MOST: 'UpMost',
#        ShinAngle.UP_MORE: 'UpMore',
#        ShinAngle.UP: 'Up',
#        ShinAngle.DOWN: 'Down',
#    }.get(x, 'ERROR')

#class FootAngle(Enum):
#    TIP_TOES = 0
#    TOE_DOWN = 1
#    FLAT = 2
#    HEEL_DOWN = 3

#def footAngle_to_pathName(x):
#    return {
#        FootAngle.TIP_TOES: 'TipToes',
#        FootAngle.TOE_DOWN: 'ToesDown',
#        FootAngle.FLAT: 'Flat',
#        FootAngle.HEEL_DOWN: 'HeelDown',
#    }.get(x, 'ERROR')
#    
#class HumerusAngle(Enum):
#    BACK = 0
#    DOWN = 1
#    LEVEL = 2
#    UP = 3

#def humerusAngle_to_pathName(x):
#    return {
#        HumerusAngle.BACK: 'Back',
#        HumerusAngle.DOWN: 'Down',
#        HumerusAngle.LEVEL: 'Level',
#        HumerusAngle.UP: 'Up',
#    }.get(x, 'ERROR')
#    
#class RadiusAngle(Enum):
#    BACK = 0
#    FORWARD = 1
#    LEVEL = 2
#    UP = 3

#def radiusAngle_to_pathName(x):
#    return {
#        RadiusAngle.BACK: 'Back',
#        RadiusAngle.FORWARD: 'Down',
#        RadiusAngle.LEVEL: 'Level',
#        RadiusAngle.UP: 'Up',
#    }.get(x, 'ERROR')
#    
#class TailrootAngle(Enum):
#    LEVEL = 0
#    UP = 1
#    UP_MORE = 2
#    UP_MOST = 3

#def tailrootAngle_to_pathName(x):
#    return {
#        TailrootAngle.LEVEL: 'Back',
#        TailrootAngle.UP: 'Down',
#        TailrootAngle.UP_MORE: 'Level',
#        TailrootAngle.UP_MOST: 'Up',
#    }.get(x, 'ERROR')
#    
#class TailtipAngle(Enum):
#    LEVEL = 0
#    UP = 1
#    STRAIGHT_UP = 2
#    CURVED = 3

#def tailtipAngle_to_pathName(x):
#    return {
#        TailtipAngle.LEVEL: 'Down',
#        TailtipAngle.UP: 'Up',
#        TailtipAngle.STRAIGHT_UP: 'StraightUp',
#        TailtipAngle.CURVED: 'Curved',
#    }.get(x, 'ERROR')

def directionAndAngle_to_angle(dir, dirAngle, angle):
    return {
        Direction.LEFT: (dirAngle, 0, -angle),
        Direction.BACK: (dirAngle, -angle, 0),
        Direction.RIGHT: (dirAngle, 0, angle),
        Direction.FORWARD: (dirAngle, angle, 0),
    }.get(dir)

def init():
    print('\n------------\n')
    
    renderX = bpy.context.scene.render.resolution_x
    renderY = bpy.context.scene.render.resolution_y
    
    for key in partNames:
        object = bpy.data.objects[partNames[key]]
        children = get_children_grandchildren_etc(object)
        parts[key] = [object] + children

    global camera 
    camera = bpy.data.objects['Camera']
    cameraDistance = 20
    
        
    bpy.context.scene.render.resolution_x = res_x
    bpy.context.scene.render.resolution_y = res_y
    
    render_all(get_lifestageSex_path_name(lifestage, sex, outputDir))
    
    bpy.context.scene.render.resolution_x = renderX
    bpy.context.scene.render.resolution_y = renderY

def get_children_grandchildren_etc(ob):
    children = [ob_child for ob_child in bpy.data.objects if ob_child.parent == ob and ob_child.name not in partNames.values()]
    children2 = [ob_child for ob_child in bpy.data.objects if ob_child.parent in children and ob_child.name not in partNames.values()]
    return children + children2


def get_lifestageSex_path_name(lifestage, sex, pathName):
    return (
        pathName + str(lifestage.value) + str(sex.value)
        + "-" + lifestage_to_pathName(lifestage) + sex_to_pathName(sex) + "/"
    )

def render_all(pathName):
    render_head(
        parts['head-neutral'] + parts['eyelid-left-neutral-open'] + parts['eyelid-right-neutral-open'],
        Emotion.NEUTRAL,
        Eyelids.OPEN,
        pathName
    )
#    render_head(
#        parts['head-neutral'] + parts['eyelid-left-neutral-closed'] + parts['eyelid-right-neutral-closed'],
#        Emotion.NEUTRAL,
#        Eyelids.CLOSED,
#        pathName
#    )
#    render_head(
#        parts['head-happy'] + parts['eyelid-left-happy-open'] + parts['eyelid-right-happy-open'],
#        Emotion.HAPPY,
#        Eyelids.OPEN,
#        pathName
#    )
#    render_head(
#        parts['head-happy'] + parts['eyelid-left-happy-closed'] + parts['eyelid-right-happy-closed'],
#        Emotion.HAPPY,
#        Eyelids.CLOSED,
#        pathName
#    )
#    render_head(
#        parts['head-sad'] + parts['eyelid-left-sad-open'] + parts['eyelid-right-sad-open'],
#        Emotion.SAD,
#        Eyelids.OPEN,
#        pathName
#    )
#    render_head(
#        parts['head-sad'] + parts['eyelid-left-sad-closed'] + parts['eyelid-right-sad-closed'],
#        Emotion.SAD,
#        Eyelids.CLOSED,
#        pathName
#    )
#    render_head(
#        parts['head-angry'] + parts['eyelid-left-angry-open'] + parts['eyelid-right-angry-open'],
#        Emotion.ANGRY,
#        Eyelids.OPEN,
#        pathName
#    )
#    render_head(
#        parts['head-angry'] + parts['eyelid-left-angry-closed'] + parts['eyelid-right-angry-closed'],
#        Emotion.ANGRY,
#        Eyelids.CLOSED,
#        pathName
#    )
#    render_head(
#        parts['head-scared'] + parts['eyelid-left-scared-open'] + parts['eyelid-right-scared-open'],
#        Emotion.SCARED,
#        Eyelids.OPEN,
#        pathName
#    )
#    render_head(
#        parts['head-scared'] + parts['eyelid-left-scared-closed'] + parts['eyelid-right-scared-closed'],
#        Emotion.SCARED,
#        Eyelids.CLOSED,
#        pathName
#    )
#    render_head(
#        parts['head-tired'] + parts['eyelid-left-tired-open'] + parts['eyelid-right-tired-open'],
#        Emotion.TIRED,
#        Eyelids.OPEN,
#        pathName
#    )
#    render_head(
#        parts['head-tired'] + parts['eyelid-left-tired-closed'] + parts['eyelid-right-tired-closed'],
#        Emotion.TIRED,
#        Eyelids.CLOSED,
#        pathName
#    )
#    
#    render_body(
#        parts['body'],
#        Pregnant.NOT,
#        pathName
#    )
#    render_body(
#        parts['body-pregnant1'],
#        Pregnant.ONE,
#        pathName
#    )
#    render_body(
#        parts['body-pregnant2'],
#        Pregnant.TWO,
#        pathName
#    )
#    render_body(
#        parts['body-pregnant3'],
#        Pregnant.THREE,
#        pathName
#    )
#    
#    render_thighLeft(
#        parts['thigh-left'],
#        pathName
#    )
#    render_shinLeft(
#        parts['shin-left'],
#        pathName
#    )
#    render_footLeft(
#        parts['foot-left-tipToes'],
#        FootAngle.TIP_TOES,
#        pathName
#    )
#    render_footLeft(
#        parts['foot-left-toeDown'],
#        FootAngle.TOE_DOWN,
#        pathName
#    )
#    render_footLeft(
#        parts['foot-left-flat'],
#        FootAngle.FLAT,
#        pathName
#    )
#    render_footLeft(
#        parts['foot-left-heelDown'],
#        FootAngle.HEEL_DOWN,
#        pathName
#    )
#    
#    render_thighRight(
#        parts['thigh-right'],
#        pathName
#    )
#    render_shinRight(
#        parts['shin-right'],
#        pathName
#    )
#    render_footRight(
#        parts['foot-right-tipToes'],
#        FootAngle.TIP_TOES,
#        pathName
#    )
#    render_footRight(
#        parts['foot-right-toeDown'],
#        FootAngle.TOE_DOWN,
#        pathName
#    )
#    render_footRight(
#        parts['foot-right-flat'],
#        FootAngle.FLAT,
#        pathName
#    )
#    render_footRight(
#        parts['foot-right-heelDown'],
#        FootAngle.HEEL_DOWN,
#        pathName
#    )
#    
#    render_humerusLeft(
#        parts['humerus-left'],
#        pathName
#    )
#    render_radiusLeft(
#        parts['radius-left'],
#        pathName
#    )
#    
#    render_humerusRight(
#        parts['humerus-right'],
#        pathName
#    )
#    render_radiusRight(
#        parts['radius-right'],
#        pathName
#    )
#    
#    render_tailRoot(
#        parts['tailRoot'],
#        pathName
#    )
#    render_tailTip(
#        parts['tailTip-level'],
#        TailtipAngle.LEVEL,
#        pathName
#    )
#    render_tailTip(
#        parts['tailTip-up'],
#        TailtipAngle.UP,
#        pathName
#    )
#    render_tailTip(
#        parts['tailTip-straightUp'],
#        TailtipAngle.STRAIGHT_UP,
#        pathName
#    )
#    render_tailTip(
#        parts['tailTip-curved'],
#        TailtipAngle.CURVED,
#        pathName
#    )

def render_head(head, emotion, eyelids, pathName):
    pathName = pathName + 'A-Head/'
    render_head_direction(head, emotion, eyelids, Direction.RIGHT, pathName)
    render_head_direction(head, emotion, eyelids, Direction.LEFT, pathName)
    render_head_direction(head, emotion, eyelids, Direction.FORWARD, pathName)
    render_head_direction(head, emotion, eyelids, Direction.BACK, pathName)

def render_head_direction(head, emotion, eyelids, direction, pathName):
    render_head_direction_angle(head, emotion, eyelids, direction, HeadAngle.DOWN, pathName)
    render_head_direction_angle(head, emotion, eyelids, direction, HeadAngle.LEVEL, pathName)
    render_head_direction_angle(head, emotion, eyelids, direction, HeadAngle.UP, pathName)
    render_head_direction_angle(head, emotion, eyelids, direction, HeadAngle.UP_MORE, pathName)

def render_head_direction_angle(head, emotion, eyelids, direction, angle, pathName):    
    file = get_head_path_name(emotion, eyelids, direction, angle, pathName)
    print("Rendering: " + file)
    #angle = (headAngle_to_angle(angle), 0, direction_to_angle(direction))
    #angle = (0, 0, random()*6.28318)
    #angle = (0, 0, direction_to_angle(direction))
    angle = directionAndAngle_to_angle(direction, direction_to_angle(direction), headAngle_to_angle(angle))
    renderAngle(head[0], angle, file)
    

def get_head_path_name(emotion, eyelids, direction, angle, pathName):
    return (
        pathName + str(emotion.value) + str(eyelids.value) + str(direction.value) + str(angle.value) 
        + "-" + emotion_to_pathName(emotion) + eyelids_to_pathName(eyelids) + direction_to_pathName(direction) + headAngle_to_pathName(angle)
        + ".png"
    )


#def render_body(body, pregnant, pathName):
#    pathName = pathName + 'B-Body/'
#    render_body_direction(body, pregnant, Direction.RIGHT, pathName)
#    render_body_direction(body, pregnant, Direction.LEFT, pathName)
#    render_body_direction(body, pregnant, Direction.FORWARD, pathName)
#    render_body_direction(body, pregnant, Direction.BACK, pathName)

#def render_body_direction(body, pregnant, direction, pathName):
#    render_body_direction_angle(body, pregnant, direction, BodyAngle.DOWN, pathName)
#    render_body_direction_angle(body, pregnant, direction, BodyAngle.LEVEL, pathName)
#    render_body_direction_angle(body, pregnant, direction, BodyAngle.UP, pathName)
#    render_body_direction_angle(body, pregnant, direction, BodyAngle.UP_MORE, pathName)

#def render_body_direction_angle(head, pregnant, direction, angle, pathName):    
#    file = get_body_path_name(pregnant, direction, angle, pathName)
#    print("Rendering: " + file)
#    

#def get_body_path_name(pregnant, direction, angle, pathName):
#    return (
#        pathName + str(pregnant.value) + str(direction.value) + str(angle.value) 
#        + "-" + pregnant_to_pathName(pregnant) + direction_to_pathName(direction) + bodyAngle_to_pathName(angle)
#        + ".png"
#    )


#def render_thighLeft(body, pathName):
#    pathName = pathName + 'C-Thigh-Left/'
#    render_thigh_direction(body, Direction.RIGHT, pathName)
#    render_thigh_direction(body, Direction.LEFT, pathName)
#    render_thigh_direction(body, Direction.FORWARD, pathName)
#    render_thigh_direction(body, Direction.BACK, pathName)

#def render_thighRight(body, pathName):
#    pathName = pathName + 'F-Thigh-Right/'
#    render_thigh_direction(body, Direction.RIGHT, pathName)
#    render_thigh_direction(body, Direction.LEFT, pathName)
#    render_thigh_direction(body, Direction.FORWARD, pathName)
#    render_thigh_direction(body, Direction.BACK, pathName)

#def render_thigh_direction(body, direction, pathName):
#    render_thigh_direction_angle(body, direction, ThighAngle.BACK, pathName)
#    render_thigh_direction_angle(body, direction, ThighAngle.DOWN, pathName)
#    render_thigh_direction_angle(body, direction, ThighAngle.UP, pathName)
#    render_thigh_direction_angle(body, direction, ThighAngle.UP_MORE, pathName)

#def render_thigh_direction_angle(head, direction, angle, pathName):    
#    file = get_thigh_path_name(direction, angle, pathName)
#    print("Rendering: " + file)
#    

#def get_thigh_path_name(direction, angle, pathName):
#    return (
#        pathName + str(direction.value) + str(angle.value) 
#        + "-" + direction_to_pathName(direction) + thighAngle_to_pathName(angle)
#        + ".png"
#    )


#def render_shinLeft(body, pathName):
#    pathName = pathName + 'D-Shin-Left/'
#    render_shin_direction(body, Direction.RIGHT, pathName)
#    render_shin_direction(body, Direction.LEFT, pathName)
#    render_shin_direction(body, Direction.FORWARD, pathName)
#    render_shin_direction(body, Direction.BACK, pathName)

#def render_shinRight(body, pathName):
#    pathName = pathName + 'G-Shin-Right/'
#    render_shin_direction(body, Direction.RIGHT, pathName)
#    render_shin_direction(body, Direction.LEFT, pathName)
#    render_shin_direction(body, Direction.FORWARD, pathName)
#    render_shin_direction(body, Direction.BACK, pathName)

#def render_shin_direction(body, direction, pathName):
#    render_shin_direction_angle(body, direction, ShinAngle.UP_MOST, pathName)
#    render_shin_direction_angle(body, direction, ShinAngle.UP_MORE, pathName)
#    render_shin_direction_angle(body, direction, ShinAngle.UP, pathName)
#    render_shin_direction_angle(body, direction, ShinAngle.DOWN, pathName)

#def render_shin_direction_angle(head, direction, angle, pathName):    
#    file = get_shin_path_name(direction, angle, pathName)
#    print("Rendering: " + file)
#    
#def get_shin_path_name(direction, angle, pathName):
#    return (
#        pathName + str(direction.value) + str(angle.value) 
#        + "-" + direction_to_pathName(direction) + shinAngle_to_pathName(angle)
#        + ".png"
#    )


#def render_footLeft(foot, angle, pathName):
#    pathName = pathName + 'E-Foot-Left/'
#    render_foot_direction_angle(foot, Direction.RIGHT, angle, pathName)
#    render_foot_direction_angle(foot, Direction.LEFT, angle, pathName)
#    render_foot_direction_angle(foot, Direction.FORWARD, angle, pathName)
#    render_foot_direction_angle(foot, Direction.BACK, angle, pathName)

#def render_footRight(foot, angle, pathName):
#    pathName = pathName + 'H-Foot-Right/'
#    render_foot_direction_angle(foot, Direction.RIGHT, angle, pathName)
#    render_foot_direction_angle(foot, Direction.LEFT, angle, pathName)
#    render_foot_direction_angle(foot, Direction.FORWARD, angle, pathName)
#    render_foot_direction_angle(foot, Direction.BACK, angle, pathName)

#def render_foot_direction_angle(foot, direction, angle, pathName):    
#    file = get_foot_path_name(direction, angle, pathName)
#    print("Rendering: " + file)
#    

#def get_foot_path_name(direction, angle, pathName):
#    return (
#        pathName + str(direction.value) + str(angle.value) 
#        + "-" + direction_to_pathName(direction) + footAngle_to_pathName(angle)
#        + ".png"
#    )


#def render_humerusLeft(body, pathName):
#    pathName = pathName + 'I-Humerus-Left/'
#    render_humerus_direction(body, Direction.RIGHT, pathName)
#    render_humerus_direction(body, Direction.LEFT, pathName)
#    render_humerus_direction(body, Direction.FORWARD, pathName)
#    render_humerus_direction(body, Direction.BACK, pathName)

#def render_humerusRight(body, pathName):
#    pathName = pathName + 'K-Humerus-Right/'
#    render_humerus_direction(body, Direction.RIGHT, pathName)
#    render_humerus_direction(body, Direction.LEFT, pathName)
#    render_humerus_direction(body, Direction.FORWARD, pathName)
#    render_humerus_direction(body, Direction.BACK, pathName)

#def render_humerus_direction(body, direction, pathName):
#    render_humerus_direction_angle(body, direction, HumerusAngle.BACK, pathName)
#    render_humerus_direction_angle(body, direction, HumerusAngle.DOWN, pathName)
#    render_humerus_direction_angle(body, direction, HumerusAngle.LEVEL, pathName)
#    render_humerus_direction_angle(body, direction, HumerusAngle.UP, pathName)

#def render_humerus_direction_angle(head, direction, angle, pathName):    
#    file = get_humerus_path_name(direction, angle, pathName)
#    print("Rendering: " + file)
#    
#def get_humerus_path_name(direction, angle, pathName):
#    return (
#        pathName + str(direction.value) + str(angle.value) 
#        + "-" + direction_to_pathName(direction) + humerusAngle_to_pathName(angle)
#        + ".png"
#    )


#def render_radiusLeft(body, pathName):
#    pathName = pathName + 'J-Radius-Left/'
#    render_radius_direction(body, Direction.RIGHT, pathName)
#    render_radius_direction(body, Direction.LEFT, pathName)
#    render_radius_direction(body, Direction.FORWARD, pathName)
#    render_radius_direction(body, Direction.BACK, pathName)

#def render_radiusRight(body, pathName):
#    pathName = pathName + 'L-Radius-Right/'
#    render_radius_direction(body, Direction.RIGHT, pathName)
#    render_radius_direction(body, Direction.LEFT, pathName)
#    render_radius_direction(body, Direction.FORWARD, pathName)
#    render_radius_direction(body, Direction.BACK, pathName)

#def render_radius_direction(body, direction, pathName):
#    render_radius_direction_angle(body, direction, RadiusAngle.BACK, pathName)
#    render_radius_direction_angle(body, direction, RadiusAngle.FORWARD, pathName)
#    render_radius_direction_angle(body, direction, RadiusAngle.LEVEL, pathName)
#    render_radius_direction_angle(body, direction, RadiusAngle.UP, pathName)

#def render_radius_direction_angle(head, direction, angle, pathName):    
#    file = get_radius_path_name(direction, angle, pathName)
#    print("Rendering: " + file)
#    
#def get_radius_path_name(direction, angle, pathName):
#    return (
#        pathName + str(direction.value) + str(angle.value) 
#        + "-" + direction_to_pathName(direction) + radiusAngle_to_pathName(angle)
#        + ".png"
#    )


#def render_tailRoot(body, pathName):
#    pathName = pathName + 'M-TailRoot/'
#    render_tailRoot_direction(body, Direction.RIGHT, pathName)
#    render_tailRoot_direction(body, Direction.LEFT, pathName)
#    render_tailRoot_direction(body, Direction.FORWARD, pathName)
#    render_tailRoot_direction(body, Direction.BACK, pathName)

#def render_tailRoot_direction(body, direction, pathName):
#    render_tailRoot_direction_angle(body, direction, TailrootAngle.LEVEL, pathName)
#    render_tailRoot_direction_angle(body, direction, TailrootAngle.UP, pathName)
#    render_tailRoot_direction_angle(body, direction, TailrootAngle.UP_MORE, pathName)
#    render_tailRoot_direction_angle(body, direction, TailrootAngle.UP_MOST, pathName)

#def render_tailRoot_direction_angle(head, direction, angle, pathName):    
#    file = get_tailRoot_pathName(direction, angle, pathName)
#    print("Rendering: " + file)
#    
#def get_tailRoot_pathName(direction, angle, pathName):
#    return (
#        pathName + str(direction.value) + str(angle.value) 
#        + "-" + direction_to_pathName(direction) + tailrootAngle_to_pathName(angle)
#        + ".png"
#    )


#def render_tailTip(body, angle, pathName):
#    pathName = pathName + 'N-TailTip/'
#    render_tailTip_direction_angle(body, Direction.RIGHT, angle, pathName)
#    render_tailTip_direction_angle(body, Direction.LEFT, angle, pathName)
#    render_tailTip_direction_angle(body, Direction.FORWARD, angle, pathName)
#    render_tailTip_direction_angle(body, Direction.BACK, angle, pathName)

#def render_tailTip_direction_angle(head, direction, angle, pathName):    
#    file = get_tailTip_pathName(direction, angle, pathName)
#    print("Rendering: " + file)
#    
#def get_tailTip_pathName(direction, angle, pathName):
#    return (
#        pathName + str(direction.value) + str(angle.value) 
#        + "-" + direction_to_pathName(direction) + tailtipAngle_to_pathName(angle)
#        + ".png"
#    )
















def renderAngle(bodyPart, angleIn, pathname):
    angle = (angleIn[1], 0, angleIn[0])
    
    camera_location = mathutils.Vector((0, camera_distance, 0))
    camera_location.rotate(mathutils.Euler(bodyPart.rotation_euler))
    camera_location.rotate(mathutils.Euler(angle))
    camera_location -= bodyPart.location
    
    camera.location = camera_location
    
    #camera.rotation_euler = camera_location.rotation_difference(Vector(bodyPart.location)).to_euler()
    look_at(camera, bodyPart.location, angleIn[2])
    
    bpy.context.scene.render.filepath = pathname
    bpy.ops.render.render(write_still = True)

def look_at(obj, target, roll=0):

    if not isinstance(target, mathutils.Vector):
        target = mathutils.Vector(target)
    loc = obj.location
    # direction points from the object to the target
    direction = target - loc

    quat = direction.to_track_quat('-Z', 'Y')

    # /usr/share/blender/scripts/addons/add_advanced_objects_menu/arrange_on_curve.py
    quat = quat.to_matrix().to_4x4()
    rollMatrix = mathutils.Matrix.Rotation(roll, 4, 'Z')

    # remember the current location, since assigning to obj.matrix_world changes it
    loc = loc.to_tuple()
    obj.matrix_world = quat @ rollMatrix
    obj.location = loc

def renderAtPositionAngleToFile(camera, position, rotation, fileName):
    camera.location = position
    camera.rotation_euler = (rotation[0], rotation[1], rotation[2])
    bpy.context.scene.render.filepath = fileName
    bpy.ops.render.render(write_still = True)

init()
