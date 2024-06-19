from motor import Motor


def main():
    pulse_pin = 156
    direction_pin = 154

    pulse_duration = 0.001
    hold_duration = 1

    motor = Motor(pulse_pin, direction_pin)

    try:
        while True:
            motor.turn_motor(pulse_duration)
            motor.hold_motor(hold_duration)
    except KeyboardInterrupt:
        motor.turn_off()


if __name__ == "__main__":
    main()
