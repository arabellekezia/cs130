import {render, cleanup, fireEvent} from '@testing-library/react-native';
import React from 'react';
import FitnessEntryFormScreen from "../app/Screens/FitnessEntryFormScreen"

describe('Fitness entry input form', () => {
  let wrapper;
  beforeEach(() => {
      wrapper = render(<FitnessEntryFormScreen route={{}} />);
    });
  afterEach(() => {
      cleanup();
      wrapper = null;
    });
  it('renders correctly', () => {
      expect(wrapper).toMatchSnapshot();
  });

  it("Shows error message if no category is selected", () => {
    const {getByText, queryByTestId} = wrapper;
    
    const submitButton = getByText("Submit");
    fireEvent.press(submitButton);
  
    const validationError = queryByTestId("error-message");
    expect(validationError).toBeTruthy();
    expect(validationError.props.children)
        .toBe("Must select a category.");
  });

  it("Shows error message if no active time minutes is inputted.", () => {
    const {getByText, queryByTestId} = wrapper;

    const cyclingOption = getByText("Cycling");
    fireEvent.press(cyclingOption);

    const submitButton = getByText("Submit");
    fireEvent.press(submitButton);
  
    const validationError = queryByTestId("error-message");
    expect(validationError).toBeTruthy();
    expect(validationError.props.children)
        .toBe("Must input active time greater than 0.");
  });

  it("Shows error message if no weight is inputted", () => {
    const {getByText, queryByTestId, getByPlaceholderText} = wrapper;

    const cyclingOption = getByText("Cycling");
    fireEvent.press(cyclingOption);

    const activeMinutesTextInput = getByPlaceholderText("30 minutes"); 
    const enteredMinutes = "25,";
    fireEvent(activeMinutesTextInput, 'onChangeText', enteredMinutes);

    const submitButton = getByText("Submit");
    fireEvent.press(submitButton);
  
    const validationError = queryByTestId("error-message");
    expect(validationError).toBeTruthy();
    expect(validationError.props.children)
        .toBe("Must input a weight greater than 0.");
  });

  it("No error is displayed with all proper inputs.", () => {
    const {getByText, queryByTestId, getByPlaceholderText} = wrapper;

    const cyclingOption = getByText("Cycling");
    fireEvent.press(cyclingOption);

    const activeMinutesTextInput = getByPlaceholderText("30 minutes"); 
    const enteredMinutes = "25,";
    fireEvent(activeMinutesTextInput, 'onChangeText', enteredMinutes);

    const weightTextInput = getByPlaceholderText("140 pounds"); 
    const enteredWeight = "140";
    fireEvent(weightTextInput, 'onChangeText', enteredWeight);

    const submitButton = getByText("Submit");
    fireEvent.press(submitButton);
  
    const validationError = queryByTestId("error-message");
    expect(validationError).toBe(null);
  });
});

