import {render, cleanup, fireEvent} from '@testing-library/react-native';
import React from 'react';
import FitnessGoalsScreen from "../app/Screens/FitnessGoalsScreen"

describe('Fitness goals input form', () => {
  let wrapper;
  beforeEach(() => {
      wrapper = render(<FitnessGoalsScreen />);
    });
  afterEach(() => {
      cleanup();
      wrapper = null;
    });
  it('renders correctly', () => {
      expect(wrapper).toMatchSnapshot();
  });

  it("Shows error message if fitness goal is less than or equal to 0", () => {
    const {getByText, queryByTestId, getByPlaceholderText} = wrapper;

    const goalTextInput = getByPlaceholderText("30 minutes"); 
    const enteredGoal = "-20";
    fireEvent(goalTextInput, 'onChangeText', enteredGoal);
    
    const saveButton = getByText("Save");
    fireEvent.press(saveButton);
  
    const validationError = queryByTestId("error-message");
    expect(validationError).toBeTruthy();
    
    expect(validationError.props.children)
        .toBe("Your daily active time goal must be greater than 0 minutes.");
  });

  it("Shows error message if the input is not a number.", () => {
    const {getByText, queryByTestId, getByPlaceholderText} = wrapper;

    const goalTextInput = getByPlaceholderText("30 minutes"); 
    const enteredGoal = "30,";
    fireEvent(goalTextInput, 'onChangeText', enteredGoal);
    
    const saveButton = getByText("Save");
    fireEvent.press(saveButton);
  
    const validationError = queryByTestId("error-message");
    expect(validationError).toBeTruthy();
    
    expect(validationError.props.children)
        .toBe("Your daily active time goal must be a number.");
  });
});

