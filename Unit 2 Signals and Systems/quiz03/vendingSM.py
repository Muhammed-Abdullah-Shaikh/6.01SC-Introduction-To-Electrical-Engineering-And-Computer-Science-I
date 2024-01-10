import lib601.sm as sm

class State:
    idle = 0
    dispensing = 1

class Vending(sm.SM):
    """
    Vending MachineThe vending machine has an unlimited number of sodas that it sells for 75 cents apiece. 
    * The user can deposit quarters in the machine. 
    * If the user presses the cancel button, all the coins she's put in so far are returned. 
    * If the user presses the dispense button, 
        * If she had not deposited at least 75 cents, she gets no soda and no change. 
        * If she had deposited 75 cents or more, she gets a soda and any amount over 75 cents that she has deposited. 
    """
    startState = 0
    sodaPrice = 75
    quarterValue = 25

    def getNextValues(self, state, inp):
        """
        Calculates the next values based on the current state and input.

        Args:
            state (State): The current state of the machine.
            inp (Input): The input received from the user.

        Returns:
            Tuple[State, io.Action]: A tuple containing the next state and the action to perform.
        """
        
        if inp == 'dispense':
            if state >= self.sodaPrice:
                return (0, (state-self.sodaPrice, True))
            else:
                return (state, (0, False))
        
        if inp == 'quarter':
            return (state+self.quarterValue, (0, False))
        
        if inp == 'cancel':
            return (0, (state, False))


## Testing
result = Vending().transduce(
    ['dispense', 'quarter', 'quarter', 'quarter', 'quarter', 'dispense', 'quarter', 'cancel', 'dispense']
) 
print(result)