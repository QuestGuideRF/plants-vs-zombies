from pygame import *
from random import *
from math import *
def drawScene (zombiesList ,plantsActionList ,bulletsList ,plantsRechargeList ,shovellingPlant ,selectingPlant ,sunAmount ,plant ,currentScreen ,loseX ):
    if currentScreen !="lose":
        screen .fill ((0 ,0 ,0 ))
        screen .blit (back ,(0 ,0 ))
        blitLawnMower (lawnMowerPic ,lawnMowerList )
        if len (lawnMowerList )>0 :
            checkLawnMower (zombiesList ,lawnMowerList ,runningMowerList )
        if len (runningMowerList )>0 :
            moveLawnMover (zombiesList ,runningMowerList ,length )
        plantAnimation (plantsNameGrid ,plantsSpriteGrid ,plantsHealthGrid ,mineCheckList ,plantsActionList ,zombiesList ,width ,length )
        returnList =zombieAnimation (currentScreen ,zombiesList ,normalZombieList ,normalZombieEat ,zombieObjectList ,plantsNameGrid ,plantsSpriteGrid ,plantsHealthGrid ,plantsActionList ,mineCheckList ,x ,y ,width ,length )
        zombiesList =returnList [0 ]
        currentScreen =returnList [1 ]
        if currentScreen =="lose":
            mixer .music .stop ()
            zombieSpawnTimer =time .set_timer (ZOMBIEEVENT ,0 )
            sunTimer =time .set_timer (SUNEVENT ,0 )
        returnList =plantAction (plantsNameGrid ,sunEnergyList ,mineCheckList ,plantsActionList ,plantsActionTimesList ,bulletsList ,width ,length )
        plantsActionList =returnList [0 ]
        bulletsList =returnList [1 ]
        returnList =checkBullets (bulletsList ,zombiesList )
        bulletsList =returnList [0 ]
        zombiesList =returnList [1 ]
        sunAnimation (sunEnergyList ,sunSpriteList ,length )
        plantsRechargeList =plantRecharge (plantsRechargeList ,plantsRechargeTimesList ,selectedPlants )
        selectPlantBar (selectBar ,selectedPlants ,plantsRechargeList ,plantsRechargeTimesList ,sunAmount ,sunAmountFont )
        screen .blit (shovelPic ,(shovelRect [0 ],shovelRect [1 ]))
        if shovellingPlant ==True :
            screen .blit (shovelCursor ,(mx -shovelCursor .get_width ()//2 ,my -shovelCursor .get_height ()//2 ))
            shovellingPlant =shovelTool (plantsNameGrid ,plantsSpriteGrid ,plantsHealthGrid ,plantsActionList ,mineCheckList ,shovellingPlant ,x ,y ,width ,length )
        if selectingPlant ==True and plant !=""and shovellingPlant ==False :
            pic =eval (plant +"List")[0 ]
            returnList =placePlant (plant ,pic ,sunAmount ,plantsCostList ,plantsNameGrid ,plantsHealthGrid ,plantsHealthList ,plantsSpriteGrid ,plantsActionList ,plantsRechargeList ,selectedPlants ,selectingPlant ,50 ,100 ,width ,length )
            selectingPlant =returnList [0 ]
            plantsRechargeList =returnList [1 ]
            plantsActionList =returnList [2 ]
            sunAmount =returnList [3 ]
            screen .blit (pic ,(mx -pic .get_width ()//2 ,my -pic .get_height ()//2 ))
        else :
            plant =""
        displayWaveAmount =sunAmountFont .render ("Wave: "+str (waveCount ),True ,(0 ,0 ,0 ))
        screen .blit (displayWaveAmount ,(1050 ,750 ))
    elif currentScreen =="lose":
        screen .fill ((0 ,0 ,0 ))
        if loseX <280 :
            loseX +=2
            screen .blit (back1 .subsurface ([290 -loseX ,0 ,1200 ,800 ]),(0 ,0 ))
        else :
            currentScreen ="lost"
            screamSound .play ()
        returnList =zombieAnimation (currentScreen ,zombiesList ,normalZombieList ,normalZombieEat ,zombieObjectList ,plantsNameGrid ,plantsSpriteGrid ,plantsHealthGrid ,plantsActionList ,mineCheckList ,x ,y ,width ,length )
        zombiesList =returnList [0 ]
    display .flip ()
    return [zombiesList ,plantsActionList ,bulletsList ,plantsRechargeList ,shovellingPlant ,selectingPlant ,sunAmount ,plant ,currentScreen ,loseX ]
def inList (item ,twoDList ):
    for oneDList in twoDList :
        if item in oneDList :
            return twoDList .index (oneDList )
    return -1
def addSprites (folder ,subfolder ,group ,name ,start ,end ):
    sprites =[]
    if group =="nut"and name =="nut":
        for i in range (end ):
             sprites .append (image .load ("%s/%s/%s/%s%i-%i.png"%(folder ,subfolder ,group ,name ,start ,i +1 )).convert_alpha ())
    else :
        for i in range (start ,end +1 ):
            sprites .append (image .load ("%s/%s/%s/%s%i.png"%(folder ,subfolder ,group ,name ,i )).convert_alpha ())
    return sprites
def createGrid (cols ,rows ):
    return [[""for a in range (cols )]for b in range (rows )]
def blit_alpha (target ,source ,location ,opacity ):
    x =location [0 ]
    y =location [1 ]
    temp =Surface ((source .get_width (),source .get_height ())).convert ()
    temp .blit (target ,(-x ,-y ))
    temp .blit (source ,(0 ,0 ))
    temp .set_alpha (opacity )
    target .blit (temp ,location )
def selectPlantBar (selectBar ,selectedPlants ,plantsRechargeList ,plantsRechargeTimesList ,sunAmount ,font ):
    screen .blit (selectBar ,(100 ,0 ))
    for ind in range (len (selectedPlants )):
        alphaPacket =False
        listIndex =inList (selectedPlants [ind ],plantsRechargeList )
        if listIndex !=-1 :
            alphaPacket =True
            currentPlant =plantsRechargeList [listIndex ][0 ]
            currentRechargeTime =time .get_ticks ()-plantsRechargeList [listIndex ][1 ]
        pic =eval (selectedPlants [ind ]+"Packet")
        pic =pic .copy ()
        if alphaPacket ==True :
            picAlpha =pic .convert ()
            picAlpha .set_alpha (50 )
            screen .blit (picAlpha ,(200 +75 *ind ,10 ))
            listIndex =inList (currentPlant ,plantsRechargeTimesList )
            rechargeTime =plantsRechargeTimesList [listIndex ][1 ]
            packetLength =int (currentRechargeTime /rechargeTime *90 )
            picNormal =pic .subsurface ([0 ,0 ,65 ,packetLength ])
            screen .blit (picNormal ,(200 +75 *ind ,10 ))
        elif alphaPacket ==False :
            screen .blit (pic ,(200 +75 *ind ,10 ))
    displaySunAmount =sunAmountFont .render (str (sunAmount ),True ,(0 ,0 ,0 ))
    screen .blit (displaySunAmount ,(120 ,80 ))
def shovelTool (plantsNameGrid ,plantsSpriteGrid ,plantsHealthGrid ,plantsActionList ,mineCheckList ,shovellingPlant ,x ,y ,width ,length ):
    oneSpot =0
    for row in range (len (plantsNameGrid )):
        for col in range (len (plantsNameGrid [row ])):
            square =Rect ([x +col *width ,y +row *length ,width ,length ])
            if square .x <mx <(square .x +length )and square .y <my <(square .y +length )and oneSpot !=1 :
                square =Rect ([x +col *width ,y +row *length ,width ,length ])
                oneSpot =1
                if mb [0 ]==1 and plantsNameGrid [row ][col ]!="":
                    shovelPlantSound .play ()
                    removePlant (plantsNameGrid ,plantsSpriteGrid ,plantsHealthGrid ,plantsActionList ,mineCheckList ,row ,col )
                    shovellingPlant =False
            else :
                square =Rect ([x +col *width ,y +row *length ,width ,length ])
                oneSpot =0
    if mb [2 ]==1 :
        shovellingPlant =False
    return shovellingPlant
def blitLawnMower (picture ,rowsList ):
    for row in rowsList :
        screen .blit (picture ,(row [0 ],row [1 ]))
def checkLawnMower (zombiesList ,lawnMowerList ,runningMowerList ):
    for mower in lawnMowerList :
        for zombie in zombiesList :
            if mower [2 ]==zombie [6 ]:
                if Rect (mower [0 ],mower [1 ],90 ,60 ).colliderect (zombie [1 ],zombie [2 ],90 ,100 ):
                    if [mower [0 ],mower [1 ],mower [2 ]]in lawnMowerList :
                        runningMowerList .append ([mower [0 ],mower [1 ],mower [2 ]])
                        lawnMowerList .remove ([mower [0 ],mower [1 ],mower [2 ]])
                        lawnMowerSound .play ()
def moveLawnMover (zombiesList ,runningMowerList ,length ):
    for movingMower in runningMowerList :
        movingMower [0 ]+=5
        screen .blit (lawnMowerPic ,(movingMower [0 ],movingMower [1 ]))
        for zombie in zombiesList :
            if movingMower [2 ]==zombie [6 ]:
                if Rect (movingMower [0 ],movingMower [1 ],90 ,60 ).colliderect (zombie [1 ],zombie [2 ],90 ,100 ):
                    zombiesList .remove ([zombie [0 ],zombie [1 ],zombie [2 ],zombie [3 ],zombie [4 ],zombie [5 ],zombie [6 ],zombie [7 ],zombie [8 ]])
                    zombieDeathSound .play ()
        if movingMower [0 ]>screenWidth :
            runningMowerList .remove ([movingMower [0 ],movingMower [1 ],movingMower [2 ]])
def placePlant (plant ,pic ,sunAmount ,plantsCostList ,plantsNameGrid ,plantsHealthGrid ,plantsHealthList ,plantSpriteGrid ,plantsActionList ,plantsRechargeList ,selectedPlants ,selectingPlant ,x ,y ,width ,length ):
    oneSpot =0
    for row in range (len (plantsNameGrid )):
        for col in range (len (plantsNameGrid [row ])):
            square =Rect ([x +col *width ,y +row *length ,width ,length ])
            if square .x <mx <(square .x +length )and square .y <my <(square .y +length )and oneSpot !=1 :
                square =Rect ([x +col *width ,y +row *length ,width ,length ])
                oneSpot =1
                if plant !=""and plantsNameGrid [row ][col ]=="":
                    pic =pic .copy ()
                    pic =pic .convert ()
                    pic .set_colorkey ((0 ,0 ,0 ))
                    pic .set_alpha (128 )
                    screen .blit (pic ,(square .x ,square .y ))
                    if mb [0 ]==1 :
                        plantSound .play ()
                        plantsNameGrid [row ][col ]=plant
                        plantsSpriteGrid [row ][col ]=0
                        healthIndex =inList (plant ,plantsHealthList )
                        plantsHealthGrid [row ][col ]=plantsHealthList [healthIndex ][1 ]
                        selectingPlant =False
                        sunAmount -=plantsCostList [sunIndex ][1 ]
                        plantsRechargeList .append ([plant ,time .get_ticks ()])
                        if plant !="nut"or plant !="bomb":
                            plantsActionList .append ([plant ,row ,col ,time .get_ticks ()])
            else :
                square =Rect ([x +col *width ,y +row *length ,width ,length ])
                oneSpot =0
    if mb [2 ]==1 :
        selectingPlant =False
    return [selectingPlant ,plantsRechargeList ,plantsActionList ,sunAmount ]
def plantAnimation (plantsNameGrid ,plantsSpriteGrid ,plantsHealthGrid ,mineCheckList ,plantsActionList ,zombiesList ,width ,length ):
    for row in range (len (plantsNameGrid )):
        for col in range (len (plantsNameGrid [row ])):
            if plantsNameGrid [row ][col ]!=""and plantsSpriteGrid [row ][col ]!="":
                if plantsNameGrid [row ][col ]=="nut":
                    if plantsHealthGrid [row ][col ]>2700 :
                        indexValue =1
                    elif plantsHealthGrid [row ][col ]>1800 :
                        indexValue =2
                    else :
                        indexValue =3
                    listName ="%sСписок"%(plantsNameGrid [row ][col ])
                    x =50 +col *width
                    y =100 +row *length
                    if (int (plantsSpriteGrid [row ][col ])+1 )==len ((eval (listName ))[indexValue ]):
                        plantsSpriteGrid [row ][col ]=0
                        pic =(eval (listName ))[indexValue ][int (plantsSpriteGrid [row ][col ])]
                        screen .blit (pic ,(x ,y ))
                    else :
                        plantsSpriteGrid [row ][col ]+=0.1
                        pic =(eval (listName ))[indexValue ][int (plantsSpriteGrid [row ][col ])]
                        screen .blit (pic ,(x ,y ))
                elif plantsNameGrid [row ][col ]=="mine":
                    explode =False
                    for mine in mineCheckList :
                        if (mine [0 ],mine [1 ])==(row ,col ):
                            explode =True
                            mineAction =mine [2 ]
                    if explode ==True :
                        listName ="%sСписок"%(plantsNameGrid [row ][col ])
                        x =50 +col *width
                        y =100 +row *length
                        if (int (plantsSpriteGrid [row ][col ])+1 )>7 and mineAction =="waiting":
                            plantsSpriteGrid [row ][col ]=0
                            pic =eval (listName )[int (plantsSpriteGrid [row ][col ])]
                            screen .blit (pic ,(x ,y ))
                        elif (int (plantsSpriteGrid [row ][col ])+1 )==15 and mineAction =="exploding":
                            removePlant (plantsNameGrid ,plantsSpriteGrid ,plantsHealthGrid ,plantsActionList ,mineCheckList ,row ,col )
                        else :
                            plantsSpriteGrid [row ][col ]+=0.2
                            pic =eval (listName )[int (plantsSpriteGrid [row ][col ])]
                            screen .blit (pic ,(x ,y ))
                        for zombie in zombiesList :
                            if row ==zombie [6 ]:
                                square =[x ,y ,width ,length ]
                                if 0 <sqrt ((square [0 ]-zombie [1 ])**2 +(square [1 ]-zombie [2 ])**2 )<width //2 :
                                    zombiesList .remove ([zombie [0 ],zombie [1 ],zombie [2 ],zombie [3 ],zombie [4 ],zombie [5 ],zombie [6 ],zombie [7 ],zombie [8 ]])
                                    for mine in mineCheckList :
                                        if (mine [0 ],mine [1 ])==(row ,col ):
                                            mine [2 ]="exploding"
                                            plantsSpriteGrid [row ][col ]=8
                                            mineSound .play ()
                                    break
                    elif explode ==False :
                        listName ="%sСписок"%(plantsNameGrid [row ][col ])
                        x =50 +col *width
                        y =100 +row *length
                        screen .blit (eval (listName )[0 ],(x ,y ))
                elif plantsNameGrid [row ][col ]=="bomb":
                    x =50 +col *width
                    y =100 +row *length
                    if int (plantsSpriteGrid [row ][col ])>5 :
                        plantsSpriteGrid [row ][col ]+=0.2
                        pic =bombList [int (plantsSpriteGrid [row ][col ])]
                        screen .blit (pic ,(x -width ,y -length ))
                        for zombie in zombiesList :
                            if Rect (zombie [1 ],zombie [2 ],90 ,100 ).colliderect ([x -width ,y -length ,pic .get_width (),pic .get_height ()]):
                                zombiesList .remove ([zombie [0 ],zombie [1 ],zombie [2 ],zombie [3 ],zombie [4 ],zombie [5 ],zombie [6 ],zombie [7 ],zombie [8 ]])
                        if (int (plantsSpriteGrid [row ][col ])+1 )==len (bombList ):
                            removePlant (plantsNameGrid ,plantsSpriteGrid ,plantsHealthGrid ,plantsActionList ,mineCheckList ,row ,col )
                    else :
                        if plantsSpriteGrid [row ][col ]<5.5 :
                            plantsSpriteGrid [row ][col ]+=0.2
                            pic =bombList [int (plantsSpriteGrid [row ][col ])]
                            screen .blit (pic ,(x ,y ))
                        else :
                            plantsSpriteGrid [row ][col ]=6
                            bombSound .play ()
                else :
                    listName ="%sСписок"%(plantsNameGrid [row ][col ])
                    x =50 +col *width
                    y =100 +row *length
                    if (int (plantsSpriteGrid [row ][col ])+1 )==len (eval (listName )):
                        plantsSpriteGrid [row ][col ]=0
                        pic =eval (listName )[int (plantsSpriteGrid [row ][col ])]
                        screen .blit (pic ,(x ,y ))
                    else :
                        plantsSpriteGrid [row ][col ]+=0.1
                        pic =eval (listName )[int (plantsSpriteGrid [row ][col ])]
                        screen .blit (pic ,(x ,y ))
def removePlant (plantsNameGrid ,plantsSpriteGrid ,plantsHealthGrid ,plantsActionList ,mineCheckList ,row ,col ):
    if plantsNameGrid [row ][col ]=="mine":
        if len (mineCheckList )>0 :
            for mine in mineCheckList :
                if (row ,col )==(mine [0 ],mine [1 ]):
                    if mine [2 ]=="exploding":
                        mineCheckList .remove ([row ,col ,"exploding"])
                    else :
                        mineCheckList .remove ([row ,col ])
    plantsNameGrid [row ][col ]=""
    plantsSpriteGrid [row ][col ]=""
    plantsHealthGrid [row ][col ]=""
    for action in plantsActionList :
        if action [1 ]==row and action [2 ]==col :
            plantsActionList .remove ([action [0 ],action [1 ],action [2 ],action [3 ]])
def plantRecharge (plantsRechargeList ,plantsRechargeTimesList ,selectedPlants ):
    for rechargeList in plantsRechargeList :
        if rechargeList [0 ]in selectedPlants :
            timeIndex =inList (rechargeList [0 ],plantsRechargeTimesList )
            if time .get_ticks ()-rechargeList [1 ]>=plantsRechargeTimesList [timeIndex ][1 ]:
                ind =plantsRechargeList .index (rechargeList )
                del plantsRechargeList [ind ]
    return plantsRechargeList
def plantAction (plantsNameGrid ,sunEnergyList ,mineCheckList ,plantsActionList ,plantsActionTimesList ,bulletsList ,width ,length ):
    for action in plantsActionList :
        timeIndex =inList (action [0 ],plantsActionTimesList )
        if action [0 ]==plantsActionTimesList [timeIndex ][0 ]:
            if time .get_ticks ()-action [3 ]>=plantsActionTimesList [timeIndex ][1 ]:
                action [3 ]=time .get_ticks ()
                if action [0 ]=="pea":
                    bulletsList .append (["pea",50 +width *action [2 ],100 +length *action [1 ]+10 ,action [1 ]])
                elif action [0 ]=="snowpea":
                    bulletsList .append (["snowpea",50 +width *action [2 ],100 +length *action [1 ]+10 ,action [1 ]])
                elif action [0 ]=="sun":
                    addSun (plantsNameGrid ,width ,length ,sunEnergyList ,"plant",action [1 ],action [2 ])
                elif action [0 ]=="mine":
                    mineCheckList .append ([action [1 ],action [2 ],"waiting"])
    return [plantsActionList ,bulletsList ]
def checkBullets (bulletsList ,zombiesList ):
    for bullet in bulletsList :
        bullet [1 ]=bullet [1 ]+10
        if bullet [1 ]>=screenWidth :
            ind =bulletsList .index (bullet )
            del bulletsList [ind ]
        screen .blit (eval (bullet [0 ]+"Bullet"),(bullet [1 ],bullet [2 ]+40 ))
        for zombie in zombiesList :
            if int (bullet [3 ])==int (zombie [6 ]):
                if Rect (bullet [1 ],bullet [2 ],20 ,20 ).colliderect (Rect (zombie [1 ],zombie [2 ],90 ,100 )):
                    if zombie [0 ]=="bucket":
                        hitSound2 .play ()
                    else :
                        hitSound1 .play ()
                    zombie [4 ]-=1
                    if bullet [0 ]=="snowpea":
                        zombie [8 ]="freeze"
                    if [bullet [0 ],bullet [1 ],bullet [2 ],bullet [3 ]]in bulletsList :
                        bulletsList .remove ([bullet [0 ],bullet [1 ],bullet [2 ],bullet [3 ]])
                    if zombie [4 ]<=0 :
                        zombiesList .remove ([zombie [0 ],zombie [1 ],zombie [2 ],zombie [3 ],zombie [4 ],zombie [5 ],zombie [6 ],zombie [7 ],zombie [8 ]])
                        zombieDeathSound .play ()
    return [bulletsList ,zombiesList ]
def addSun (plantsNameGrid ,width ,length ,sunEnergyList ,source ,row ,col ):
    if source =="sky":
        row =randint (0 ,len (plantsNameGrid )-1 )
        col =randint (0 ,len (plantsNameGrid )-1 )
        x =50 +col *width
        y =100
        sunEnergyList .append ([0 ,x ,y ,"falling",row ,col ])
    elif source =="plant":
        row =row
        col =col
        x =50 +col *width
        y =100 +row *length
        sunEnergyList .append ([0 ,x ,y ,"idle",row ,col ])
def sunAnimation (sunEnergyList ,sunSpriteList ,length ):
    for sunEnergy in sunEnergyList :
        if sunEnergy [3 ]=="falling":
            if sunEnergy [2 ]<(100 +sunEnergy [4 ]*length ):
                sunEnergy [2 ]+=1
        if (int (sunEnergy [0 ])+1 )>=len (sunSpriteList ):
            sunEnergy [0 ]=0
            screen .blit (sunSpriteList [int (sunEnergy [0 ])],(sunEnergy [1 ],sunEnergy [2 ]))
        else :
            sunEnergy [0 ]+=0.05
            screen .blit (sunSpriteList [int (sunEnergy [0 ])],(sunEnergy [1 ],sunEnergy [2 ]))
def checkSun (sunEnergyList ,returningSunList ):
    for sunEnergy in sunEnergyList :
        if Rect (sunEnergy [1 ],sunEnergy [2 ],(sunSpriteList [int (sunEnergy [0 ])].get_width ()),(sunSpriteList [int (sunEnergy [0 ])].get_height ())).collidepoint (mx ,my ):
            if mb [0 ]==1 :
                ind =sunEnergyList .index (sunEnergy )
                returningSunList .append (sunEnergyList [ind ])
                del sunEnergyList [ind ]
def returnSun (sunAmount ,returningSunList ,sunSpriteList ):
    for sunEnergy in returningSunList :
        if sqrt ((sunEnergy [1 ]-120 )**2 +(sunEnergy [2 ]-15 )**2 )<100 :
            sunAmount +=25
            pointsSound .play ()
            ind =returningSunList .index (sunEnergy )
            del returningSunList [ind ]
        else :
            angle =radians (tan ((sunEnergy [1 ]-120 )/(sunEnergy [2 ]-15 )))
            angle =atan2 ((sunEnergy [2 ]-0 ),(sunEnergy [1 ]-120 ))
            sunEnergy [1 ]-=100 *cos (angle )
            sunEnergy [2 ]-=100 *sin (angle )
            screen .blit (sunSpriteList [0 ],(sunEnergy [1 ],sunEnergy [2 ]))
    return sunAmount
def addZombies (zombiesList ,waveCount ,screenWidth ,y ,width ,length ):
    zombieNum =randint (1 ,waveCount )
    soundNum =randint (1 ,5 )
    soundName =eval ("zombieSound"+str (soundNum ))
    soundName .play ()
    for i in range (zombieNum ):
        zombieType =randint (1 ,6 )
        zombieX =screenWidth
        randRow =randint (0 ,4 )
        zombieY =y +(randRow *length )
        if zombieType ==1 :
            speed =width /(40 *4.7 )
            health =10
            spriteIndex =0
            zombiesList .append (["normal",zombieX ,zombieY ,speed ,health ,spriteIndex ,randRow ,"walking","normal"])
        elif zombieType ==2 :
            speed =width /(40 *4.7 )
            health =20
            spriteIndex =0
            zombiesList .append (["cone",zombieX ,zombieY ,speed ,health ,spriteIndex ,randRow ,"walking","normal"])
        elif zombieType ==3 :
            speed =width /(40 *4.7 )
            health =30
            spriteIndex =0
            zombiesList .append (["bucket",zombieX ,zombieY ,speed ,health ,spriteIndex ,randRow ,"walking","normal"])
        elif zombieType ==4 :
            speed =2 *(width /(40 *4.7 ))
            health =5
            spriteIndex =0
            zombiesList .append (["football",zombieX ,zombieY ,speed ,health ,spriteIndex ,randRow ,"walking","normal"])
        elif zombieType ==5 :
            speed =0.5 *(width /(40 *4.7 ))
            health =40
            spriteIndex =0
            zombiesList .append (["trash",zombieX ,zombieY ,speed ,health ,spriteIndex ,randRow ,"walking","normal"])
        elif zombieType ==6 :
            speed =0.5 *(width /(40 *4.7 ))
            health =30
            spriteIndex =0
            zombiesList .append (["door",zombieX ,zombieY ,speed ,health ,spriteIndex ,randRow ,"walking","normal"])
def zombieAnimation (currentScreen ,zombiesList ,normalZombieList ,normalZombieEat ,zombieObjectList ,plantsNameGrid ,plantsSpriteGrid ,plantsHealthGrid ,plantsActionList ,mineCheckList ,x ,y ,width ,length ):
    for zombie in zombiesList :
        for row in range (len (plantsNameGrid )):
            for col in range (len (plantsNameGrid [row ])):
                square =[x +col *width ,y +row *length ,width ,length ]
                if plantsNameGrid [row ][col ]!=""and 0 <sqrt ((square [0 ]-zombie [1 ])**2 +(square [1 ]-zombie [2 ])**2 )<width //2 :
                    zombie [7 ]=[row ,col ]
    for zombie in zombiesList :
        if zombie [1 ]<0 :
            loseZombie =zombie
            del zombiesList [:]
            loseZombie [1 ]=50
            zombiesList .append (loseZombie )
            currentScreen ="lose"
        if zombie [7 ]=="walking":
            freezePic =""
            if currentScreen !="lose":
                if zombie [8 ]=="normal":
                    zombie [1 ]-=zombie [3 ]
                elif zombie [8 ]=="freeze":
                    zombie [1 ]-=zombie [3 ]/2
                    freezePic =image .load ("freezeAlpha.png").convert_alpha ()
            elif currentScreen =="lose":
                if zombie [8 ]=="normal":
                    if sqrt ((0 -zombie [1 ])**2 +(400 -zombie [2 ])**2 )>5 :
                        if zombie [2 ]>400 :
                            zombie [2 ]-=1
                        else :
                            zombie [2 ]+=1
                elif zombie [8 ]=="freeze":
                    if 0 <sqrt ((400 -zombie [1 ])**2 +(0 -zombie [2 ])**2 )<5 :
                        if zombie [2 ]>400 :
                            zombie [2 ]-=1
                        else :
                            zombie [2 ]+=1
                    freezePic =image .load ("freezeAlpha.png").convert_alpha ()
            if (int (zombie [5 ])+1 )==len (normalZombieList ):
                zombie [5 ]=0
                pic =normalZombieList [int (zombie [5 ])]
            else :
                zombie [5 ]+=0.2
                pic =normalZombieList [int (zombie [5 ])]
            if freezePic !="":
                freezeSurface =Surface ((90 ,100 ),SRCALPHA ).convert ()
                freezeSurface .blit (pic ,(0 ,0 ))
                blit_alpha (freezeSurface ,freezePic ,(0 ,0 ),125 )
                freezeCol =freezeSurface .get_at ((0 ,0 ))
                freezeSurface .set_colorkey (freezeCol )
                screen .blit (freezeSurface ,(zombie [1 ],zombie [2 ]))
            else :
                screen .blit (pic ,(zombie [1 ],zombie [2 ]))
        else :
            if (int (zombie [5 ])+1 )==len (normalZombieEat ):
                zombie [5 ]=0
                pic =normalZombieEat [int (zombie [5 ])]
                if plantsHealthGrid [zombie [7 ][0 ]][zombie [7 ][1 ]]!=""and plantsHealthGrid [zombie [7 ][0 ]][zombie [7 ][1 ]]>0 :
                    plantsHealthGrid [zombie [7 ][0 ]][zombie [7 ][1 ]]-=1
                    if eatChannel .get_busy ()==0 :
                        eatChannel .play (zombieEatSound )
                elif plantsHealthGrid [zombie [7 ][0 ]][zombie [7 ][1 ]]!="":
                    removePlant (plantsNameGrid ,plantsSpriteGrid ,plantsHealthGrid ,plantsActionList ,mineCheckList ,zombie [7 ][0 ],zombie [7 ][1 ])
                    gulpSound .play ()
                    zombie [7 ]="walking"
                if len (zombie [7 ])==2 and plantsHealthGrid [zombie [7 ][0 ]][zombie [7 ][1 ]]=="":
                    zombie [7 ]="walking"
                screen .blit (pic ,(zombie [1 ],zombie [2 ]))
            else :
                zombie [5 ]+=0.2
                if (int (zombie [5 ])+1 )>=len (normalZombieEat ):
                    zombie [5 ]=0
                    pic =normalZombieEat [int (zombie [5 ])]
                else :
                    pic =normalZombieEat [int (zombie [5 ])]
                if plantsHealthGrid [zombie [7 ][0 ]][zombie [7 ][1 ]]!=""and plantsHealthGrid [zombie [7 ][0 ]][zombie [7 ][1 ]]>0 :
                    plantsHealthGrid [zombie [7 ][0 ]][zombie [7 ][1 ]]-=1
                    if eatChannel .get_busy ()==0 :
                        eatChannel .play (zombieEatSound )
                elif plantsHealthGrid [zombie [7 ][0 ]][zombie [7 ][1 ]]!="":
                    removePlant (plantsNameGrid ,plantsSpriteGrid ,plantsHealthGrid ,plantsActionList ,mineCheckList ,zombie [7 ][0 ],zombie [7 ][1 ])
                    gulpSound .play ()
                    zombie [7 ]="walking"
                if len (zombie [7 ])==2 and plantsHealthGrid [zombie [7 ][0 ]][zombie [7 ][1 ]]=="":
                    zombie [7 ]="walking"
                if zombie [8 ]=="freeze":
                    freezePic =image .load ("freezeAlpha.png").convert_alpha ()
                    freezeSurface =Surface ((90 ,100 ),SRCALPHA ).convert ()
                    freezeSurface .blit (pic ,(0 ,0 ))
                    blit_alpha (freezeSurface ,freezePic ,(0 ,0 ),125 )
                    freezeCol =freezeSurface .get_at ((0 ,0 ))
                    freezeSurface .set_colorkey (freezeCol )
                    screen .blit (freezeSurface ,(zombie [1 ],zombie [2 ]))
                else :
                    screen .blit (pic ,(zombie [1 ],zombie [2 ]))
        objectIndex =inList (zombie [0 ],zombieObjectList )
        if zombie [0 ]=="cone":
            screen .blit (zombieObjectList [objectIndex ][1 ],(zombie [1 ]+25 ,zombie [2 ]-30 ))
        elif zombie [0 ]=="bucket":
            screen .blit (zombieObjectList [objectIndex ][1 ],(zombie [1 ]+12 ,zombie [2 ]-27 ))
        elif zombie [0 ]=="football":
            screen .blit (zombieObjectList [objectIndex ][1 ],(zombie [1 ]+12 ,zombie [2 ]-27 ))
        elif zombie [0 ]=="trash":
            screen .blit (zombieObjectList [objectIndex ][1 ],(zombie [1 ]-30 ,zombie [2 ]+25 ))
        elif zombie [0 ]=="door":
            screen .blit (zombieObjectList [objectIndex ][1 ],(zombie [1 ]-10 ,zombie [2 ]))
    return [zombiesList ,currentScreen ]
init ()
font .init ()
size =(screenWidth ,screenHeight )=(1200 ,800 )
screen =display .set_mode (size )
display .set_caption ("Растения против зомби - Филипп Фам")
mx ,my =mouse .get_pos ()
menuBackground =image .load ("menu/menu.jpg")
logoPic =image .load ("menu/logo.png")
helpBackground =image .load ("menu/help.png")
startButton =image .load ("menu/startbutton.png")
instructionsBackground =image .load ("menu/instructions.png")
nextButton1 =image .load ("menu/nextbutton1.png")
nextButton2 =image .load ("menu/nextbutton2.png")
backButton =image .load ("menu/backbutton.png")
backButton .set_colorkey ((255 ,255 ,255 ))
playRect =Rect (600 ,90 ,500 ,175 )
helpRect =Rect (950 ,640 ,100 ,100 )
quitRect =Rect (1065 ,640 ,100 ,100 )
helpMenuRect =Rect (480 ,695 ,235 ,55 )
nextRect =Rect (1050 ,340 ,148 ,148 )
backRect =Rect (1000 ,620 ,127 ,125 )
mixer .init ()
mixer .set_num_channels (10 )
hitSound1 =mixer .Sound ("sounds/splat2.wav")
hitSound2 =mixer .Sound ("sounds/shieldhit.wav")
mineSound =mixer .Sound ("sounds/potato_mine.wav")
bombSound =mixer .Sound ("sounds/cherrybomb.wav")
lawnMowerSound =mixer .Sound ("sounds/lawnmower.wav")
pointsSound =mixer .Sound ("sounds/points.wav")
plantSound =mixer .Sound ("sounds/plant.wav")
packetSound =mixer .Sound ("sounds/seedlift.wav")
shovelPlantSound =mixer .Sound ("sounds/plant2.wav")
shovelSound =mixer .Sound ("sounds/Shovel.ogx")
zombieSound1 =mixer .Sound ("sounds/awooga.wav")
zombieSound2 =mixer .Sound ("sounds/groan5.wav")
zombieSound3 =mixer .Sound ("sounds/hugewave.wav")
zombieSound4 =mixer .Sound ("sounds/siren.wav")
zombieSound5 =mixer .Sound ("sounds/sukhbir6.wav")
zombieDeathSound =mixer .Sound ("sounds/groan2.wav")
screamSound =mixer .Sound ("sounds/scream.wav")
gulpSound =mixer .Sound ("sounds/gulp.wav")
loseSound =mixer .Sound ("sounds/losemusic.wav")
zombieEatSound =mixer .Sound ("sounds/ZombieBite.ogx")
zombieEatSound .set_volume (1.0 )
eatChannel =mixer .Channel (5 )
back1 =image .load ("backgrounds/stage1.jpg").convert_alpha ()
backSubsurface =back1 .subsurface ([290 ,0 ,1200 ,800 ])
back =backSubsurface
loseX =0
loseBack =image .load ("menu/loseBack.jpg").convert_alpha ()
selectBar =image .load ("backgrounds/bar.png").convert_alpha ()
peaList =addSprites ("sprites","plants","pea","pea",1 ,8 )
sunList =addSprites ("sprites","plants","sun","sun",1 ,8 )
snowpeaList =addSprites ("sprites","plants","snowpea","snowpea",1 ,8 )
mineList =addSprites ("sprites","plants","mine","mine",1 ,16 )
nutList =[image .load ("sprites/plants/nut/nut1-1.png"),addSprites ("sprites","plants","nut","nut",1 ,4 ),addSprites ("sprites","plants","nut","nut",2 ,4 ),addSprites ("sprites","plants","nut","nut",3 ,4 )]
bombList =addSprites ("sprites","plants","bomb","bomb",1 ,14 )
peaPacket =image .load ("sprites/plants/pea/PeashooterSeedPacket.png").convert_alpha ()
sunPacket =image .load ("sprites/plants/sun/SunflowerSeedPacket.png").convert_alpha ()
nutPacket =image .load ("sprites/plants/nut/WallnutSeedPacket.png").convert_alpha ()
snowpeaPacket =image .load ("sprites/plants/snowpea/SnowpeaSeedPacket.png").convert_alpha ()
bombPacket =image .load ("sprites/plants/bomb/CherrybombSeedPacket.png").convert_alpha ()
minePacket =image .load ("sprites/plants/mine/PotatomineSeedPacket.png").convert_alpha ()
peaBullet =image .load ("sprites/plants/pea/b1.png").convert_alpha ()
snowpeaBullet =image .load ("sprites/plants/snowpea/snowb1.png").convert_alpha ()
bulletsList =[]
selectedPlants =["pea","sun","nut","snowpea","bomb","mine"]
selectingPlant =False
shovelCursor =image .load ("sprites/extra/ShovelCursor.png").convert_alpha ()
shovelPic =image .load ("sprites/extra/Shovel.jpg").convert_alpha ()
shovelRect =Rect (660 ,0 ,100 ,100 )
shovellingPlant =False
plant =""
plantsRechargeList =[]
plantsRechargeTimesList =[]
plantsRechargeTimesList .append (["pea",7500 ])
plantsRechargeTimesList .append (["sun",7500 ])
plantsRechargeTimesList .append (["nut",30000 ])
plantsRechargeTimesList .append (["snowpea",7500 ])
plantsRechargeTimesList .append (["bomb",50000 ])
plantsRechargeTimesList .append (["mine",30000 ])
plantsActionList =[]
plantsActionTimesList =[]
plantsActionTimesList .append (["pea",1430 ])
plantsActionTimesList .append (["sun",24000 ])
plantsActionTimesList .append (["snowpea",1430 ])
plantsActionTimesList .append (["mine",15000 ])
plantsCostList =[]
plantsCostList .append (["pea",100 ])
plantsCostList .append (["sun",50 ])
plantsCostList .append (["nut",50 ])
plantsCostList .append (["snowpea",175 ])
plantsCostList .append (["bomb",150 ])
plantsCostList .append (["mine",25 ])
plantsHealthList =[]
plantsHealthList .append (["pea",300 ])
plantsHealthList .append (["sun",300 ])
plantsHealthList .append (["nut",3600 ])
plantsHealthList .append (["snowpea",300 ])
plantsHealthList .append (["bomb",9999 ])
plantsHealthList .append (["mine",300 ])
mineCheckList =[]
plantsNameGrid =createGrid (9 ,5 )
plantsSpriteGrid =createGrid (9 ,5 )
plantsHealthGrid =createGrid (9 ,5 )
width =120
length =130
x =50
y =100
zombiesList =[]
normalZombieList =addSprites ("sprites","zombies","normal","normal",1 ,8 )
normalZombieEat =addSprites ("sprites","zombies","normaleat","normaleat",1 ,7 )
conePic =image .load ("sprites/zombies/cone/cone.png")
bucketPic =image .load ("sprites/zombies/bucket/bucket.png")
footballPic =image .load ("sprites/zombies/football/football.png")
trashPic =image .load ("sprites/zombies/trash/trash.png")
doorPic =image .load ("sprites/zombies/door/door.png")
zombieObjectList =[["cone",conePic ],["bucket",bucketPic ],["football",footballPic ],["trash",trashPic ],["door",doorPic ]]
lawnMowerPic =image .load ("sprites/lawnmower.png")
lawnMowerList =[]
for i in range (5 ):
    lawnMowerList .append ([5 ,110 +i *140 ,i ])
runningMowerList =[]
sunSpriteList =addSprites ("sprites","extra","sunenergy","sunenergy",1 ,4 )
sunEnergyList =[]
returningSunList =[]
sunAmount =50
sunAmountFont =font .SysFont ("SeriesOrbit",20 )
waveCount =0
fpsClock =time .Clock ()
SUNEVENT =USEREVENT +0
ZOMBIEEVENT =USEREVENT +1
currentScreen ="menu"
mixer .music .load ("sounds/maintheme.mp3")
mixer .music .play (-1 ,0.0 )
while currentScreen !="exit":
    if currentScreen =="menu":
        running =True
        while running :
            for evt in event .get ():
                if evt .type ==QUIT :
                    running =False
                    currentScreen ="exit"
            mx ,my =mouse .get_pos ()
            mb =mouse .get_pressed ()
            screen .blit (menuBackground ,(0 ,0 ))
            screen .blit (logoPic ,(0 ,50 ))
            displayNameAmount =sunAmountFont .render ("Автор: Филип Фам",True ,(0 ,0 ,0 ))
            screen .blit (displayNameAmount ,(200 ,400 ))
            if playRect .collidepoint (mx ,my ):
                screen .blit (startButton ,(playRect [0 ],playRect [1 ]))
                if mb [0 ]==1 :
                    running =False
                    currentScreen ="game"
                    mixer .music .load ("sounds/day.mp3")
                    mixer .music .play (-1 ,0.0 )
                    sunTimer =time .set_timer (SUNEVENT ,5000 )
                    zombieSpawnTimer =time .set_timer (ZOMBIEEVENT ,20000 )
            if helpRect .collidepoint (mx ,my )and mb [0 ]==1 :
                running =False
                currentScreen ="help"
            if quitRect .collidepoint (mx ,my )and mb [0 ]==1 :
                running =False
                currentScreen ="exit"
            display .flip ()
    if currentScreen =="help":
        running =True
        while running :
            for evt in event .get ():
                if evt .type ==QUIT :
                    running =False
                    currentScreen ="exit"
            mx ,my =mouse .get_pos ()
            mb =mouse .get_pressed ()
            screen .blit (helpBackground ,(0 ,0 ))
            screen .blit (nextButton1 ,(nextRect [0 ],nextRect [1 ]))
            if helpMenuRect .collidepoint (mx ,my )and mb [0 ]==1 :
                running =False
                currentScreen ="menu"
            if nextRect .collidepoint (mx ,my ):
                screen .blit (nextButton2 ,(nextRect [0 ],nextRect [1 ]))
                if mb [0 ]==1 :
                    running =False
                    currentScreen ="instructions"
            display .flip ()
        if currentScreen =="instructions":
            running =True
            while running :
                for evt in event .get ():
                    if evt .type ==QUIT :
                        running =False
                        currentScreen ="exit"
                mx ,my =mouse .get_pos ()
                mb =mouse .get_pressed ()
                screen .blit (instructionsBackground ,(0 ,0 ))
                screen .blit (backButton ,(backRect [0 ],backRect [1 ]))
                if backRect .collidepoint (mx ,my )and mb [0 ]==1 :
                    running =False
                    currentScreen ="help"
                display .flip ()
    if currentScreen =="lost":
        running =True
        while running :
            for evt in event .get ():
                if evt .type ==QUIT :
                    running =False
                    currentScreen ="exit"
            screen .fill ((0 ,0 ,0 ))
            screen .blit (loseBack ,(0 ,0 ))
            displayLostAmount =sunAmountFont .render ("Волны выжили: "+str (waveCount ),True ,(255 ,255 ,255 ))
            screen .blit (displayLostAmount ,(500 ,700 ))
            display .flip ()
    if currentScreen =="game"or currentScreen =="lose":
        running =True
        while running :
            for evt in event .get ():
                if evt .type ==QUIT :
                    running =False
                    currentScreen ="exit"
                if evt .type ==SUNEVENT :
                    addSun (plantsNameGrid ,width ,length ,sunEnergyList ,"sky",0 ,0 )
                if evt .type ==ZOMBIEEVENT :
                    waveCount +=1
                    addZombies (zombiesList ,waveCount ,screenWidth ,y ,width ,length )
                if evt .type ==MOUSEBUTTONDOWN :
                    if evt .button ==1 and selectingPlant ==False and shovellingPlant ==False and shovelRect .collidepoint (mx ,my ):
                        shovellingPlant =True
                        shovelSound .play ()
                    if evt .button ==1 and selectingPlant ==False and plant ==""and shovellingPlant ==False :
                        for ind in range (len (selectedPlants )):
                            if Rect (200 +75 *ind ,10 ,65 ,90 ).collidepoint (mx ,my ):
                                selectingPlant =True
                                plant =selectedPlants [ind ]
                                nameIndex =inList (plant ,plantsRechargeList )
                                sunIndex =inList (plant ,plantsCostList )
                                if (sunAmount -plantsCostList [sunIndex ][1 ])<0 :
                                    plant =""
                                    selectingPlant =False
                                elif nameIndex !=-1 :
                                    plant =""
                                    selectingPlant =False
                                else :
                                    packetSound .play ()
            mx ,my =mouse .get_pos ()
            mb =mouse .get_pressed ()
            checkSun (sunEnergyList ,returningSunList )
            returnList =drawScene (zombiesList ,plantsActionList ,bulletsList ,plantsRechargeList ,shovellingPlant ,selectingPlant ,sunAmount ,plant ,currentScreen ,loseX )
            zombiesList =returnList [0 ]
            plantsActionList =returnList [1 ]
            bulletsList =returnList [2 ]
            plantsRechargeList =returnList [3 ]
            shovellingPlant =returnList [4 ]
            selectingPlant =returnList [5 ]
            sunAmount =returnList [6 ]
            plant =returnList [7 ]
            currentScreen =returnList [8 ]
            loseX =returnList [9 ]
            if currentScreen =="lost":
                break
            sunAmount =returnSun (sunAmount ,returningSunList ,sunSpriteList )
            display .flip ()
            fpsClock .tick (30 )
quit ()