import {render, cleanup, fireEvent} from '@testing-library/react-native';
import React from 'react';
import SleepEntryFormScreen from "../app/Screens/SleepEntryFormScreen"

describe('Sleep entry input form', () => {
  let wrapper;
  beforeEach(() => {
      wrapper = render(<SleepEntryFormScreen route={{}} />);
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
        .toBe("Start date is invalid.");
  });
});

