import React from "react";
import { SafeAreaView, StyleSheet, Text } from "react-native";
import AppText from "../components/AppText";
import AppTextInput from "../components/AppTextInput";
import TextButton from "../components/TextButton";

function LoginScreen() {
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [err, setError] = React.useState({ email: false, password: false });

  function login() {
    if (!validate(email, password, setError)) {
      console.log(err);
    }
    console.log("Successfully logged in.");
  }

  function displayErrorMessage(err) {
    if (err.email || err.password) {
      return <ErrorMessage message="Incorrect email or password." />;
    }
  }

  return (
    <SafeAreaView style={styles.container}>
      <AppText
        style={{
          alignSelf: "flex-start",
          marginLeft: "5%",
          marginBottom: "5%",
          fontSize: 34,
        }}
        children="Welcome!"
      />
      <AppTextInput
        style={styles.textInput}
        placeholder="Email"
        icon="account"
        isError={err.email}
        onChangeText={(email) => {
          setEmail(email);
          setError({ email: false, password: false });
        }}
      />
      <AppTextInput
        style={styles.textInput}
        placeholder="Password"
        icon="lock"
        onChangeText={(password) => {
          setPassword(password);
          setError({ email: false, password: false });
        }}
        isError={err.password}
        secureTextEntry={true}
      />
      {displayErrorMessage(err)}
      <TextButton
        style={styles.submitButton}
        name="Login"
        onPress={login}
      />
      <Text style={{ marginVertical: "5%" }}>
        Don't have an account?
        <Text
          style={{ color: "#0079d3" }}
          onPress={() => {
            console.log("Navigate to the signup screen");
          }}
        >
          {" Sign up!"}
        </Text>
      </Text>
    </SafeAreaView>
  );
}

function ErrorMessage({ message }) {
  return (
    <AppText
      style={{
        alignSelf: "flex-start",
        marginLeft: "6%",
        color: "red",
      }}
      children={message}
    />
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

function validateEmail(email) {
  const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(String(email).toLowerCase());
}

function validate(email, password, setError) {
  const validEmail = validateEmail(email);
  const validPassword = Boolean(password);
  setError({ email: !validEmail, password: !validPassword });
  return validEmail && validPassword;
}

export default LoginScreen;
