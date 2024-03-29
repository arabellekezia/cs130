import React from "react";
import { SafeAreaView, StyleSheet, Text, View } from "react-native";
import { ScrollView } from "react-native-gesture-handler";
import AppText from "../components/AppText";
import AppTextInput from "../components/AppTextInput";
import TextButton from "../components/TextButton";
import AuthenticationService from "../services/AuthenticationService";

function SignupScreen({ navigation }) {
  const [name, setName] = React.useState("");
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [confirmPassword, setConfirmPassword] = React.useState("");
  const [err, setError] = React.useState({
    name: false,
    email: false,
    password: false,
    accountExists: false,
  });

  async function signup() {
    if (!validateFields({ name, email, password, confirmPassword }, setError)) {
      return;
    }
    const isSuccess = await AuthenticationService.signup(name, email, password);
    if (isSuccess) {
      navigation.navigate("Login");
    } else {
      setError({ email: true, accountExists: true });
    }
  }

  function displayErrorMessage(err) {
    if (err.name) {
      return <ErrorMessage message="Please enter your full name." />;
    }

    if (err.accountExists) {
      return (
        <ErrorMessage message="An account with this email already exists." />
      );
    }

    if (err.email) {
      return <ErrorMessage message="Please use a valid email." />;
    }

    if (err.password) {
      if (password.length < 8) {
        return (
          <ErrorMessage message="Password must be at least 8 characters long!" />
        );
      }
      return <ErrorMessage message="Passwords do not match." />;
    }
  }

  function resetErrors() {
    setError({ name: false, email: false, password: false });
  }

  return (
    <ScrollView
      contentContainerStyle={{
        flex: 1,
      }}
      keyboardShouldPersistTaps="handled"
    >
      <SafeAreaView style={styles.container}>
        <AppText
          style={{
            alignSelf: "flex-start",
            marginLeft: "5%",
            marginBottom: "5%",
            fontSize: 34,
          }}
          children="Let's get started!"
        />
        <AppTextInput
          style={styles.textInput}
          placeholder="Full name"
          icon="account"
          isError={err.name}
          onChangeText={(name) => {
            setName(name);
            resetErrors();
          }}
        />
        <AppTextInput
          style={styles.textInput}
          placeholder="Email"
          autoCapitalize="none"
          keyboardType="email-address"
          icon="email"
          isError={err.email}
          onChangeText={(email) => {
            setEmail(email);
            resetErrors();
          }}
        />
        <AppTextInput
          style={styles.textInput}
          placeholder="Password"
          icon="lock"
          onChangeText={(password) => {
            setPassword(password);
            resetErrors();
          }}
          isError={err.password}
          secureTextEntry={true}
        />
        <AppTextInput
          style={styles.textInput}
          placeholder="Confirm password"
          icon="lock"
          onChangeText={(password) => {
            setConfirmPassword(password);
            resetErrors();
          }}
          isError={err.password}
          secureTextEntry={true}
        />
        {displayErrorMessage(err)}
        <TextButton
          style={styles.submitButton}
          name="Sign Up"
          onPress={async () => await signup()}
        />
        <Text style={{ marginVertical: "5%" }}>
          Already have an account?
          <Text
            style={{ color: "#0079d3" }}
            onPress={() => {
              console.log("Navigate to the login screen");
              navigation.navigate("Login");
            }}
          >
            {" Log in!"}
          </Text>
        </Text>
      </SafeAreaView>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "white",
    alignItems: "center",
    justifyContent: "center",
  },
  textInput: {
    width: "90%",
  },
  submitButton: { marginVertical: 12, minWidth: "90%" },
});

function ErrorMessage({ message }) {
  return (
    <AppText
      style={{
        alignSelf: "flex-start",
        marginLeft: "6%",
        color: "red",
      }}
      testID="error-message"
      children={message}
    />
  );
}

function validateEmail(email) {
  const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(String(email).toLowerCase());
}

function validateFields(fields, setError) {
  const { name, email, password, confirmPassword } = fields;
  const validName = Boolean(name);
  if (!validName) {
    // Only error on the name field
    setError({ name: !validName, email: false, password: false });
    return validName;
  }

  const validEmail = validateEmail(email);
  if (!validEmail) {
    // Only error on the email field
    setError({ name: false, email: !validEmail, password: false });
    return validEmail;
  }

  const validPassword =
    Boolean(password) && password === confirmPassword && password.length >= 8;
  setError({ name: !validName, email: !validEmail, password: !validPassword });
  return validPassword;
}

export default SignupScreen;
