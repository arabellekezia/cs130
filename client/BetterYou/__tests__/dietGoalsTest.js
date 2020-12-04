import {render, cleanup, fireEvent} from '@testing-library/react-native';
import React from 'react';
import DietGoalsScreen from "../app/Screens/DietGoalsScreen"

describe('Diet goals input form', () => {
  let wrapper;
  beforeEach(() => {
      wrapper = render(<DietGoalsScreen />);
    });
  afterEach(() => {
      cleanup();
      wrapper = null;
    });
  it('renders correctly', () => {
      expect(wrapper).toMatchSnapshot();
  });

  it("No error message is displayed with valid input.", () => {
    const {getByText, queryByTestId, getByPlaceholderText} = wrapper;

    const goalTextInput = getByPlaceholderText("2000 cal"); 
    const enteredGoal = "1800";
    fireEvent(goalTextInput, 'onChangeText', enteredGoal);
    
    const saveButton = getByText("Save");
    fireEvent.press(saveButton);
  
    const validationError = queryByTestId("error-message");
    expect(validationError).toBe(null);
  });

  it("Shows error message if daily calorie budget is less than 1000 calories (not reasonable input)", () => {
    const {getByText, queryByTestId, getByPlaceholderText} = wrapper;

    const goalTextInput = getByPlaceholderText("2000 cal"); 
    const enteredGoal = "800";
    fireEvent(goalTextInput, 'onChangeText', enteredGoal);
    
    const saveButton = getByText("Save");
    fireEvent.press(saveButton);
  
    const validationError = queryByTestId("error-message");
    expect(validationError).toBeTruthy();
    
    expect(validationError.props.children)
        .toBe("Your daily calorie budget must be greater than 1000 calories.");
  });

  it("Shows error message if the input is not a number.", () => {
    const {getByText, queryByTestId, getByPlaceholderText} = wrapper;

    const goalTextInput = getByPlaceholderText("2000 cal"); 
    const enteredGoal = "2000,";
    fireEvent(goalTextInput, 'onChangeText', enteredGoal);
    
    const saveButton = getByText("Save");
    fireEvent.press(saveButton);
  
    const validationError = queryByTestId("error-message");
    expect(validationError).toBeTruthy();
    
    expect(validationError.props.children)
        .toBe("Your daily calorie budget must be a number.");
  });
});

