from pico2d import *


def select_stage():
    global Playing
    global Selecting
    global IsClear
    global stage
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            Playing = False
            Selecting = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                Playing = False
                Selecting = False
            elif event.key == SDLK_UP:
                stage = (stage - 1) % 3
            elif event.key == SDLK_DOWN:
                stage = (stage + 1) % 3
            elif event.key == SDLK_RETURN:
                Selecting = False
                Playing = False
    pass


def handle_events():
    global Playing
    global IsClear, KeyBoardDic, CharacterAnimation
    global InDungeon
    global stage, Combo
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Playing = False
            InDungeon = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                Playing = False
                InDungeon = False
            elif event.key == SDLK_w:
                KeyBoardDic.update(w=True)
            elif event.key == SDLK_s:
                KeyBoardDic.update(s=True)
            elif event.key == SDLK_a:
                KeyBoardDic.update(a=True)
            elif event.key == SDLK_d:
                KeyBoardDic.update(d=True)
            elif event.key == SDLK_SPACE:
                if not CharacterState == 0:
                    CharacterAnimation = 0
                KeyBoardDic.update(space=True)
            elif event.key == SDLK_j:
                if not CharacterState == 2:
                    CharacterAnimation = 0
                KeyBoardDic.update(j=True)
            elif event.key == SDLK_k:
                if not CharacterState == 1:
                    CharacterAnimation = 0
                KeyBoardDic.update(k=True)

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_k:
                KeyBoardDic.update(k=False)
            elif event.key == SDLK_w:
                KeyBoardDic.update(w=False)
            elif event.key == SDLK_s:
                KeyBoardDic.update(s=False)
            elif event.key == SDLK_a:
                KeyBoardDic.update(a=False)
            elif event.key == SDLK_d:
                KeyBoardDic.update(d=False)

    pass


def update_state():
    global CharacterState

    if KeyBoardDic['space']:
        KeyBoardDic.update(j=False)
        CharacterState = 0

    elif KeyBoardDic['k']:
        KeyBoardDic.update(j=False)
        CharacterState = 1

    elif KeyBoardDic['j']:
        CharacterState = 2

    elif KeyBoardDic['w']:
        CharacterState = 3

    elif KeyBoardDic['s']:
        CharacterState = 4

    elif KeyBoardDic['a']:
        CharacterState = 5

    elif KeyBoardDic['d']:
        CharacterState = 6

    else:
        CharacterState = 7
    pass


def update_character():
    global CharacterState, CharacterX, CharacterY
    global CharacterAnimationDir

    if CharacterState == 0:
        if CharacterAnimationDir == 0:
            if CharacterY < Height - 80:
                CharacterY += 1.5

        elif CharacterAnimationDir == 1:
            if CharacterY > 120:
                CharacterY -= 1.5

        elif CharacterAnimationDir == 2:
            if CharacterX > 160:
                CharacterX -= 1.5

        elif CharacterAnimationDir == 3:
            if CharacterX < Width - 160:
                CharacterX += 1.5

    elif CharacterState == 3:
        CharacterAnimationDir = 0
        if CharacterY < Height - 80:
            CharacterY += 1

    elif CharacterState == 4:
        CharacterAnimationDir = 1
        if CharacterY > 120:
            CharacterY -= 1

    elif CharacterState == 5:
        CharacterAnimationDir = 2
        if CharacterX > 160:
            CharacterX -= 1

    elif CharacterState == 6:
        CharacterAnimationDir = 3
        if CharacterX < Width - 160:
            CharacterX += 1
    pass


def character_draw():
    global CharacterX, CharacterY
    if CharacterState == 0:
        CharacterRoll.clip_draw(100 * CharacterAnimation, 100 * CharacterAnimationDir, 100, 100, CharacterX, CharacterY)
    elif CharacterState == 1:
        CharacterShield.clip_draw(100 * CharacterAnimation, 100 * CharacterAnimationDir,
                                  100, 100, CharacterX, CharacterY)
    elif CharacterState == 2:
        if CharacterAnimationDir > 1:
            CharacterAttack.clip_draw(400 * CharacterAnimation, 400 * CharacterAnimationDir,
                                      400, 400, CharacterX, CharacterY - 15)
        else:
            CharacterAttack.clip_draw(400 * CharacterAnimation, 400 * CharacterAnimationDir,
                                      400, 400, CharacterX, CharacterY)

    elif 2 < CharacterState < 7:
        CharacterWalk.clip_draw(100 * CharacterAnimation, 100 * CharacterAnimationDir, 100, 100, CharacterX, CharacterY)
    else:
        CharacterIdle.clip_draw(100 * CharacterAnimation, 100 * CharacterAnimationDir, 100, 100, CharacterX, CharacterY)


def update_animation():
    global CharacterAnimation, DoorAnimation

    if CharacterState == 0:
        if CharacterAnimation == 7:
            KeyBoardDic.update(space=False)
        CharacterAnimation = (CharacterAnimation + 1) % 8
    elif CharacterState == 1:
        CharacterAnimation = (CharacterAnimation + 1) % blocked
    elif CharacterState == 2:
        if CharacterAnimation > 16:
            KeyBoardDic.update(j=False)
        CharacterAnimation = (CharacterAnimation + 1) % 18

    elif 2 < CharacterState < 9:
        CharacterAnimation = (CharacterAnimation + 1) % 8

    if IsClear:
        if DoorAnimation < 11:
            DoorAnimation += 1
    else:
        if DoorAnimation < 7:
            DoorAnimation += 1
    pass


Width, Height = 1276, 720
open_canvas(Width, Height)

stageSelect = []
stageSelect.append(load_image("map/Stage_Normal.png"))
stageSelect.append(load_image("map/Stage_Hard.png"))
stageSelect.append(load_image("map/Stage_VeryHard.png"))

DungeonBK = load_image("map/Dungeon_BK.png")
DungeonBK2 = load_image("map/BKWalls.png")

DungeonDoor = load_image("map/Door.png")

CharacterRoll = load_image("player/player_roll.png")
CharacterDie = load_image("player/Player_Die.png")
CharacterIdle = load_image("player/player_idle.png")
CharacterWalk = load_image("player/player_walk.png")
CharacterAttack = load_image("player/player_attack.png")
CharacterShield = load_image("player/player_shield_defense.png")

CharacterX = Width // 2
CharacterY = Height // 2

# village.draw(CharacterX, CharacterY)
# dungeon.draw(DungeonWidth // 2, DungeonHeight // 2)

KeyBoardDic = {'w': False, 's': False, 'a': False, 'd': False, 'space': False, 'j': False, 'k': False}

Playing = True
Selecting = True
InDungeon = True
IsClear = False
stage = 0
DoorAnimation = 0
AnimationClock = 0
CharacterAnimation = 0
CharacterAnimationDir = 0
CharacterState = 0
blocked = 1

while Playing:
    # while Selecting:
    #     clear_canvas()
    #     stageSelect[stage].draw(Width // 2, Height // 2)
    #     update_canvas()
    #     select_stage()

    while InDungeon:
        clear_canvas()
        DungeonBK.draw(Width // 2, Height // 2)
        DungeonBK2.draw(Width // 2, Height // 2)
        DungeonDoor.clip_draw(200 * DoorAnimation, 0, 200, 200, Width // 2, Height - 60)
        if AnimationClock % 45 == 0:
            update_animation()

        if AnimationClock % 2 == 0:
            update_state()
            update_character()

        AnimationClock = (AnimationClock + 1) % 100
        character_draw()
        update_canvas()
        handle_events()
        pass

close_canvas()
