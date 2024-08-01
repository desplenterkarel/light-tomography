from motor import Motor


def main():
    pulse_pin = 156
    direction_pin = 154
    steps = 200
    pulse_duration = 0.002
    hold_duration = 0.5

    motor = Motor(pulse_pin, direction_pin, steps)

    try:
        while True:
            motor.turn_motor(pulse_duration)
            motor.hold_motor(hold_duration)
    except KeyboardInterrupt:
        motor.turn_off()


if __name__ == "__main__":
    main()
