import {render, cleanup, fireEvent} from '@testing-library/react-native';
import React from 'react';
import SleepGoalsScreen from "../app/Screens/SleepGoalsScreen"

describe('Sleep goals input form', () => {
  let wrapper;
  beforeEach(() => {
      wrapper = render(<SleepGoalsScreen />);
    });
  afterEach(() => {
      cleanup();
      wrapper = null;
    });
  it('renders correctly', () => {
      expect(wrapper).toMatchSnapshot();
  });

  it("Shows error message if target sleep is less than 24 hours per night", () => {
    const {getByText, queryByTestId, getByPlaceholderText} = wrapper;

    const goalTextInput = getByPlaceholderText("7 hours"); 
    const enteredGoal = "25";
    fireEvent(goalTextInput, 'onChangeText', enteredGoal);
    
    const saveButton = getByText("Save");
    fireEvent.press(saveButton);
  
    const validationError = queryByTestId("error-message");
    expect(validationError).toBeTruthy();
    
    expect(validationError.props.children)
        .toBe("Your goal must be less than 24 hours per night.");
  });

  it("Shows error message if target sleep is less than 0 hours per night", () => {
    const {getByText, queryByTestId, getByPlaceholderText} = wrapper;

    const goalTextInput = getByPlaceholderText("7 hours"); 
    const enteredGoal = "-10";
    fireEvent(goalTextInput, 'onChangeText', enteredGoal);
    
    const saveButton = getByText("Save");
    fireEvent.press(saveButton);
  
    const validationError = queryByTestId("error-message");
    expect(validationError).toBeTruthy();
    
    expect(validationError.props.children)
        .toBe("Your goal must be greater than 0 hours per night.");
  });

  it("Shows error message if the input is not a number.", () => {
    const {getByText, queryByTestId, getByPlaceholderText} = wrapper;

    const goalTextInput = getByPlaceholderText("7 hours"); 
    const enteredGoal = "6,";
    fireEvent(goalTextInput, 'onChangeText', enteredGoal);
    
    const saveButton = getByText("Save");
    fireEvent.press(saveButton);
  
    const validationError = queryByTestId("error-message");
    expect(validationError).toBeTruthy();
    
    expect(validationError.props.children)
        .toBe("Your goal must be a number.");
  });
});

