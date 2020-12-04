import {render, cleanup, fireEvent} from '@testing-library/react-native';
import React from 'react';
import SignupScreen from "../app/Screens/SignupScreen"

describe('Signup Form', () => {
  let wrapper;
  beforeEach(() => {
      wrapper = render(<SignupScreen />);
    });
  afterEach(() => {
      cleanup();
      wrapper = null;
    });
  it('renders correctly', () => {
      expect(wrapper).toMatchSnapshot();
  });

  it("Shows invalid email error message when user provides an ill-formatted email", () => {
    const {getByText, queryByTestId, getByPlaceholderText} = wrapper;

    const fullNameInput = getByPlaceholderText("Full name"); 
    const enteredFullName = "Evan Lin";
    fireEvent(fullNameInput, 'onChangeText', enteredFullName);
    
    const emailTextInput = getByPlaceholderText("Email"); 
    const invalidEnteredEmail = "test";
    fireEvent(emailTextInput, 'onChangeText', invalidEnteredEmail);
    
    const signupButton = getByText("Sign Up");
    fireEvent.press(signupButton);
  
    const validationError = queryByTestId("error-message");
    expect(validationError).toBeTruthy();
    
    expect(validationError.props.children)
        .toBe("Please use a valid email.");
  });

  it("Shows missing name error when user doesn't provides their name", () => {
    const {getByText, queryByTestId, getByPlaceholderText} = wrapper;
    
    const signupButton = getByText("Sign Up");
    fireEvent.press(signupButton);
  
    const validationError = queryByTestId("error-message");
    expect(validationError).toBeTruthy();
    
    expect(validationError.props.children)
        .toBe("Please enter your full name.");
  });

  it("Shows password validation error message when the password is less than 8 characters long.", () => {
    const {getByText, queryByTestId, getByPlaceholderText} = wrapper;
    const fullNameInput = getByPlaceholderText("Full name"); 
    const enteredFullName = "Evan Lin";
    fireEvent(fullNameInput, 'onChangeText', enteredFullName);
    
    const emailTextInput = getByPlaceholderText("Email"); 
    const validEnteredEmail = "test@gmail.com";
    fireEvent(emailTextInput, 'onChangeText', validEnteredEmail);

    const passwordTextInput = getByPlaceholderText("Password"); 
    const passwordEntered = "1234567";
    fireEvent(passwordTextInput, 'onChangeText', passwordEntered);

    const signupButton = getByText("Sign Up");
    fireEvent.press(signupButton);
  
    const validationError = queryByTestId("error-message");
    expect(validationError).toBeTruthy();
    
    expect(validationError.props.children)
        .toBe("Password must be at least 8 characters long!");
  });

  it("Shows error when the password and confirm password inputs are mismatched.", () => {
    const {getByText, queryByTestId, getByPlaceholderText} = wrapper;
    const fullNameInput = getByPlaceholderText("Full name"); 
    const enteredFullName = "Evan Lin";
    fireEvent(fullNameInput, 'onChangeText', enteredFullName);
    
    const emailTextInput = getByPlaceholderText("Email"); 
    const validEnteredEmail = "test@gmail.com";
    fireEvent(emailTextInput, 'onChangeText', validEnteredEmail);

    const passwordTextInput = getByPlaceholderText("Password"); 
    const passwordEntered = "12345678";
    fireEvent(passwordTextInput, 'onChangeText', passwordEntered);

    const confirmPasswordTextInput = getByPlaceholderText("Confirm password"); 
    const confirmPasswordEntered = "12345677";
    fireEvent(confirmPasswordTextInput, 'onChangeText', confirmPasswordEntered);

    const signupButton = getByText("Sign Up");
    fireEvent.press(signupButton);
  
    const validationError = queryByTestId("error-message");
    expect(validationError).toBeTruthy();
    
    expect(validationError.props.children)
        .toBe("Passwords do not match.");
  });

  it("No error should be displayed when all valid inputs.", () => {
    const {getByText, queryByTestId, getByPlaceholderText} = wrapper;
    const fullNameInput = getByPlaceholderText("Full name"); 
    const enteredFullName = "Evan Lin";
    fireEvent(fullNameInput, 'onChangeText', enteredFullName);
    
    const emailTextInput = getByPlaceholderText("Email"); 
    const validEnteredEmail = "test@gmail.com";
    fireEvent(emailTextInput, 'onChangeText', validEnteredEmail);

    const passwordTextInput = getByPlaceholderText("Password"); 
    const passwordEntered = "12345678";
    fireEvent(passwordTextInput, 'onChangeText', passwordEntered);

    const confirmPasswordTextInput = getByPlaceholderText("Confirm password"); 
    const confirmPasswordEntered = "12345678";
    fireEvent(confirmPasswordTextInput, 'onChangeText', confirmPasswordEntered);

    const signupButton = getByText("Sign Up");
    fireEvent.press(signupButton);
  
    const validationError = queryByTestId("error-message");
    expect(validationError).toBe(null);
  });
});

