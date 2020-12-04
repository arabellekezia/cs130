import {render, cleanup, fireEvent} from '@testing-library/react-native';
import React from 'react';
import LoginScreen from "../app/Screens/LoginScreen"

describe('Login Form', () => {
  let wrapper;
  beforeEach(() => {
      wrapper = render(<LoginScreen />);
    });
  afterEach(() => {
      cleanup();
      wrapper = null;
    });
  it('renders correctly', () => {
      expect(wrapper).toMatchSnapshot();
  });

  it("Shows 'Incorrect email or password' when user doesn't provide an email or password", () => {
    const {getByText, queryByTestId} = wrapper;
    
    const loginButton = getByText("Login");
    fireEvent.press(loginButton);
  
    const validationError = queryByTestId("error-message");
    expect(validationError).toBeTruthy();
    
    expect(validationError.props.children)
        .toBe("Incorrect email or password.");
  });

  it("Shows 'Incorrect email or password' when user provides only the email", () => {
    const {getByText, queryByTestId, getByPlaceholderText } = wrapper;
    
    const emailTextInput = getByPlaceholderText("Email"); 
    const enteredEmail = "test@gmail.com";
    fireEvent(emailTextInput, 'onChangeText', enteredEmail);

    const loginButton = getByText("Login");
    fireEvent.press(loginButton);
  
    const validationError = queryByTestId("error-message");
    expect(validationError).toBeTruthy();
    
    expect(validationError.props.children)
        .toBe("Incorrect email or password.");
  });

  it("No error message should appear with valid email and password.", () => {
    const {getByText, queryByTestId, getByPlaceholderText } = wrapper;
    
    const emailTextInput = getByPlaceholderText("Email"); 
    const enteredEmail = "test@gmail.com";
    fireEvent(emailTextInput, 'onChangeText', enteredEmail);

    const passwordTextInput = getByPlaceholderText("Password"); 
    const enteredPassword = "12345678";
    fireEvent(passwordTextInput, 'onChangeText', enteredPassword);

    const loginButton = getByText("Login");
    fireEvent.press(loginButton);
  
    const validationError = queryByTestId("error-message");
    expect(validationError).toBe(null);
  });
});

