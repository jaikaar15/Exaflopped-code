Level = 0
isLoaded = False

def Intake_Intaking__If_intake_in_or_intake_out(Intake_Intaking__If_intake_in_or_intake_out__Intaking_):
    global my_event, w, thig, Level, isLoaded
    if Intake_Intaking__If_intake_in_or_intake_out__Intaking_:
        while not not controller.buttonLDown.pressing():
            WindL.spin(REVERSE)
            WindR.spin(REVERSE)
            wait(20, MSEC)
        WindL.stop()
        WindR.stop()
    else:
        while not not controller.buttonLUp.pressing():
            WindL.spin(FORWARD)
            WindR.spin(FORWARD)
            wait(20, MSEC)
        WindL.stop()
        WindR.stop()

def Set_up_loading():
    global my_event, w, thig, Level, isLoaded
    WindL.set_velocity(100, PERCENT)
    WindR.set_velocity(100, PERCENT)
    WindL.set_max_torque(100, PERCENT)
    WindR.set_velocity(100, PERCENT)
    WindL.set_stopping(HOLD)
    WindR.set_stopping(HOLD)
    WindL.spin(FORWARD)
    WindR.spin(REVERSE)

def Load():
    global my_event, w, thig, Level, isLoaded
    WindL.spin(REVERSE)
    WindR.spin(FORWARD)
    wait(1, SECONDS)
    if Level == 3:
        while not math.fabs(WindL.velocity(PERCENT)) <= 0.5:
            wait(20, MSEC)
    else:
        while not math.fabs(WindL.velocity(PERCENT)) <= 20:
            wait(20, MSEC)
    WindL.stop()
    WindR.stop()
    isLoaded = True

def when_started1():
    global my_event, w, thig, Level, isLoaded
    # Make sure the robot stops when not moving sticks
    Left.set_stopping(BRAKE)
    Right.set_stopping(BRAKE)
    while True:
        Left.set_velocity((controller.axisA.position() + controller.axisC.position() / 2), PERCENT)
        Right.set_velocity((controller.axisA.position() - controller.axisC.position() / 2), PERCENT)
        Left.spin(REVERSE)
        Right.spin(REVERSE)
        wait(20, MSEC)

def when_started2():
    global my_event, w, thig, Level, isLoaded
    # Start at L3 mode
    L3L4.pump_on()
    L3L4.retract(CYLINDER2)
    while True:
        if controller.buttonRUp.pressing():
            L3L4.extend(CYLINDER2)
            Level = 4
        if controller.buttonRDown.pressing():
            L3L4.retract(CYLINDER2)
            WindL.spin(REVERSE)
            WindR.spin(FORWARD)
            wait(0.5, SECONDS)
            Left.stop()
            Right.stop()
            Level = 3
        if controller.buttonEUp.pressing():
            # Stops all code if we need to manually reset
            L3L4.pump_off()
            WindL.spin(FORWARD)
            WindR.spin(REVERSE)
            wait(0.5, SECONDS)
            WindL.stop()
            WindR.stop()
            isLoaded = True
            brain.program_stop()
        wait(20, MSEC)

def when_started3():
    global my_event, w, thig, Level, isLoaded
    # Loading code
    Set_up_loading()
    wait(1, SECONDS)
    WindL.stop()
    WindR.stop()
    Load()

def when_started4():
    global my_event, w, thig, Level, isLoaded
    # Intake code
    while True:
        if controller.buttonLDown.pressing() and isLoaded:
            Intake_Intaking__If_intake_in_or_intake_out(True)
        if controller.buttonLUp.pressing() and isLoaded:
            Intake_Intaking__If_intake_in_or_intake_out(False)
        wait(20, MSEC)

def when_started5():
    global my_event, w, thig, Level, isLoaded
    # Shooting section
    while True:
        if controller.buttonFUp.pressing() and brain.timer.time(SECONDS) > 1:
            WindL.spin(FORWARD)
            WindR.spin(REVERSE)
            wait(0.5, SECONDS)
            WindL.stop()
            WindR.stop()
            isLoaded = False
            Load()
            brain.timer.clear()
        wait(20, MSEC)

def when_started6():
    global my_event, w, thig, Level, isLoaded
    # Indicator light depends on the mode the catapult is in
    Level = 3
    Indicator.set_brightness(100)
    Indicator.set_fade(FadeType.FAST)
    while True:
        if Level == 3:
            Indicator.set_color(Color.BLUE)
        else:
            Indicator.set_color(Color.YELLOW)
        wait(20, MSEC)

ws2 = Thread( when_started2 )
ws3 = Thread( when_started3 )
ws4 = Thread( when_started4 )
ws5 = Thread( when_started5 )
ws6 = Thread( when_started6 )
when_started1()
